$(document).ready(function () {
    maskField()
    checkSize()
    checkFilter()
    if (!document.hidden || !document.webkitHidden) checkStatus()
    checkStatusFilter()
    count_table_td()
})
$(window).resize(function () {
    checkSize()
})

// href
$("body").on('click', '[href*="#"]', function (e) {
    var fixed_offset = 0;
    $('html,body').stop().animate({
        scrollTop: $(this.hash).offset().top - fixed_offset
    }, 1000);
    e.preventDefault();
});

$(document).on('click', '.checkField', function (el) {
    el.preventDefault();
    checkField(el)
})

function checkField(el) {
    let field = $(el.target).parents('form').find('input, textarea, select'),
        rating = $(el.target).parents('form').find('.rating-mini')

    for (let i = 0; i < field.length; i++) {
        if (!$(field[i]).hasClass('no-r')) {
            if ($(field[i]).val() != null) {
                if ($(field[i]).val() != '') {
                    if ($(field[i]).attr('type') == 'phone' || $(field[i]).hasClass('phone') || $(field[i]).attr('id') == 'phone' || $(field[i]).attr('name') == 'phone') {
                        if ($(field[i]).val().length < 17) {
                            $(field[i]).addClass('error')
                        } else {
                            $(field[i]).removeClass('error')
                        }
                    } else {
                        $(field[i]).removeClass('error')
                    }
                    if ($(field[i]).attr('type') == 'radio') {
                        if (!$(field[i]).hasClass('secondary')) {
                            let inputName = $(field[i]).attr('name'),
                                inputCheckedAll = $(el.target).parents('form').find(`input[name='${inputName}']`),
                                inputChecked = $(el.target).parents('form').find(`input[name='${inputName}']:checked`)
                            if (inputChecked.length == 0) {
                                inputCheckedAll.addClass('error')
                            } else {
                                inputCheckedAll.removeClass('error')
                            }
                        }
                    } else {
                        if (!$(field[i]).hasClass('gocity')) {
                            $(field[i]).removeClass('error')
                        } else {
                            let t = 0
                            for (let j = 0; j < $(field[i]).parents('.form-group-auto-row').find('.list.list-directions ul li').length; j++) {
                                if (t = 0) {
                                    if ($(field).eq(i).val() != $(field).eq(i).parents('.form-group-auto-row').find('.list.list-directions ul li').eq(j).text()) {
                                        $(field).eq(i).addClass('error')
                                    } else {
                                        $(field).eq(i).removeClass('error')
                                        t++
                                    }
                                }
                            }
                        }
                    }
                    if ($(field[i]).attr('type') == 'checkbox') {
                        if (!$(field[i]).hasClass('secondary')) {
                            let inputName = $(field[i]).attr('name'),
                                inputCheckedAll = $(el.target).parents('form').find(`input[name='${inputName}']`),
                                inputChecked = $(el.target).parents('form').find(`input[name='${inputName}']:checked`)
                            if (inputChecked.length == 0) {
                                inputCheckedAll.addClass('error')
                            } else {
                                inputCheckedAll.removeClass('error')
                            }
                        }
                    } else {
                        if (!$(field[i]).hasClass('gocity')) {
                            $(field[i]).removeClass('error')
                        } else {
                            let t = 0
                            for (let j = 0; j < $(field[i]).parents('.form-group-auto-row').find('.list.list-directions ul li').length; j++) {
                                if (t = 0) {
                                    if ($(field).eq(i).val() != $(field).eq(i).parents('.form-group-auto-row').find('.list.list-directions ul li').eq(j).text()) {
                                        $(field).eq(i).addClass('error')
                                    } else {
                                        $(field).eq(i).removeClass('error')
                                        t++
                                    }
                                }
                            }
                        }
                    }
                    if ($(field[i]).attr('type') == 'email') {
                        if (isValidEmail($(field[i]).val())) {
                            $(field[i]).removeClass('error')
                        } else {
                            $(field[i]).addClass('error')
                        }
                    }
                } else {
                    $(field[i]).addClass('error')
                }
            } else {
                $(field[i]).addClass('error')
            }
        } else {
            if ($(field[i]).attr('type') == 'email' && $(field[i]).val() != '') {
                if (isValidEmail($(field[i]).val())) {
                    $(field[i]).removeClass('error')
                } else {
                    $(field[i]).addClass('error')
                }
            } else {
                if (!$(field[i]).hasClass('gocity')) {
                    $(field[i]).removeClass('error')
                } else {
                    let t = 0
                    for (let j = 0; j < $(field[i]).parents('.form-group-auto-row').find('.list.list-directions ul li').length; j++) {
                        if (t = 0) {
                            if ($(field).eq(i).val() != $(field).eq(i).parents('.form-group-auto-row').find('.list.list-directions ul li').eq(j).text()) {
                                $(field).eq(i).addClass('error')
                            } else {
                                $(field).eq(i).removeClass('error')
                                t++
                            }
                        }
                    }
                }
            }
        }
    }
    if ($(rating).find('span.active').length == 0) {
        $(rating).addClass('error')
    } else {
        $(rating).removeClass('error')
    }
    if ($(el.target).parents('form').find('.error').length == 0) {
        sendAjax(field, el)
        clearFields(el)
    }
}

function clearFields(el) {
    $(el.target).parents('form').find('input:not([type=checkbox]):not([name=csrfmiddlewaretoken])').val('')
    $(el.target).parents('form').find('textarea').val('')
    $(el.target).parents('form').find('.__select__title').removeClass('error')
}

function isValidEmail(email) {
    let emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailPattern.test(email);
}

function sendAjax(dataForm, el) {
    let obj = {},
        type = $(el.target).attr('data-request'),
        titleText = $('.modal#infoModal .modal-header'),
        bodyText = $('.modal#infoModal .modal-body')

    $.each(dataForm, function (i, el) {
        let name = $(el).attr('name'),
            value = $(el).val();
        if (obj[name] !== undefined) {
            if ($(el).is(':checked')) {
                obj[name] = value;
            }
        } else {
            if (name === 'proxy') {
                let urls = value.split('\n'),
                    arrayProxy = []
                urls.forEach(function(url) {
                    let new_url = new URL(url)
                    arrayProxy.push({
                        "ip_address": new_url.hostname,
                        "port": new_url.port,
                        "username": new_url.username,
                        "password": new_url.password,
                        "protocol": new_url.protocol.replace(":", "")
                    })
                })
                obj['proxy'] = arrayProxy
            } else {
                if (value) {
                    obj[name] = value;
                }
            }
        }
    });
    if (type === 'delete_phrases' || type === 'delete_projects') {
        obj['id'] = $(el.target).attr('data-id')
    }
    if (type === 'delete_selected_phrases') {
        let id_array = []
        $(el.target).parents('.accordion-item').find('td input:checked').map(function(i, item) {
            id_array.push($(item).val())
        })
        obj['id_array'] = id_array
    }
    if (type === 'delete_selected_projects') {
        let id_array = []
        $(el.target).parents('.info-block-main').find('table td input:checked').map(function(i, item) {
            id_array.push($(item).val())
        })
        obj['id_array'] = id_array
    }
    if (type === 'change_selected_phrases' || type === 'change_selected_domains' || type === 'change_selected_urls' || type === 'change_selected_shots') {
        let id_array = []
        $(el.target).parents('.info-block-main').find('table td input:checked').map(function(i, item) {
            id_array.push($(item).val())
        })
        obj['id_array'] = id_array
        obj['status'] = $(el.target).parents('.change').find('select.status-all-change option:selected').val()
    }
    if (type === 'update_proxy' || type === 'delete_proxy') {
        obj['id'] = Number($(el.target).attr('data-id'))
    }
    if (type === 'get_phrases') {
        obj['id'] = Number($(el.target).parents('.accordion-item').attr('data-id'))
    }

    obj['type'] = type
    let csrftoken = $("input[name='csrfmiddlewaretoken']").val();
    $.ajax({
        url: '/ajax/',
        method: "POST",
        data: JSON.stringify(obj),
        headers: {
            'X-CSRFToken': csrftoken,
        },
        success: function (response) {
            if (response.error) {
                console.log(response.error)
            } else {
                if (type === 'new_group') {
                    $('#infoModal').modal('hide')
                    $('.group_select').html(response);
                    $('.group_select option:last').prop('selected', true);
                    $('.indexSection .item.phrase').removeClass('d-none')
                } else if (type === 'save_phrase') {
                    $('.message_phrase').html('<span style="color:green;">Phrases added successfully</span>');
                    setTimeout(function () {
                        $('.message_phrase').html('')
                    }, 1500)
                    $('.accordion-phrase').html(response);
                } else if (type === 'delete_phrases' || type === 'delete_projects') {
                    if (response.delete) {
                        $(el.target).parents('tr').fadeOut().remove()
                    }
                } else if (type === 'delete_selected_phrases') {
                    if (response.delete) {
                        $(el.target).parents('tr').fadeOut().remove()
                        obj['id_array'].map(function(i, item) {
                            $(`.accordion-item tr td input[value=${i}]`).parents('tr').fadeOut().remove()
                        })
                    }
                } else if (type === 'delete_selected_projects') {
                    if (response.delete) {
                        $(el.target).parents('tr').fadeOut().remove()
                        obj['id_array'].map(function(i, item) {
                            $(`table.table tr td input[value=${i}]`).parents('tr').fadeOut().remove()
                        })
                    }
                } else if (type === 'change_selected_phrases' || type === 'change_selected_domains' || type === 'change_selected_urls' || type === 'change_selected_shots') {
                    if (response.change) {
                        $(el.target).parents('tr').fadeOut().remove()
                        obj['id_array'].map(function(i, item) {
                            let value = $(el.target).parents('.change').find('select.status-all-change option:selected').text(),
                                block = $(`table.table tr td input[value=${i}]`)
                            $(block).parents('tr').fadeOut().find('td.status-td').text(value)
                            $(block).parents('tr').fadeOut().fadeIn()
                        })
                    }
                } else if (type === 'add_proxy') {
                    $('.message_proxy').html('<span style="color:green;">Proxies added successfully</span>');
                    setTimeout(function () {
                        $('.message_proxy').html('')
                    }, 1500)
                    $('.proxyListSection .info-block-main').html(response);
                } else if (type === 'update_proxy') {
                    $(el.target).parents('form').find('.field').append('<div class="message_status"><span style="color:green;">Proxies have been successfully updated</span></div>')
                     setTimeout(function () {
                        $(el.target).parents('form').find('.field .message_status').remove()
                    }, 1500)
                } else if (type === 'delete_proxy') {
                    if (response.delete) {
                        $(el.target).parents('.proxy-item').fadeOut().remove()
                    }
                } else if (type === 'get_phrases') {
                    $(`.accordion-phrase .accordion-item .accordion-body .table tbody`).html('')
                    $(`.accordion-phrase .accordion-item[data-id=${obj['id']}] .accordion-body .table tbody`).html(response)
                }
            }
        }
    });

    // console.log(dataForm);
    // // alert('Запрос Ajax')
    // // titleText.html('')
    // // bodyText.html('')
    // if (type == 'success') {
    //     window.location.href = '/success.html'
    // } else if (type == 'reviews') {
    //     window.location.href = '/success-review.html'
    // }
}

function maskField() {
    $(".mask-phone").click(function () {
        $(this).setCursorPosition(3);
    }).mask("+7(999) 999-9999");
    // $(".mask-phone").mask("+7 (999) 999-99-99");
    $('.mask-date').mask('99.99.9999');
}

$.fn.setCursorPosition = function (pos) {
    if ($(this).get(0).setSelectionRange) {
        $(this).get(0).setSelectionRange(pos, pos);
    } else if ($(this).get(0).createTextRange) {
        var range = $(this).get(0).createTextRange();
        range.collapse(true);
        range.moveEnd('character', pos);
        range.moveStart('character', pos);
        range.select();
    }
};

function checkSize() {

}

$(document).on('click', '.open-modal', function (el) {
    el.preventDefault()
    infoOpenModal(el)
})

function infoOpenModal(elem) {
    let type = $(elem.target).attr('data-type-modal'),
        titleText = $('.modal#infoModal .modal-header'),
        bodyText = $('.modal#infoModal .modal-body')
    titleText.html('')
    bodyText.html('')
    if (type === 'add-group') {
        titleText.html(`
            <div class="h1 _title36 modal-title" id="exampleModalLabel">Добавить проект</div>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Закрыть"></button>
        `)
        bodyText.html(`
            <form class="application-block">
                <input class="group_add" placeholder="Новый проект" name="name">
                <div class="btn checkField" data-request="new_group">Создать новый проект</div>
            </form>
        `)
    }
    maskField()
    $('#infoModal').modal('show')
}

$('.left-col .list ul li > a.openSub').on('click', function () {
    $(this).parent('li').toggleClass('open')
})

$('.main-container .left-col .func .item.open-all').on('click', function () {
    if ($('.left-col .list ul li > a.openSub').parent('li').length == $('.left-col .list ul li > a.openSub').parent('li.open').length) {
        $('.left-col .list ul li > a.openSub').parent('li').removeClass('open')
    } else {
        $('.left-col .list ul li > a.openSub').parent('li').addClass('open')
    }
})

$('.select-block').on('click', function () {
    if ($(this).hasClass('active')) {
        $(this).removeClass('active');
    } else {
        $(this).addClass('active');
    }
});
$('.select-block input').on('click', function (el) {
    el.stopPropagation();
});

$('table .delete').on('click', function(el) {
    el.preventDefault()
    sendAjax('', el)
})

$('form .search_filter_btn').on('click', function (el) {
    el.preventDefault();
    let dataArray = $('form.nameFilter-block').serializeArray();
    let mergedData = {};

    $.each(dataArray, function (index, item) {
        const paramName = item.name;
        if ((item.name.endsWith('__gte') || item.name.endsWith('__lte')) && item.value !== '') {
            if (mergedData[paramName] !== undefined) {
                let existingValues = mergedData[paramName].split(',');
                let newValues = item.value.split(',');
                let mergedValues = Array.from(new Set(existingValues.concat(newValues)));
                mergedData[paramName] = mergedValues.join(',');
            } else {
                mergedData[paramName] = item.value;
            }
        } else if (item.value !== '') {
            if (mergedData[paramName] !== undefined) {
                mergedData[paramName] = mergedData[paramName] + ',' + item.value;
            } else {
                mergedData[paramName] = item.value;
            }
        }
    });

    let mergedSerializedData = $.param(mergedData),
        decodedSerializedData = decodeURIComponent(mergedSerializedData),
        filter = window.location.search,
        urlParams = new URLSearchParams(window.location.search);

    if (urlParams.get("filter_p_sort") !== null) {
    if (urlParams.get("p") !== null) {
      window.location.search = decodedSerializedData + `&filter_p_sort=${urlParams.get("filter_p_sort")}&p=${urlParams.get("p")}`;
    } else {
      window.location.search = decodedSerializedData + `&filter_p_sort=${urlParams.get("filter_p_sort")}`;
    }
    } else {
    if (urlParams.get("p") !== null) {
      window.location.search = decodedSerializedData + `&p=${urlParams.get("p")}`;
    } else {
      window.location.search = decodedSerializedData;
    }
    }
});

function checkFilter() {
    let filter = window.location.search;
    let params = new URLSearchParams(filter);

    // Проход по каждому ключу параметров URL
    params.forEach(function (value, key) {
        // Исключение для ключа "stocks и available"

        // Поиск полей ввода с совпадающим именем ключа
        $('input[name="' + key + '"]').each(function () {
            let inputValues = $(this).val().split(',');

            let hasMatchingValues = ''
            if (key !== 'available' && key !== 'stocks') {
                // Проверка наличия совпадающих значений
                hasMatchingValues = inputValues.some(function (inputValue) {
                    return value.split(',').includes(inputValue);
                });
            }

            if (hasMatchingValues) {
                $(this).prop('checked', true);
                $(this).parents('.group_block').addClass('active')
            }
        });
    });
}

$('form .reset').on('click', function(el) {
    el.preventDefault()
    window.location.search = ''
})

$('.group_select').on('change', function() {
    $('.indexSection .item.phrase').removeClass('d-none')
})

$('.status-all-search-block .f-status').on('click', function() {
    let selectedValue = $('.status-all-search').val(),
        filter = window.location.search,
        type = $('.status-all-search').attr('name'),
        regex = new RegExp(`[?&]?${type}=[^&]+`, 'gi');

    if (window.location.href.indexOf(type) !== -1) {
        window.location.search = `${filter.replace(regex, '')}&${type}=${selectedValue}`
    } else {
        if (window.location.href.indexOf('?') !== -1) {
            window.location.search = `${filter}&${type}=${selectedValue}`
        } else {
            window.location.search = `?${type}=${selectedValue}`
        }
    }
});

$('.status-all-search-block .reset-status').on('click', function() {
    let currentUrl = window.location.href;
    let searchParams = new URLSearchParams(window.location.search);
    let paramName = $('.status-all-search').attr('name');
    if (searchParams.has(paramName)) {
        searchParams.delete(paramName);
        let newUrl = `${window.location.origin}${window.location.pathname}?${searchParams.toString()}`;
        window.history.replaceState({ path: newUrl }, '', newUrl);
        location.reload();
    }
});

function checkStatus() {
    let accordion = $('.accordion-phrase .accordion-item')
    for (let i=0; i<accordion.length; i++) {
        let id = $(accordion).eq(i).attr('data-id')
        $.ajax({
            url: `/api/searchqueries/?project=${id}`,
            method: "GET",
            success: function (response) {
                if (response.length) {
                    let count = response.length, // всего
                        added = 0, // добавлен
                        done = 0, // сделано
                        inprogress = 0, // в процессе
                        error = 0, // ошибка
                        status
                    for (let j=0; j<count; j++) {
                        if (response[j].status === 0) {
                            added++
                        } else if (response[j].status === 1) {
                            done++
                        } else if (response[j].status === 2) {
                            inprogress++
                        } else if (response[j].status === 3) {
                            error++
                        }
                    }
                    if (done === count) {
                        status = 'Completed'
                    } else if (done+added === count) {
                        status = 'There are not verified'
                    } else if (done+error === count) {
                        status = 'There are errors'
                    } else if (done+error+added === count) {
                        status = 'There are tested, not tested and errors'
                    } else if (error+added === count) {
                        status = 'There are errors and not verified'
                    } else if (error === count) {
                        status = 'Error'
                    } else if (added === count) {
                        status = 'Added'
                    } else {
                        status = 'In process'
                    }
                    $('.accordion-phrase').find(`.accordion-item[data-id=${id}] .status`).html(`<span data-request="get_phrases">${done}/${count} (${((done/count)*100).toFixed(1)}%)</span><span data-request="get_phrases">${status}</span>`)
                }
            }
        });
    }
}

setInterval(function() {
    if (!document.hidden || !document.webkitHidden) checkStatus()
}, 5000)

$('.status-all-search').on('change', function() {
    checkStatusFilter()
})

function checkStatusFilter() {
    if ($('.status-all-search').val() !== null) {
        $('.status-all-search-block .f-status').addClass('active')
    }
}

function createNestedStructure(data, el) {
    const ul = $('<ul class="list-domain">');
    if (typeof data === 'object') {
        $.each(data, function(key, value) {
            if (key !== 'count') {
                if (value.count > 0) {
                    if (value.link) {
                        const link = $('<a>')
                            .attr('href', `/urls/${value.id}/`)
                            .text(value.link);
                        const li = $('<li class="main-title">').append(link);
                        ul.append(li);
                    } else {
                        const nestedUl = createNestedStructure(value);
                        const li = $('<li>').append(nestedUl);
                        li.append(`<div class="count">${value.count}</div>`);
                        ul.append(li);
                    }
                } else {
                    const nestedUl = createNestedStructure(value, el);
                    ul.append(nestedUl);
                }
            }
        });
    }
    $(el).append(ul);
    return ul;
}

$(document).on('click', '.more_urls a', function (el) {
    el.stopPropagation();
})

$(document).on('click', '.more_urls', function (el) {
    const id = Number($(this).attr('data-id'));
    if (!$(el.target).parents('tr').next('tr.list-images-block').hasClass('list-images-block')) {
        $('.table .list-images-block').remove()
        $('.table tr').removeClass('active')
        $(el.target).parents('tr').after(`<tr class="list-images-block"><td colspan="13" class="list-images"><div class="list-images-main"></div></td></tr>`)
        const tr = $(el.target).parents('tbody').find('tr.list-images-block td.list-images .list-images-main')
        $.ajax({
            url: `/get-urls-domain/${id}/`,
            type: 'get',
            dataType: 'json',
            async: false,
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
            },
            success: function(response) {
                createNestedStructure(response.nested_urls, tr);
                $('.list-images-block').prev(tr).addClass('active')
            }
        });

        // const imageSliderBlock = $(el.target).parents('tbody').find('tr.list-images-block td.list-images .list-images-main')
        // $.ajax({
        //     url: `/api/domain_photo/?domain_id=${id}`, // Передаем URL как часть запроса
        //     type: 'get',
        //     dataType: 'json',
        //     headers: {
        //         'X-CSRFToken': getCookie('csrftoken'),
        //     },
        //     success: function(response) {
        //         $(imageSliderBlock).append(`<div class="slider"><div class="swiper galleryDomainSlider"><div class="swiper-wrapper"></div><div class="swiper-button-next"></div><div class="swiper-button-prev"></div></div></div>`)
        //         let imageSlider = $(imageSliderBlock).find('.swiper .swiper-wrapper')
        //         new Swiper(".galleryDomainSlider", {
        //           navigation: {
        //             nextEl: ".swiper-button-next",
        //             prevEl: ".swiper-button-prev",
        //           },
        //         });
        //         if (response) {
        //             for (let i=0; i<response.length; i++) {
        //                 $(imageSlider).append(`
        //                     <div class="swiper-slide"><img src="${response[i].photo}" alt=""></div>
        //                 `)
        //             }
        //         } else {
        //             console.log('Ошибка при получении скриншота');
        //         }
        //     },
        //     error: function(response) {
        //         console.log(response);
        //     }
        // });
    } else {
        $('.table .list-images-block').remove()
        $('.table tr').removeClass('active')
    }
});

function count_table_td() {
  let count_table = 0;
  for (let i = 0; i < $('.table.tree-count-results td.count-td').length; i++) {
    let block = $('.table.tree-count-results td.count-td').eq(i);
    let count = 0;
    for (let j = 0; j < $(block).find('> span').length; j++) {
      count += Number($(block).find('> span').eq(j).text());
    }
    count_table += count;
    $(block).append(count);
  }
  $('.table.tree-count-results .count-th > span').text(`(${count_table})`);
}

$('.checks_all').on('click', function(){
    if($(this).prop('checked')){
        let checking = $(this).parents('table').find('.checks').map(function(i, el){
            return $(el).prop('checked', true);
        }).get();
    }else{
        let checking = $(this).parents('table').find('.checks').map(function(i, el){
            return $(el).prop('checked', false);
        }).get();
    }
});

$(document).on('click', '.info-block-main .delete-selected, .info-block-main .delete-proxy, .info-block-main .change-selected, .phrasesSection .accordion-phrase .accordion-item .accordion-header', function (el) {
    sendAjax('', el)
})
$(document).on('click', '.info-block-main .update-proxy', function (el) {
    sendAjax($(el.target).parents('form').find('input[name=proxy]'), el)
})
$(document).on('click', '.phrasesSection .accordion-phrase .accordion-item .accordion-header', function (el) {
    $(`.accordion-phrase .accordion-item .accordion-body .table tbody`).html('')
})

$('.page-item .page-link').on('click', function(el) {
    el.preventDefault()
    let selectedValue = $(this).attr('href'),
        filter = window.location.search,
        type = 'page',
        regex = new RegExp(`[?&]?${type}=[^&]+`, 'gi');
    selectedValue = selectedValue.replace('?page=', '');

    if (window.location.href.indexOf(type) !== -1) {
        window.location.search = `${filter.replace(regex, '')}&${type}=${selectedValue}`
    } else {
        if (window.location.href.indexOf('?') !== -1) {
            window.location.search = `${filter}&${type}=${selectedValue}`
        } else {
            window.location.search = `?${type}=${selectedValue}`
        }
    }
});

$('.search-name input').on('input', function() {
    let temp = $(this).val()
    if (temp) {
        $(this).parents('.info-block-main').find('.accordion .accordion-item').each(function () {
            if ($(this).find('.accordion-button').text().toLowerCase().indexOf(temp.toLowerCase()) > -1) {
                $(this).removeClass('d-none')
            } else {
                $(this).addClass('d-none')
            }
        })
    } else {
        $(this).parents('.info-block-main').find('.accordion .accordion-item').each(function () {
            $(this).removeClass('d-none')
        })
    }
})