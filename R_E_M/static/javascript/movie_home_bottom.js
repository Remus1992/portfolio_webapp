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
    window.location.replace(`/filmmaking/?category=${this.id}`);
});


// IMAGE UPLOADER PLUS MODAL
let imagesPreview = function (input, placeToInsertImagePreview) {
    $(placeToInsertImagePreview).html('');
    //let movie_html = '<div class="movie_info"><input type="text" id="movie_title" name="movie_title" class="resizedTextbox" placeholder="Movie Title"><input type="text" id="movie_tag" name="movie_tag" placeholder="Movie Tagline" class="resizedTextbox"><input list="categories" id="movie_category" name="movie_category" placeholder="Movie Category" class="resizedTextbox"><datalist id="categories">{% for c in movie_cats %}<option value="{{ c.name }}">{% endfor %}</datalist><input type="text" id="youtube_link" name="movie_youtube" placeholder="YouTube Link" class="resizedTextbox"><input type="date" id="movie_date" name="movie_date" class="resizedTextbox"><br><br><br><p>Movie Poster</p><input type="file" id="movie_poster" name="movie_poster" class="resizedTextbox"><input type="text" id="alt_text" name="alt_text" placeholder="Poster Alt Text" class="resizedTextbox"><br><br><br><p>Movie Script</p><input type="file" id="movie_script" name="movie_script" class="resizedTextbox"></div><div class="movie-details-row"><textarea id="movie_details" name="movie_details" cols="30" rows="10" placeholder="Movie Details"></textarea></div><div class="movie-still-input-row"><h2>Movie Stills</h2><input class="movie_modal_btn" name="images" type="file" multiple id="gallery-movie-still-add"></div><div id="movie_gallery_images" class="movie_gallery_images"></div>'
    //$(placeToInsertImagePreview).append(movie_html);

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
                    .append($(`<span class="movie-close" id="close_image_${num + 1}" onClick="removeElement('movie_gallery_images', 'image_${num + 1}')">&times;</span><img class="movie-preview-image" src="${event.target.result}" id="new_picture_${num + 1}" onload="calcPreviewImg(this)"><div><label for="image_name_${num + 1}">Photo Title</label></div><div><input type="text" value="${name}" name="image_name_${num + 1}"></div><div><label for="alt_text_${num + 1}">Alt Text</label></div><div><input type="text" id="alt_text_${num + 1}" name="alt_text_${num + 1}" value="${name}"></div><div><label for="creation_date_${num + 1}">Date Taken</label></div><div><input type="date" id="creation_date_${num + 1}" name="creation_date_${num + 1}"></div><div><label for="image_details_${num + 1}">Image Details</label></div><div><input type="textarea" id="image_details_${num + 1}" name="image_details_${num + 1}"></div>`));
                $(placeToInsertImagePreview).append(html);
            };

            reader.readAsDataURL(input.files[i]);
        }
    }
    input.value = ''
};

$('#gallery-movie-still-add').on('change', function () {
    imagesPreview(this, 'div.movie_gallery_images');
});

function removeElement(parentDiv, childDiv) {
    console.log("Child Div is " + childDiv);
    console.log("Parent Div is " +parentDiv);
    if (childDiv == parentDiv) {
        alert("The parent div cannot be removed.")
    } else if (document.getElementById(childDiv)) {
        let child = document.getElementById(childDiv);
        let parent = document.getElementById(parentDiv);
        console.log("Child Div is " + child);
        console.log("Parent Div is " + parent);
        parent.removeChild(child);
    }
    else {
        alert("Child div has already been removed or does not exist.");
        return false;
    }
}

// Get the modal
let movieUploadModal = document.getElementById('movieModal');

// Get the button that opens the modal
let movieBtn = document.getElementById("movieModalBtn");

// Get the <span> element that closes the modal
let span = document.getElementsByClassName("movie-close")[0];

// When the user clicks the button, open the modal
movieBtn.onclick = function() {
    movieUploadModal.style.display = "block";
};

// When the user clicks on <span> (x), close the modal
span.onclick = function() {
    movieUploadModal.style.display = "none";
    let movie_html = '<div class="movie_info"><input type="text" id="movie_title" name="movie_title" class="resizedTextbox" placeholder="Movie Title"><input type="text" id="movie_tag" name="movie_tag" placeholder="Movie Tagline" class="resizedTextbox"><input list="categories" id="movie_category" name="movie_category" placeholder="Movie Category" class="resizedTextbox"><datalist id="categories">{% for c in movie_cats %}<option value="{{ c.name }}">{% endfor %}</datalist><input type="text" id="youtube_link" name="movie_youtube" placeholder="YouTube Link" class="resizedTextbox"><input type="date" id="movie_date" name="movie_date" class="resizedTextbox"><br><br><br><p>Movie Poster</p><input type="file" id="movie_poster" name="movie_poster" class="resizedTextbox"><input type="text" id="alt_text" name="alt_text" placeholder="Poster Alt Text" class="resizedTextbox"><br><br><br><p>Movie Script</p><input type="file" id="movie_script" name="movie_script" class="resizedTextbox"></div><div class="movie-details-row"><textarea id="movie_details" name="movie_details" cols="30" rows="10" placeholder="Movie Details"></textarea></div><div class="movie-still-input-row"><h2>Movie Stills</h2><input class="movie_modal_btn" name="images" type="file" multiple id="gallery-movie-still-add"></div><div id="movie_gallery_images" class="movie_gallery_images"></div>'
    $("div.movie_gallery").html(movie_html);
    $('#gallery-movie-still-add').on('change', function () {
        imagesPreview(this, 'div.movie_gallery_images');
    });

};