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

// console.log(document.location.toString().split("?category=")[1]);

let blog_url_slug = document.location.toString().split("?category=")[1];

if (blog_url_slug === "undefined") {
    console.log("Element is Undefined")
} else {
    console.log("Element is " + blog_url_slug)
}

$('.checkbox').each(function (i, el) {
    console.log(el.id);
    $(el).removeClass('checkFocus');
    if (el.id === document.location.toString().split("?category=")[1]){
        console.log("Success!");
        $(this).addClass('checkFocus');
    }
});


