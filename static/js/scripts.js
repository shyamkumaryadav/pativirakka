/*!
    * Start Bootstrap - Resume v6.0.1 (https://startbootstrap.com/template-overviews/resume)
    * Copyright 2013-2020 Start Bootstrap
    * Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-resume/blob/master/LICENSE)
    */
(function ($) {
    "use strict"; // Start of use strict

    // Smooth scrolling using jQuery easing
    $('a.js-scroll-trigger[href*="#"]:not([href="#"])').click(function () {
        if (
            location.pathname.replace(/^\//, "") ==
            this.pathname.replace(/^\//, "") &&
            location.hostname == this.hostname
        ) {
            var target = $(this.hash);
            target = target.length
                ? target
                : $("[name=" + this.hash.slice(1) + "]");
            if (target.length) {
                $("html, body").animate(
                    {
                        scrollTop: target.offset().top,
                    },
                    1000,
                    "easeInOutExpo"
                );
                return false;
            }
        }
    });


    // Form Login
    const form = $("#loginForm");
    const btn = $("#loginFormBtn");
    var time = 0;
    btn.on('click', (event) => {
        event.preventDefault();
        time += 1;
        $.ajax({
            type: "POST",
            url: "login/",
            context: document.body,
            data: form.serialize(),
            success: (data) => {
                if (data.error) {
                    toastr.error(data.error);
                    $("#password_login").val("");
                }
                else if (data === 'ok') {
                    document.location.reload();
                }
            },
            statusCode: {
                404: () => {
                    toastr.error('error 404');
                },
                500: () => {
                    toastr.error('error 500');
                }
            }

        });
    });

    // Closes responsive menu when a scroll trigger link is clicked
    $(".js-scroll-trigger").click(function () {
        $(".navbar-collapse").collapse("hide");
    });


    // Activate scrollspy to add active class to navbar items on scroll
    $("body").scrollspy({
        target: "#sideNav",
    });
})(jQuery); // End of use strict
