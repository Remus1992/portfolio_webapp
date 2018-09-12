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
        window.location.replace(`/webdev/`);
    } else {
        window.location.replace(`/webdev/?category=${this.id}`);
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
    $(placeToInsertImagePreview).html('');
    //let website_html = '<div class="website_info"><input type="text" id="website_title" name="website_title" class="resizedTextbox" placeholder="website Title"><input type="text" id="website_tag" name="website_tag" placeholder="website Tagline" class="resizedTextbox"><input list="categories" id="website_category" name="website_category" placeholder="website Category" class="resizedTextbox"><datalist id="categories">
    // {% for c in website_cats %}<option value = "{{ c.name }}">{% endfor %}</datalist><input type="text" id="youtube_link" name="website_youtube" placeholder="YouTubeLink" class="resizedTextbox"><input type="date" id="website_date" name="website_date" class="resizedTextbox"><br><br><br><p>website Poster</p><input type="file" id="website_poster" name="website_poster" class="resizedTextbox"><input type="text" id="alt_text" name="alt_text" placeholder="PosterAltText" class="resizedTextbox"><br><br><br><p>website Script</p><input type="file" id="website_script" name="website_script" class="resizedTextbox"></div><div class="website-details-row"><textarea id="web_details" name="web_details" cols="30" rows="10" placeholder="websiteDetails"></textarea></div><div class="website-still-input-row"><h2>website Stills</h2><input class="website_modal_btn" name="images" type="file" multiple id="gallery-website-still-add"></div><div id="website_gallery_images" class="website_gallery_images"></div>'
    //$(placeToInsertImagePreview).append(website_html);

    if (input.files) {
        let filesAmount = input.files.length;

        for (let i = 0; i < filesAmount; i++) {
            let reader = new FileReader();
            let num = i
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
                    .append($(`<span class="website-close" id="close_image_${num + 1}" onClick="removeElement('website_gallery_images', 'image_${num + 1}')">&times;</span><img class="website-preview-image" src="${event.target.result}" id="new_picture_${num + 1}" onload="calcPreviewImg(this)"><div><label for="image_name_${num + 1}">Photo Title</label></div><div><input type="text" value="${name}" name="image_name_${num + 1}"></div><div><label for="alt_text_${num + 1}">Alt Text</label></div><div><input type="text" id="alt_text_${num + 1}" name="alt_text_${num + 1}" value="${name}"></div>`));
                $(placeToInsertImagePreview).append(html);
            };

            reader.readAsDataURL(input.files[i]);
        }
    }
    input.value = ''
};

$('#gallery-website-still-add').on('change', function () {
    imagesPreview(this, 'div.website_gallery_images');
});

function removeElement(parentDiv, childDiv) {
    console.log("Child Div is " + childDiv);
    console.log("Parent Div is " + parentDiv);
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
let websiteUploadModal = document.getElementById('websiteModal');

// Get the button that opens the modal
let websiteBtn = document.getElementById("websiteModalBtn");

// Get the <span> element that closes the modal
let span = document.getElementsByClassName("website-close")[0];

// When the user clicks the button, open the modal
websiteBtn.onclick = function () {
    websiteUploadModal.style.display = "block";
};

// When the user clicks on <span> (x), close the modal
span.onclick = function () {
    websiteUploadModal.style.display = "none";
    let website_html = '<div class="website_info"><input type="text" id="website_title" name="website_title" class="resizedTextbox" placeholder="website Title"><input type="text" id="website_tag" name="website_tag" placeholder="website Tagline" class="resizedTextbox"><input list="categories" id="website_category" name="website_category" placeholder="website Category" class="resizedTextbox"><datalist id="categories">{% for c in website_cats %}<option value = "{{ c.name }}">{% endfor %}</datalist><input type="text" id="youtube_link" name="website_youtube" placeholder="YouTubeLink" class="resizedTextbox"><input type="date" id="website_date" name="website_date" class="resizedTextbox"><br><br><br><p>website Poster</p><input type="file" id="website_poster" name="website_poster" class="resizedTextbox"><input type="text" id="alt_text" name="alt_text" placeholder="PosterAltText" class="resizedTextbox"><br><br><br><p>website Script</p><input type="file" id="website_script" name="website_script" class="resizedTextbox"></div><div class="website-details-row"><textarea id="web_details" name="web_details" cols="30" rows="10" placeholder="websiteDetails"></textarea></div><div class="website-still-input-row"><h2>website Stills</h2><input class="website_modal_btn" name="images" type="file" multiple id="gallery-website-still-add"></div><div id="website_gallery_images" class="website_gallery_images"></div>'
    $("div.website_gallery").html(website_html);
    $('#gallery-website-still-add').on('change', function () {
        imagesPreview(this, 'div.website_gallery_images');
    });

};