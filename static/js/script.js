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
                urls.forEach(function (url) {
                    let regex = /^([^:]+)(:\/\/)?([^:]+):([^@]+)@([^:]+):(\d+)$/;
                    let match = url.match(regex);
                    if (match) {
                        if (match[2] === '://') {
                            let protocol = match[1];
                            let username = match[3];
                            let password = match[4];
                            let ipAddress = match[5];
                            let port = match[6];
                            arrayProxy.push({
                                "ip_address": ipAddress,
                                "port": port,
                                "username": username,
                                "password": password,
                                "protocol": protocol
                            })
                        }
                    }
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
        $(el.target).parents('.accordion-item').find('td input:checked').map(function (i, item) {
            id_array.push($(item).val())
        })
        obj['id_array'] = id_array
    }
    if (type === 'delete_selected_projects') {
        let id_array = []
        $(el.target).parents('.info-block-main').find('table td input:checked').map(function (i, item) {
            id_array.push($(item).val())
        })
        obj['id_array'] = id_array
    }
    if (type === 'change_selected_phrases' || type === 'change_selected_domains' || type === 'change_selected_urls' || type === 'change_selected_shots') {
        let id_array = []
        $(el.target).parents('.info-block-main').find('table td input:checked').map(function (i, item) {
            id_array.push($(item).val())
        })
        obj['id_array'] = id_array
        obj['status'] = $(el.target).parents('.change').find('select.status-all-change option:selected').val()
    }
    if (type === 'update_proxy' || type === 'delete_proxy') {
        obj['id'] = Number($(el.target).attr('data-id'))
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
                console.error(response.error)
            } else {
                if (type === 'new_group') {
                    $('#infoModal').modal('hide')
                    $('.group_select').html(response);
                    $('.group_select option:last').prop('selected', true);
                    $('.indexSection .item.phrase').removeClass('d-none')
                } else if (type === 'save_phrase') {
                    showToasts('Phrases added successfully', 'text-bg-success')
                    // $('.message_phrase').html('<span style="color:green;">Phrases added successfully</span>');
                    // setTimeout(function () {
                    //     $('.message_phrase').html('')
                    // }, 1500)
                    $('.list').html(response);
                } else if (type === 'delete_phrases' || type === 'delete_projects') {
                    if (response.delete) {
                        $(el.target).parents('tr').fadeOut().remove()
                    }
                } else if (type === 'delete_selected_phrases') {
                    if (response.delete) {
                        $(el.target).parents('tr').fadeOut().remove()
                        obj['id_array'].map(function (i, item) {
                            $(`.accordion-item tr td input[value=${i}]`).parents('tr').fadeOut().remove()
                        })
                    }
                } else if (type === 'delete_selected_projects') {
                    if (response.delete) {
                        $(el.target).parents('tr').fadeOut().remove()
                        obj['id_array'].map(function (i, item) {
                            $(`table.table tr td input[value=${i}]`).parents('tr').fadeOut().remove()
                        })
                    }
                } else if (type === 'change_selected_phrases' || type === 'change_selected_domains' || type === 'change_selected_urls' || type === 'change_selected_shots') {
                    if (response.change) {
                        $(el.target).parents('tr').fadeOut().remove()
                        obj['id_array'].map(function (i, item) {
                            let value = $(el.target).parents('.change').find('select.status-all-change option:selected').text(),
                                block = $(`table.table tr td input[value=${i}]`)
                            $(block).prop('checked', false)
                            $('.checks_all').prop('checked', false)
                            if (type !== 'change_selected_domains' && type !== 'change_selected_phrases') {
                                $(block).parents('tr').fadeOut().find('td.status-td').text(value)
                                $(block).parents('tr').fadeOut().fadeIn()
                            }
                        })
                    }
                } else if (type === 'add_proxy') {
                    $('.message_proxy').html('<span style="color:green;">Proxies added successfully</span>');
                    setTimeout(function () {
                        $('.message_proxy').html('')
                    }, 1500)
                    $('.proxyListSection .info-block-main').html(response);
                } else if (type === 'update_proxy') {
                    if (response.error_message) {
                        $(el.target).parents('form').find('.field').append(`<div class="message_status"><span style="color:red;">${response.error_message}</span></div>`)
                    } else {
                        $(el.target).parents('form').find('.field').append(`<div class="message_status"><span style="color:green;">Proxies have been successfully updated</span></div>`)
                    }
                    setTimeout(function () {
                        $(el.target).parents('form').find('.field .message_status').remove()
                    }, 2000)
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
            <div class="h1 _title36 modal-title" id="exampleModalLabel">Add a project</div>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
        `)
        bodyText.html(`
            <form class="application-block">
                <input class="group_add" placeholder="New project" name="name">
                <div class="btn checkField" data-request="new_group">Create a new project</div>
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

$('table .delete').on('click', function (el) {
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

$('form .reset').on('click', function (el) {
    el.preventDefault()
    window.location.search = ''
})

$('.group_select').on('change', function () {
    $('.indexSection .item.phrase').removeClass('d-none')
})

$('.status-all-search-block .f-status').on('click', function () {
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

$('.status-all-search-block .reset-status').on('click', function () {
    let currentUrl = window.location.href;
    let searchParams = new URLSearchParams(window.location.search);
    let paramName = $('.status-all-search').attr('name');
    if (searchParams.has(paramName)) {
        searchParams.delete(paramName);
        let newUrl = `${window.location.origin}${window.location.pathname}?${searchParams.toString()}`;
        window.history.replaceState({path: newUrl}, '', newUrl);
        location.reload();
    }
});

function checkStatus() {
    let accordion = $('.accordion-phrase .accordion-item')
    for (let i = 0; i < accordion.length; i++) {
        let id = $(accordion).eq(i).attr('data-id')
        $.ajax({
            url: `/api/searchqueries/check_status/?project=${id}`,
            method: "GET",
            success: function (response) {
                $('.accordion-phrase').find(`.accordion-item[data-id=${id}] .status`).html(`<span data-request="get_phrases">${response.status}</span>`)
            }
        });
    }
}

setInterval(function () {
    if (!document.hidden || !document.webkitHidden) checkStatus()
}, 5000)

$('.status-all-search').on('change', function () {
    checkStatusFilter()
})

function checkStatusFilter() {
    if ($('.status-all-search').val() !== null) {
        $('.status-all-search-block .f-status').addClass('active')
    }
}

function createNestedStructure(data, el) {
    const ul = $('<ul>');
    if (typeof data === 'object') {
        $.each(data, function (key, value) {
            if (value.count > 1) {
                $(ul).addClass('sub-ul-menu')
            }

            if (key !== 'id' && key !== 'count' && key !== '' && key !== 'last') {
                if (value.link && value.link.slice(-1) === "/") {
                    const li = $(`<li><a href="/urls/${value.id}/">${value.link}</a></li>`);
                    ul.append(li);
                } else {
                    const li = $('<li class="folder"></li>');
                    if (value.last && value.count === 1) $(li).addClass('not-nested')
                    if (!value.last) {
                        let arrow = $(`<div class="down"><i class="fa-solid fa-chevron-right"></i></div><span>${value.link || key}</span>`)
                        li.append(arrow);
                        ul.append(li);
                    } else {
                        if (value.count === 1) {
                            $.each(data, function (key, value) {
                                if (value.id) {
                                    li.append(`<a href="/urls/${value.id}/">${value.link}</a>`);
                                    ul.append(li);
                                }
                            })
                        } else {
                            let arrow = $(`<div class="down"><i class="fa-solid fa-chevron-right"></i></div><span>${value.link || key}</span>`)
                            li.append(arrow);
                            ul.append(li);
                        }
                    }
                }
            }

            if (value.count) {
                let li_main = $('<li>');
                if (key !== '') $(li_main).addClass('li_1')
                if (value.last) $(li_main).addClass('li_2')
                if (!key) $(li_main).addClass('main-title')
                if (value.count > 1) $(li_main).addClass('subMenu')

                if (value.link) {
                    const link = $(`<a href="/urls/${value.id}/">${value.link}</a>`)
                    li_main.append(link)
                    ul.append(li_main);
                } else {
                    const nestedUl = createNestedStructure(value, el);
                    ul.append(nestedUl);
                }
            } else {
                const nestedUl = createNestedStructure(value, el);
                ul.append(nestedUl);
            }
        });
    }
    $(el).append(ul);
    return ul;
}

$(document).on('click', '.more_urls a', function (el) {
    el.stopPropagation();
})
$(document).on('click', '.more_urls input', function (el) {
    el.stopPropagation();
})

let galleryDomainSlider
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
            success: function (response) {
                createNestedStructure(response.nested_urls, tr);
                $('.list-images-block').prev(tr).addClass('active')
            }
        });

        const imageSliderBlock = $(el.target).parents('tbody').find('tr.list-images-block td.list-images .list-images-main')
        $.ajax({
            url: `/api/domain_images/?domain_id=${id}`, // Передаем URL как часть запроса
            type: 'get',
            dataType: 'json',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
            },
            success: function (response) {
                $(imageSliderBlock).append(`<div class="slider"><div class="swiper galleryDomainSlider"><div class="swiper-wrapper"></div><div class="swiper-button-next"></div><div class="swiper-button-prev"></div><div class="swiper-pagination"></div></div></div>`)
                let imageSlider = $(imageSliderBlock).find('.swiper .swiper-wrapper')
                galleryDomainSlider = new Swiper(".galleryDomainSlider", {
                    spaceBetween: 20,
                    navigation: {
                        nextEl: ".swiper-button-next",
                        prevEl: ".swiper-button-prev",
                    },
                    pagination: {
                        el: ".swiper-pagination",
                        type: "fraction",
                    },
                });
                if (response) {
                    for (let i = 0; i < response.length; i++) {
                        const imageUrl = response[i].photo;
                        const fileNameWithoutExtension = imageUrl.split('/').pop().split('.')[0];
                        $(imageSlider).append(`
                            <div class="swiper-slide"><img src="${imageUrl}" loading="lazy" alt=""><div class="info"><span>${fileNameWithoutExtension}</span><div class="copy"><i class="fa-regular fa-copy"></i></div></div><div class="swiper-lazy-preloader swiper-lazy-preloader-black"></div></div>
                        `)
                    }
                } else {
                    console.log('Error when getting a screenshot');
                }
            },
            error: function (response) {
                console.log(response);
            }
        });
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

$('.checks_all').on('click', function () {
    if ($(this).prop('checked')) {
        let checking = $(this).parents('table').find('.checks').map(function (i, el) {
            return $(el).prop('checked', true);
        }).get();
    } else {
        let checking = $(this).parents('table').find('.checks').map(function (i, el) {
            return $(el).prop('checked', false);
        }).get();
    }
});

$(document).on('click', '.info-block-main .delete-selected, .info-block-main .delete-proxy, .info-block-main .change-selected', function (el) {
    sendAjax('', el)
})
$(document).on('click', '.info-block-main .update-proxy', function (el) {
    sendAjax($(el.target).parents('form').find('input[name=proxy]'), el)
})

$('.page-item .page-link').on('click', function (el) {
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

$('.search-name input').on('input', function () {
    let temp = $(this).val()
    if (temp) {
        $(this).parents('.info-block-main').find('.list > a').each(function () {
            if ($(this).text().toLowerCase().indexOf(temp.toLowerCase()) > -1) {
                $(this).removeClass('d-none')
            } else {
                $(this).addClass('d-none')
            }
        })
    } else {
        $(this).parents('.info-block-main').find('.list > a').each(function () {
            $(this).removeClass('d-none')
        })
    }
})

$(document).on('click', 'ul.first-list li.folder', function (el) {
    $(this).toggleClass('open')
})
$(document).on('click', '.list-images-block .list-images-main > ul li.folder', function (el) {
    $(this).toggleClass('open')
})

$(document).on('click', '.list-images-block .list-images-main .slider .swiper-slide', function (el) {
    el.stopPropagation();
    let content = `<img src="${$(this).find('img').attr('src')}" alt="">`,
        title = $(this).find('.info > span').text()
    if (!$('.modal#imgFull').length) {
        $('body').append(`
            <div class="modal fade" id="imgFull" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
                <div class="modal-dialog modal-fullscreen">
                    <div class="modal-content">
                        <div class="modal-header">
                            <div class="h1 _title36 modal-title" id="exampleModalLabel"><div class="info"><span>${title}</span><div class="copy"><i class="fa-regular fa-copy"></i></div></div></div>
                            <div class="button-prevnext btn-block">
                                <div class="btn prev">Prev</div>
                                <div class="btn next">Next</div>
                            </div>
                            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Закрыть"></button>
                        </div>
                        <div class="modal-body">${content}</div>
                    </div>
                </div>
            </div>
        `)
    } else {
        $('.modal#imgFull .modal-content .modal-header .modal-title .info > span').html(`${title}`)
        $('.modal#imgFull .modal-content .modal-body').html(`${content}`)
    }
    $('#imgFull').modal('show')
})

$(document).on('click', '.info .copy', function (el) {
    el.stopPropagation();
    let text = $(this).parents('.info').find('> span').text(),
        input = $('<textarea>').val(text).appendTo(this).select();
    document.execCommand('copy');
    input.remove();
    showToasts('Successfully copied!', 'text-bg-success')
});

function showToasts(text, color) {
    if (!$('.toast').length) {
        $('body').append(`
            <div class="toast ${color} align-items-center" role="alert" aria-live="assertive" aria-atomic="true">
                <div class="d-flex">
                    <div class="toast-body">${text}</div>
                    <button type="button" class="btn-close me-2 m-auto" data-bs-dismiss="toast" aria-label="Закрыть"></button>
                </div>
            </div>
        `)
    } else {
        $('.toast .toast-body').html(`${text}`)
    }
    $('.toast').toast('show')
}

let page_size_start = 50,
    page_size = page_size_start,
    page = 1,
    isDataExhausted = false;

function uploadSearchQuery(el) {
    if (isDataExhausted) {
        return;
    }
    let status = ''
    var params = window.location.search.substring(1).split("&");
    for (let i = 0; i < params.length; i++) {
        let param = params[i].split("=");
        if (param[0] === "status") {
            status = param[1]
            break;
        }
    }
    $(el).parents('.accordion-item').find('.accordion-body .table tbody').append('<tr class="tr-loader"><td class="loader-block" colspan="3"><span class="loader"></span></td></tr>')
    $.ajax({
        url: `/api/searchqueries/?project=${$(el).parents('.accordion-item').attr('data-id')}&status=${status}&page_size=` + page_size + '&page=' + page,
        method: 'GET',
        success: function(data) {
            if (data.results.length > 0) {
                $(el).parents('.accordion-item').find('.accordion-body .table tbody .tr-loader').remove()
                for (let i = 0; i < data.results.length; i++) {
                    $(el).parents('.accordion-item').find('.accordion-body .table tbody').append(`
                        <tr>
                            <td><input type="checkbox" value="${data.results[i].id}" class="checks group-${data.results[i].id}"></td>
                            <td>${data.results[i].query}</td>
                            <td class="status-td">${data.results[i].status_name}</td>
                        </tr>
                    `);
                }
                // Если получено записей меньше, чем page_size, это означает, что данных больше нет
                if (data.results.length < page_size) {
                    isDataExhausted = true;
                }
                page++;
            } else {
                // Если получено ноль записей, это также означает, что данных больше нет
                isDataExhausted = true;
                console.log('There is no more data to download.');
            }
        },
        error: function(error) {
            console.log(error);
        }
    });
}

$('.accordion-phrase .accordion-body .table-block').scroll(function() {
    let el = $(this).parents('.accordion-item').find('.accordion-header'),
        $this = $(this),
        scrollTop = $this.scrollTop(),
        scrollHeight = $this.prop('scrollHeight'),
        innerHeight = $this.innerHeight();
    if (scrollTop + innerHeight >= scrollHeight) {
        uploadSearchQuery(el);
    }
});

$(document).on('click', '.phrasesSection .accordion-phrase .accordion-item .accordion-header', function (el) {
    isDataExhausted = false
    page_size = page_size_start
    page = 1
    if (!$(this).hasClass('active-search')) {
        $(`.accordion-phrase .accordion-item .accordion-body .table tbody`).html('')
        uploadSearchQuery($(this))
        $('.phrasesSection .accordion-phrase .accordion-item .accordion-header').removeClass('active-search')
        $(this).addClass('active-search')
    } else {
        $(this).removeClass('active-search')
        $(`.accordion-phrase .accordion-item .accordion-body .table tbody`).html('')
    }
})

$('.list-domains-tree .func .item.open-all').on('click', function() {
    let tree = $(this).parents('.list-domains-tree')
    if ($(tree).find('.folder').length == $(tree).find('.folder.open').length) {
        $(tree).find('.folder').removeClass('open')
    } else {
        $(tree).find('.folder').addClass('open')
    }
})

const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]')
const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl))

$(document).ready(function() {
    $('form.proxy-item').keydown(function(event) {
        if(event.keyCode == 13) {
            event.preventDefault();
            return false;
        }
    });
});

$(document).on('click', '.button-prevnext .btn', function() {
    let info_text = $(this).parents('.modal-header').find('.modal-title .info > span'),
        img = $(this).parents('.modal-content').find('.modal-body img')

    if ($(this).hasClass('prev')) {
        galleryDomainSlider.slidePrev()
    }
    if ($(this).hasClass('next')) {
        galleryDomainSlider.slideNext()
    }

    let info_text_new = $('.galleryDomainSlider').find('.swiper-slide.swiper-slide-active .info > span'),
        img_new = $('.galleryDomainSlider').find('.swiper-slide.swiper-slide-active img')

    $(info_text).text($(info_text_new).text())
    $(img).attr('src', $(img_new).attr('src'))
})

function handleLeftArrowKeyPress(event) {
    if (event.which === 37) {
        galleryDomainSlider.slidePrev()
        console.log(1)
    }
}
function handleRightArrowKeyPress(event) {
    if (event.which === 39) {
        galleryDomainSlider.slideNext()
        console.log(2)
    }
}
$(document).keydown(function(el) {
    let info_text = $(el.target).find('.modal-header').find('.modal-title .info > span'),
        img = $(el.target).find('.modal-content').find('.modal-body img')
    if ($('.modal#imgFull').length && $('.modal#imgFull').hasClass('show')) {
        handleLeftArrowKeyPress(el);
        handleRightArrowKeyPress(el);
    }

    let info_text_new = $('.galleryDomainSlider').find('.swiper-slide.swiper-slide-active .info > span'),
        img_new = $('.galleryDomainSlider').find('.swiper-slide.swiper-slide-active img')

    $(info_text).text($(info_text_new).text())
    $(img).attr('src', $(img_new).attr('src'))
});