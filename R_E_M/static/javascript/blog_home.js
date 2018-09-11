// Gives Markdown Editor to the Blog Content Div
$('#blog_content').trumbowyg();

// Allows for continual coloring of button after click event
$('.checkbox').click(function () {
    let cat = this.id;

    // removing shade from other elements
    $('.checkbox').each(function (i, el) {
        $(el).removeClass('checkFocus');
    });

    $(this).addClass('checkFocus');
});


function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        let cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            let cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

let csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$.ajaxSetup({
    beforeSend: function (xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

$('.checkbox').click(function () {
    window.location.replace(`/blog/?category=${this.id}`);
});

// Get the modal
let blogUploadModal = document.getElementById('blogModal');

// Get the button that opens the modal
let blogBtn = document.getElementById("blogModalBtn");

// Get the <span> element that closes the modal
let span = document.getElementsByClassName("blog-close")[0];

// When the user clicks the button, open the modal
blogBtn.onclick = function () {
    blogUploadModal.style.display = "block";
};

// When the user clicks on <span> (x), close the modal
span.onclick = function () {
    blogUploadModal.style.display = "none";
    let blog_html = '<div class="blog_info"><input type="text" id="blog_title" name="blog_title" class="resizedTextbox" placeholder="Blog Title"><input list="categories" id="category" name="category" placeholder="Blog Category" class="resizedTextbox"><datalist id="categories">{% for c in cat %}<option value="{{ c.name }}">{% endfor %}</datalist><input type="text" id="youtube_link" name="youtube_link" placeholder="YouTube Link" class="resizedTextbox"><br><br><br><p>Blog Image</p><input type="file" id="blog_image" name="blog_image" class="resizedTextbox"><input type="text" id="alt_text" name="alt_text" placeholder="Alt Text" class="resizedTextbox"></div><div class="blog-details-row"><textarea id="blog_content" name="blog_content" cols="30" rows="10" placeholder="Blog Content"></textarea></div>'
    $("div.blog_gallery").html(blog_html);
    $('#blog_content').trumbowyg();
};