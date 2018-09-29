let infinite = new Waypoint.Infinite({
    element: $('.infinite-container')[0],
    onBeforePageLoad: function () {
        $('.loading').show();
    },
    onAfterPageLoad: function ($items) {
        $('.loading').hide();
    }
});

$('.checkbox').click(function () {
    let cat = this.id;

    // removing shade from other elements
    $('.checkbox').each(function (i, el) {
        $(el).removeClass('checkFocus');
    });

    $(this).addClass('checkFocus');
});

$('.checkbox').click(function () {
    if (this.id === "All") {
        window.location.replace(`/photography/`);
    } else {
        window.location.replace(`/photography/?category=${this.id}`);
    }

});

$('.checkbox').each(function (i, el) {
    //console.log(el.id);
    //$(el).removeClass('checkFocus');
    if (el.id === document.location.toString().split("?category=")[1]){
        //console.log("Success!");
        $(this).addClass('checkFocus');
    }
});


// IMAGE UPLOADER PLUS MODAL
let imagesPreview = function (input, placeToInsertImagePreview) {
    // $(placeToInsertImagePreview).html('');
    // let album_html = '<div class="album_info"><input type="text" id="album_title" name="album_title" class="resizedTextbox" placeholder="Album Title"><input type="text" id="album_alt_text" name="album_alt_text" placeholder="Album Alt Text" class="resizedTextbox"><input list="categories" id="album_category" name="album_category" placeholder="Album Category" class="resizedTextbox"><datalist id="categories">{% for c in album_cats %}<option value="{{ c.name }}">{% endfor %}</datalist><textarea rows="4" cols="50" id="album_details" name="album_details" placeholder="Album Details" class="resizedTextbox album_details"></textarea></div><div class="album_gallery_images" id="album_gallery_images"></div>';
    // $(placeToInsertImagePreview).append(album_html);

    if (input.files) {
        let filesAmount = input.files.length;

        for (let i = 0; i < filesAmount; i++) {
            let reader = new FileReader();
            let num = i;
            let name = input.files[i].name;
            reader.onload = function (event) {
                let html = $(`<div class="img_holder" id="image_${num + 1}"></div>`, {
                    'id': `image_div_${num + 1}`
                })
                    .append($(`<input>`).attr({
                        'type': 'hidden',
                        'value': event.target.result,
                        'name': `image_${num + 1}`
                    }))
                    .append($(`<span class="album-close" id="close_image_${num + 1}" onClick="removeElement('album_gallery_images', 'image_${num + 1}')">&times;</span><img class="album-preview-image" src="${event.target.result}" id="new_picture_${num + 1}" onload="calcPreviewImg(this)"><div><label for="image_name_${num + 1}">Photo Title</label></div><div><input type="text" value="${name}" name="image_name_${num + 1}"></div><div><label for="alt_text_${num + 1}">Alt Text</label></div><div><input type="text" id="alt_text_${num + 1}" name="alt_text_${num + 1}" value="${name}"></div><div><label for="creation_date_${num + 1}">Date Taken</label></div><div><input type="date" id="creation_date_${num + 1}" name="creation_date_${num + 1}"></div><div><label for="image_details_${num + 1}">Image Details</label></div><div><input type="textarea" id="image_details_${num + 1}" name="image_details_${num + 1}"></div>`));
                $('div.album_gallery_images').append(html);
            };

            reader.readAsDataURL(input.files[i]);
        }
    }
    input.value = ''
};
$('#gallery-photo-add').on('change', function () {
    imagesPreview(this, 'div.album_gallery');
});

function removeElement(parentDiv, childDiv) {
    //console.log("Child Div is " + childDiv);
    //console.log("Parent Div is " +parentDiv);
    if (childDiv == parentDiv) {
        alert("The parent div cannot be removed.")
    } else if (document.getElementById(childDiv)) {
        let child = document.getElementById(childDiv);
        let parent = document.getElementById(parentDiv);
        //console.log("Child Div is " + child);
        //console.log("Parent Div is " + parent);
        parent.removeChild(child);
    }
    else {
        alert("Child div has already been removed or does not exist.");
        return false;
    }
}


// Get the modal
let photoAlbumModal = document.getElementById('photoModal');

// Get the button that opens the modal
let photoAlbumBtn = document.getElementById("photoModalBtn");

// Get the <span> element that closes the modal
let span = document.getElementsByClassName("album-close")[0];

// When the user clicks the button, open the modal
photoAlbumBtn.onclick = function () {
    photoAlbumModal.style.display = "block";
};

// When the user clicks on <span> (x), close the modal
span.onclick = function () {
    photoAlbumModal.style.display = "none";
    let ac = $("div.album_gallery_images");
    $(ac).html('');
};