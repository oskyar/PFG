// Funciones de Óscar Zafra para la aplicación de Test.

$(document).ready(function () {

    $('select').material_select();

    validate_form();
    //$(".button-collapse").sideNav();
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            function getCookie(name) {
                var cookieValue = null;
                if (document.cookie && document.cookie != '') {
                    var cookies = document.cookie.split(';');
                    for (var i = 0; i < cookies.length; i++) {
                        var cookie = jQuery.trim(cookies[i]);
                        // Does this cookie string begin with the name we want?
                        if (cookie.substring(0, name.length + 1) == (name + '=')) {
                            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                            break;
                        }
                    }
                }
                return cookieValue;
            }

            if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
                // Only send the token to relative URLs i.e. locally.
                xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
            }
        }
    });

    $("#id_username").on('keyup', function (ev) {
        if ($(this).val().length > 3) {
            $.post('/user/register/', {username: $(this).val()})
                .done(function (data) {
                    console.log(data);
                    if (data['username'] == undefined) {
                        $('#id_username').addClass('valid').removeClass('invalid');
                    } else {
                        $('#id_username').addClass('invalid').removeClass('valid')
                            .next().attr('data-error', "Error: " + data['username'][0]);
                    }
                });
        }
    });

    $("#id_email").on('keyup', function (ev) {
        if ($(this).val().length > 3) {
            $.post('/user/register/', {email: $(this).val(), email2: $('#id_email2').val()})
                .done(function (data) {
                    console.log(data);
                    if (data['email'] == undefined) {
                        $('#id_email').addClass('valid').removeClass('invalid');
                    } else {
                        $('#id_email').addClass('invalid').removeClass('valid')
                            .next().attr('data-error', "Error: " + data['email'][0]);
                    }
                });
        }
    });

    $("#id_email2").on('keyup', function (ev) {
        if ($(this).val().length > 3) {
            $.post('/user/register/', {email: $('#id_email').val(), email2: $(this).val()})
                .done(function (data) {
                    console.log(data);
                    if (data['email2'] == undefined) {
                        $('#id_email2').addClass('valid').removeClass('invalid');
                    } else {
                        $('#id_email2').addClass('invalid').removeClass('valid')
                            .next().attr('data-error', "Error: " + data['email2'][0]);
                    }
                });
        }
    });


    $('.button-collapse').sideNav({
            menuWidth: 300, // Default is 240
            edge: 'left', // Choose the horizontal origin
            closeOnClick: false // Closes side-nav on <a> clicks, useful for Angular/Meteor
        }
    );

    $('ul.tabs').tabs();

    $('.collapsible').collapsible({
        accordion: true // A setting that changes the collapsible behavior to expandable instead of the default accordion style
    });

    $(".dial").knob({
        min: 0,
        max: 100,
        angleOffset: 0, //30 me gusta
        angleArc: 360,     //300 me gusta
        readOnly: true,
        width: 195,
        thickness: 0.1,
        displayInput: false,
        fgColor: '#a7ffeb',
        bgColor: '#4db6ac',
        lineCap: 'round'
    }).hover(function () {

        $('.level').fadeToggle(200);
    });

    $('i.close').on('click', function () {
        $(this).parents('.card-panel').fadeOut();
    });

    $('.table-of-contents').pushpin({top: $('.container').offset().top});
    $('.scrollspy').scrollSpy();


    $('.modal-trigger').leanModal();

    if ($('.side-nav').hasClass('hide')) {
        $('header, main, footer').css('padding-left', 0);
    }

    /********** Eventos Asignatura ************/

    $('#id_name').on('keyup', function () {
        $('[data-name="subject_name"]').text($(this).val());
    });
    $('#id_category').on('keyup', function () {
        $('[data-name="subject_name"]').text($(this).val());
    });
    $('#id_description').on('keyup', function () {
        if ($(this).val().length > 0) {

            $('[data-name="description"]').text($(this).val()).prev().text("done").removeClass("red-text").addClass('green-text');
        } else {
            $('[data-name="description"]').text("Descripción de la asignatura").prev().text("clear").removeClass("green-text").addClass('red-text');
        }
    });

    $("#id_capacity").on('keyup', function () {
        $('[data-name="capacity"]').text($(this).val());
    });

    $("#id_num_topics").on('keyup', function () {
        $('[data-name="num_topics"]').text($(this).val());
    });

    $('#id_test_opt').on('change', function () {
        if ($(this).prop('checked')) {
            $("[data-name='text_opt'] i").text("done").removeClass("red-text").addClass('green-text');
        } else {
            $('[data-name="text_opt"] i').text("clear").removeClass("green-text").addClass('red-text');

        }
    });

    $('[data-name="image_subject"]').draggable({
        start: function () {
            $(this).parents('.card, .card-image').css('overflow', 'visible');
        },
        stop: function () {
            $(this).parents('.card, .card-image').css('overflow', 'hidden');
        }
    });

    var n = 0;
    $('[data-name="image_subject"]').dblclick(function () {
        if (n == 0) {
            $(this).css('width', '');
            $(this).css('height', '');
        } else if (n == 1) {
            $(this).css('width', 'auto');
            $(this).css('height', '');
        } else if (n == 2) {
            $(this).css('width', '');
            $(this).css('height', 'auto');
        } else if (n == 4) {
            $(this).css('width', 'auto');
            $(this).css('height', 'auto');
        }
        n = ++n % 4;

    });

    $('#subject_form  input, textarea').val("");

    //Cambiamos el check dependiendo del tipo de pregunta
    $('#id_type').change(function () {
        if (parseInt($(this).val()) == 0) { // Pregunta de respuesta única
            //$('.replies-container').show();
            $('.valid-reply').attr('type', 'radio').removeAttr('checked').each(function (k, v) {

                var num = $(v).attr('id').split('-')[1];
                $('#id_answer-' + num + '-adjustment').val(0);
            });

        } else if (parseInt($(this).val()) == 2) {
            $('.replies-container').hide().first().show();
            //$('.replies-container input[name=valid-reply]').first().show();
        } else if (parseInt($(this).val()) == 1) {
            //$('.replies-container').show();
            $('.valid-reply').attr('type', 'checkbox').each(function (k, v) {

                var num = $(v).attr('id').split('-')[1];
                //$('#id_answer-' + num + '-adjustment').show();
            });
        }
    });

    $('.valid-reply').click(function (ev) {
        if (parseInt($('#id_type').val()) == 0) {
            $('.valid-reply').each(function (k, v) {
                var num = $(v).attr('id').split('-')[1];
                if (ev != null) {
                    if ($(v).attr('id') != ev.target.id) {
                        $(v).attr('checked', false);
                        $('#id_answer-' + num + '-adjustment').val(0);
                    } else {
                        $('#id_answer-' + num + '-adjustment').val(100);
                    }
                }
            });

        }
    });

    //Validate question
    $('#submit_question').click(function (ev) {
        var isReplySelected = false;
        $('.valid-reply').each(function (k, v) {
            if ($(v).context.checked == true) {
                isReplySelected = true;
            }
        });
        if (!isReplySelected) {
            ev.preventDefault();
            alert("Debe seleccionar una respuesta correcta");
        }
    });


    $(".delete_question").click(function () {
        if (confirm("¿Quiere eliminar la pregunta? No habrá vuelta atrás")) {
            var id = $(this).attr('id');
            $.ajax({
                type: "POST",
                url: $(this).data('url'),
                data: {id: id},
                success: function (response) {
                    $('#question_' + id).remove();
                    Materialize.toast('Pregunta eliminada correctamente', 3000)
                },
                error: function (res) {
                    alert("ERROR: No se puede borrar la pregunta");
                }
            });
        }
        return false;
    });

    //Asignaturas
    $('[data-target="subject"]').click(function () {
        window.location = $(this).data('url');
    });


});

function initialize_question_view() {
    $('#id_type').trigger('change');
    //$('.valid-reply').trigger('click');
}

function validate_form() {
    $('input').each(function (k, v) {
        if ($(v).next().attr('data-error')) {
            $(v).addClass('invalid').attr('placeholder', "Es obligatorio");
        } else {
            if ($(v).val().length > 0)
                $(v).addClass('valid');
        }
    });
}