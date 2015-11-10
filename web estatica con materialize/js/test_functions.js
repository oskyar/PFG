// Funciones de Óscar Zafra para la aplicación de Test.

$(document).ready(function () {
    //$(".button-collapse").sideNav();


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

    $('.table-of-contents').pushpin({ top: $('.container').offset().top });
     $('.scrollspy').scrollSpy();
    //$('.button-collapse').sideNav('show');

    //Esconder filtros y mostrarlos (En asignaturas)
    /*$('#button_filter').on('click', function () {
     $(this).toggleClass('mdl-cell--3-col mdl-cell--1-col');
     $('#filters_container').toggleClass('mdl-cell--3-col mdl-cell--1-col')
     $('#subject_container').toggleClass('mdl-cell--9-col mdl-cell--11-col');
     $('#form_container').toggleClass('hidden');
     $('#filters_icons_container').toggleClass('hidden');
     $(this).find('i').toggleClass('fa-caret-left fa-caret-right', 500);

     });*/
});