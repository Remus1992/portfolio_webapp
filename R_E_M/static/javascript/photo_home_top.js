function calcImg(img) {
    let h = $(img).height();
    let w = $(img).width();

    //console.log(h);
    //console.log(w);

    if ($(img).parent('.album-image-wrap').length === 0) {
        // wrap the image in a "cropping" div
        $(img).wrap('<div class="album-image-wrap"></div>');
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

function calcPreviewImg(img) {
    console.log(img);
    let h = $(img).height();
    let w = $(img).width();

    console.log(h);
    console.log(w);

    if ($(img).parent('.album_gallery_images').length === 0) {
        // wrap the image in a "cropping" div
        $(img).wrap('<div class="album-preview-image-wrap"></div>');
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