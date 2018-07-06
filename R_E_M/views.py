from django.shortcuts import render, HttpResponseRedirect, get_object_or_404, reverse, redirect
from R_E_M.models import User, Album, Photo, Website, Blog, Category, Movie
import base64
from django.core.files.base import ContentFile
import re
from PIL import Image


def home(request):
    return render(request, 'misc/home.html')


def about(request):
    return render(request, 'misc/about.html')


def contact(request):
    return render(request, 'misc/contact.html')


def photography_home(request):
    complete_album_list = Album.objects.all()
    return render(request, 'photos/photo_home.html', {'albums': complete_album_list})


def photo_album_view(request, slug):
    album = Album.objects.get(slug=slug)
    return render(request, 'photos/photo_album_view.html', {"album": album})


def photo_single_view(request, slug):
    photo = get_object_or_404(Album, slug=slug)
    return render(request, 'photos/single_photo_view.html', {"photo": photo})


def photo_upload(request):
    if request.method == "POST":
        # print(request.POST)
        print(request.FILES)
        album = Album()
        album.owner = request.user
        album.title = request.POST.get('album_title')
        album.album_details = request.POST.get('album_details')
        album.alt_text = request.POST.get('album_alt_text')
        album.save()

        for k, v in request.POST.items():
            if re.match('^image_\d+$', k):
                num = int(re.search(r'\d+', k).group())
                format, imgstr = v.split(';base64,')
                ext = format.split('/')[-1]
                data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

                photo = Photo()
                photo.image = data
                photo.album = album
                photo.owner = request.user
                photo.title = request.POST.get('image_name_{}'.format(num))
                photo.alt_text = request.POST.get('alt_text_{}'.format(num))
                photo.date_taken = request.POST.get('creation_date_{}'.format(num))
                photo.image_details = request.POST.get('image_details_{}'.format(num))
                photo.save()

        return HttpResponseRedirect(reverse("album_view", kwargs={"slug": album.slug}))
    return render(request, 'photos/photo_upload_page.html')


def filmmaking_home(request):
    return render(request, 'movies/movie_home.html')


def movie_single_view(request):
    return render(request, "movies/movie_view.html")


def movie_create(request):
    if request.method == "POST":
        movie = Movie()
        movie.owner = request.user
        movie.title = request.POST.get('movie_title')
        movie.tag_line = request.POST.get('movie_tag')
        movie.movie_details = request.POST.get('movie_details')
        movie.date_built = request.POST.get('movie_date')
        movie.youtube = request.POST.get('movie_youtube')

        poster = request.FILES.get('movie_poster')
        if poster:
            movie.movie_poster = poster

        script = request.FILES.get('movie_script')
        if script:
            movie.movie_script = script
        return HttpResponseRedirect(reverse("movie_single_view", kwargs={"slug": movie.slug}))
    return render(request, "movies/movie_create.html")


def webdev_home(request):
    return render(request, "web_dev/web_dev_home.html")


def webdev_view(request):
    return render(request, "web_dev/web_dev_single_view.html", {"website": website})


def webdev_create(request):
    if request.method == "POST":
        website = Website()
        website.owner = request.user
        website.website_name = request.POST.get('web_name')
        website.website_link = request.POST.get('web_link')
        website.website_details = request.POST.get('web_details')
        website.date_built = request.POST.get('web_date')
        website.youtube = request.POST.get('web_youtube')
        website.alt_text = request.POST.get('web_alt_text')

        screenshot = request.FILES.get('website_screenshot')
        if screenshot:
            website.website_screenshot = screenshot
        return HttpResponseRedirect(reverse("webdev_view", kwargs={"slug": website.slug}))
    return render(request, "web_dev/web_dev_create.html")


def blog_single_view(request, cat, slug):
    blog_single = get_object_or_404(Blog, category__slug=cat, slug=slug)
    cat = Category.objects.all()
    return render(request, 'blog/blog_single_view.html', {'blog': blog_single, 'cat': cat})


def blog(request):
    blog_list = Blog.objects.all()
    return render(request, "blog/blog_home.html", {'blogs': blog_list})


def blog_create(request):
    if request.method == 'POST':
        blog = Blog()

        # tags = request.POST.getlist('tag')
        print(request.POST)

        blog.title = request.POST.get('blog_title')
        blog.author = request.user
        blog.content = request.POST.get('blog_content')

        blog_image = request.FILES.get('blog_image')
        if blog_image:
            blog.image = blog_image

        blog.alt_text = request.POST.get('alt_text')
        blog.youtube_link = request.POST.get('youtube_link')

        blog.save()
        return HttpResponseRedirect(reverse('blog_single_view', kwargs={'cat': blog.category.slug, 'slug': blog.slug}))

    return render(request, 'blog/blog_create.html', {
        # 'tag': Tag.objects.all()
        'cat': Category.objects.all()
    })
