function calcImg(img) {
    let h = $(img).height();
    let w = $(img).width();

    //console.log(h);
    //console.log(w);

    if ($(img).parent('.movie-image-wrap').length === 0) {
        // wrap the image in a "cropping" div
        $(img).wrap('<div class="movie-image-wrap"></div>');
    }

    if (w / h < 300 / 430) {
        $(img).addClass('narrow');
    } else if (w / h > 300 / 430) {
        $(img).addClass('wide');
    } else {
        $(img).addClass('perfect');
    }
}

function calcPreviewImg(img) {
    console.log(img);
    let h = $(img).height();
    let w = $(img).width();

    console.log(h);
    console.log(w);

    if ($(img).parent('.movie_gallery_images').length === 0) {
        // wrap the image in a "cropping" div
        $(img).wrap('<div class="movie-preview-image-wrap"></div>');
    }

    if (h > w) {
        // pic is portrait
        $(img).addClass('portrait');
        let m = -(((h / w) * 100) - 100) / 2; //math the negative margin
        $(img).css('margin-top', m + '%');
    } else if (w > h) {
        // pic is landscape
        $(img).addClass('landscape');
        let m = -(((w / h) * 100) - 100) / 2;  //math the negative margin
        $(img).css('margin-left', m + '%');
    } else {
        // pic is square
        $(img).addClass('square');
    }
}


function movieCardCheckFocus(card) {
    if (window.matchMedia("(max-width: 766px)").matches) {
        $('.movie-card').each(function (i, el) {
            $(el).children('.color-overlay').css({"background": "none"});
            $(el).children('.title-content').css({"opacity": "0"});
            $(el).children('.card-info').css({"opacity": "0"});
            $(el).children('.movie_read_more').css({"opacity": "0"});
            $(el).children('.movie_button').css({"opacity": "0", "margin": "40px"});
        });
        $(card).children('.color-overlay').css({"background": "rgba(84, 104, 110, 0.9)"});
        $(card).children('.title-content').css({"opacity": "1"});
        $(card).children('.card-info').css({"opacity": "1"});
        $(card).children('.movie_read_more').css({"opacity": "1"});
        $(card).children('.movie_button').css({"background-color": "white",
                                            "opacity": "0.7",
                                            "border": "white solid 2px",
                                            "color": "black",
                                            "padding": "3px 5px",
                                            "border-radius": "5px",
                                            "text-align": "center",
                                            "text-decoration": "none",
                                            "font-size": "16px",
                                            "margin": "40px",
                                            "cursor": "pointer",
                                            "font-weight": "bold",
                                            "display": "inline-block"});
    } else if (window.matchMedia("(max-width: 1024px)").matches) {
        $('.movie-card').each(function (i, el) {
            $(el).children('.color-overlay').css({"background": "none"});
            $(el).children('.title-content').css({"opacity": "0"});
            $(el).children('.card-info').css({"opacity": "0"});
            $(el).children('.movie_read_more').css({"opacity": "0"});
            $(el).children('.movie_button').css({"opacity": "0", "margin": "40px"});
        });
        $(card).children('.color-overlay').css({"background": "rgba(84, 104, 110, 0.9)"});
        $(card).children('.title-content').css({"opacity": "1"});
        $(card).children('.card-info').css({"opacity": "1"});
        $(card).children('.movie_read_more').css({"opacity": "1"});
        $(card).children('.movie_button').css({"background-color": "white",
                                            "opacity": "0.7",
                                            "border": "white solid 2px",
                                            "color": "black",
                                            "padding": "3px 5px",
                                            "border-radius": "5px",
                                            "text-align": "center",
                                            "text-decoration": "none",
                                            "font-size": "16px",
                                            "margin": "40px",
                                            "cursor": "pointer",
                                            "font-weight": "bold",
                                            "display": "inline-block"});
    } else {
        console.log('Large')
    }
}
