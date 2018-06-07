from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from R_E_M.models import User, Album, Photo, Website

def home(request):
    return render(request, 'misc/home.html')


def about(request):
    return render(request, 'misc/about.html')


def photography_home(request):
    complete_album_list = Album.objects.all()
    return render(request, 'photos/photo_home.html', {'albums': complete_album_list})


def photo_album_view(request):
    album = Album.objects.get(slug=slug)
    return render(request, 'photos/photo_album_view.html', {"album": album})


def photo_single_view(request):
    photo = get_object_or_404(Album, slug=slug)
    return render(request, 'photos/single_photo_view.html', {"photo": photo})


def photo_upload(request):
    if request.method == "POST":
        print(request.POST)
        print(request.FILES)
        album = Album()
        album.owner = request.user
        album.title = request.POST.get('album_title')
        album.album_details = request.POST.get('album_details')
        album.alt_text = request.POST.get('album_alt_text')

        # photo
        photo_list = 0
        for picture in request.POST:
            if photo.startswith('photo_name_'):
                photo_list += 1

        for picture in range(photo_list):
            photo = Photo()
            photo.album = album
            photo.title = request.POST.get('photo_name_{}'.format(picture))

    return render(request, 'photos/photo_upload_page.html')


def filmmaking_home(request):
    return render(request, 'movies/movie_home.html')


def movie_single_view(request):
    return render(request, "movies/movie_view.html")


def webdev_home(request):
    return render(request, "web_dev/web_dev_home.html")


def webdev_view(request):
    return render(request, "web_dev/web_dev_single_view.html", {"website": website})


def blog_single_view(request, cat, slug):
    blog = get_object_or_404(Blog, category__slug=cat, slug=slug)
    cat = Category.objects.all()
    return render(request, 'blog/blog_single_view.html', {'blog': blog, 'cat': cat})


def blog(request):
    blog_list = Blog.objects.filter(fitness_library=False)
    return render(request, "blog/blog_home.html", {'blogs': blog_list})


def blog_create(request):
    if request.method == 'POST':
        user = User()

        # tags = request.POST.getlist('tag')
        print(request.POST)
        blog = form.save(commit=False)
        blog.author = request.user
        blog.save()
        return HttpResponseRedirect(reverse('blog_single_view', kwargs={'cat': blog.category.slug, 'slug': blog.slug}))

    return render(request, 'blog/blog_create.html', {
        # 'tag': Tag.objects.all()
        'cat': Category.objects.all(),
        'form': form
    })
