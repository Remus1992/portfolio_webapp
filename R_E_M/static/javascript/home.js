$(document).ready(function () {
    let windowW = window.innerWidth;
    //console.log(windowW);

    if (window.matchMedia("(max-width: 767px)").matches) {
        //console.log('small');
        $("#loader").css("display", "none")
    } else {
        $(".small_REM_container").css("display", "none");
        $(".rw-wrapper").css("display", "none");
        $("#preFooter").css("display", "none");
        $("#footer").css("display", "none");

        let offsets = {};
        gather_offset('#R1', {'opacity': '0.8', 'top': '250px'});
        gather_offset('#R2', {'opacity': '0.8', 'top': '100px', 'left': '300px'});
        gather_offset('#R3', {'opacity': '0.8', 'top': '-100px', 'left': '300px'});
        gather_offset('#R4', {'opacity': '0.8', 'top': '250px', 'left': '300px'});
        gather_offset('#E1', {'opacity': '0.8', 'top': '250px'});
        gather_offset('#E2', {'opacity': '0.8', 'left': '750px'});
        gather_offset('#E3', {'opacity': '0.8', 'left': '750px'});
        gather_offset('#E4', {'opacity': '0.8', 'left': '750px'});
        gather_offset('#M1', {'opacity': '0.8', 'top': '250px'});
        gather_offset('#M2', {'opacity': '0.8', 'top': '-250px', 'left': '750px'});
        gather_offset('#M3', {'opacity': '0.8', 'top': '-250px', 'left': '1350px'});
        gather_offset('#M4', {'opacity': '0.8', 'top': '250px'});

        $( document ).ready(function() {
            setTimeout(function () {
                $('#loader').hide('slow');
                ani("#R1", offsets["#R1"], 2000);
                ani("#R2", offsets["#R2"], 2000);
                ani("#R3", offsets["#R3"], 2000);
                ani("#R4", offsets["#R4"], 2000);
                ani("#E1", offsets["#E1"], 2000);
                ani("#E2", offsets["#E2"], 2000);
                ani("#E3", offsets["#E3"], 2000);
                ani("#E4", offsets["#E4"], 2000);
                ani("#M1", offsets["#M1"], 2000);
                ani("#M2", offsets["#M2"], 2000);
                ani("#M3", offsets["#M3"], 2000);
                ani("#M4", offsets["#M4"], 2000);
            }, 1000);
        });

        function gather_offset(id, css) {
            offsets[id] = $(id).offset();
            $(id).css(css)
        }

        function ani(id, offset, time) {
            let el = $(`${id}`);
            $(el).animate(offset, time);
        }
    }

});

let slideIndex = 1;
showSlides(slideIndex);

function plusSlides(n) {
    showSlides(slideIndex += n);
}

setInterval(function () {
    plusSlides(1)
}, 6000);


function currentSlide(n) {
    showSlides(slideIndex = n);
}

function showSlides(n) {
    let i;
    let slides = document.getElementsByClassName("mySlides");
    if (n > slides.length) {
        slideIndex = 1
    }
    if (n < 1) {
        slideIndex = slides.length
    }
    for (i = 0; i < slides.length; i++) {
        slides[i].style.display = "none";
    }
    slides[slideIndex - 1].style.display = "block";
}