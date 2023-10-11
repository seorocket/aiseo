$(document).ready(function() {
    maskField()
    checkSize()
})
$(window).resize(function() {
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
                            let t=0
                            for (let j=0; j<$(field[i]).parents('.form-group-auto-row').find('.list.list-directions ul li').length; j++) {
                                if (t=0) {
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
                            let t=0
                            for (let j=0; j<$(field[i]).parents('.form-group-auto-row').find('.list.list-directions ul li').length; j++) {
                                if (t=0) {
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
                    let t=0
                    for (let j=0; j<$(field[i]).parents('.form-group-auto-row').find('.list.list-directions ul li').length; j++) {
                        if (t=0) {
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
        clearFields()
    }
}

function clearFields() {
    $('input:not([type=checkbox])').val('')
    $('textarea').val('')
    $('.__select__title').removeClass('error')
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
            if (value) {
                obj[name] = value;
            }
        }
    });

    obj['type'] = type
    let csrftoken = $("input[name='csrfmiddlewaretoken']").val();
    $.ajax({
        url: '/ajax/',
        method: "POST",
        data: JSON.stringify(obj),
        headers: {
            'X-CSRFToken': csrftoken,
        },
        success: function (response){
            console.log(response)
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
    $(".mask-phone").click(function(){
      $(this).setCursorPosition(3);
    }).mask("+7(999) 999-9999");
    // $(".mask-phone").mask("+7 (999) 999-99-99");
    $('.mask-date').mask('99.99.9999');
}
$.fn.setCursorPosition = function(pos) {
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
            <div class="h1 _title36 modal-title" id="exampleModalLabel">Добавить группу</div>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Закрыть"></button>
        `)
        bodyText.html(`
            <form class="application-block">
                <input class="group_add" placeholder="Новая группа" name="name">
                <div class="btn checkField" data-request="new_group">Создать новую группу</div>
            </form>
        `)
    }
    maskField()
    $('#infoModal').modal('show')
}

$('.left-col .list ul li > a.openSub').on('click', function() {
    $(this).parent('li').toggleClass('open')
})

$('.main-container .left-col .func .item.open-all').on('click', function() {
    if ($('.left-col .list ul li > a.openSub').parent('li').length == $('.left-col .list ul li > a.openSub').parent('li.open').length) {
        $('.left-col .list ul li > a.openSub').parent('li').removeClass('open')
    } else {
        $('.left-col .list ul li > a.openSub').parent('li').addClass('open')
    }
})

// $('.save_group').click(function(){
//     let name_group = $('.group_add').val();
//     if (name_group !== '') {
//         $.ajax({
//             url: '/ajax/',
//             method: "POST",
//             data: {
//                 csrfmiddlewaretoken: getCookie('csrftoken'),
//                 type: 'save_group',
//                 name: name_group,
//             },
//             success: function (data, textStatus){
//                 if(data.error){
//                     $('.message').html('<span style="color:red;">' + data.error + '</span>');
//                 }else{
//                     $('.group_select').html(data);
//                     $('.group_select option:last').prop('selected', true);
//                     $('.message').html('<span style="color:green;">Группа успешно добавлена</span>');
//                     $('.add-phrase .phrase .field').removeClass('d-none')
//                     $('.group_add').val('')
//                     setTimeout(function() {
//                         $('.message').html('')
//                     }, 1500)
//                 }
//             }
//         });
//     } else {
//         $('.message').html('<span style="color:red;">Пустое название группы</span>');
//     }
// });
//  $('.save_phrase').click(function(){
//     let phrase = $('.phrase_text').val();
//     let sel = $('.group_select').val();
//     $.ajax({
//         url: '/ajax/',
//         method: "POST",
//         data: {
//             csrfmiddlewaretoken: getCookie('csrftoken'),
//             type: 'save_search_key',
//             group: sel,
//             phrases: phrase
//         },
//         success: function (data, textStatus){
//             if(data.status == 'ok' || data.ok){
//                 $('.message_phrase').html('<span style="color:green;">Фразы успешно добавлены</span>');
//                 $('.phrase_text').val('');
//                 $('.group_select').val('');
//                 window.location.href = '/phrase/'
//             }else{
//                 $('.message_phrase').html('<span style="color:red;">' + data.error + '</span>');
//             }
//         }
//     });
// });
//  $('.group_select').on('change', function() {
//      $('.add-phrase .phrase .field').removeClass('d-none')
//  })