from django.shortcuts import render, HttpResponseRedirect, HttpResponse, get_object_or_404, reverse, redirect
from R_E_M.models import User, Album, AlbumCategory, Photo, Website, Blog, Category, Movie, MovieStillPhoto, \
    WebsiteScreenShot, MovieCategory, WebsiteCategory
import base64
from django.core.files.base import ContentFile
import re
import requests
from django.db.models import Q
from django.http import JsonResponse
from R_E_M.secret import insta_api_access_token
from django.core.mail import send_mail
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from math import ceil


# from PIL import Image


def home(request):
    return render(request, 'misc/home.html')


def about(request):
    return render(request, 'misc/about.html')


def technology(request):
    return render(request, 'misc/tech.html')


def contact(request):
    if request.method == "POST":
        email = request.POST.get('contact_email')
        subject = request.POST.get('contact_subject')
        body = request.POST.get('contact_body')

        send_mail(
            'New Contact From {}'.format(email),
            'Email:\n{}\n\nSubject:\n{}\n\nMessage:\n{}'.format(email, subject, body),
            '{}'.format('remington.henderson@gmail.com'),
            ['remington.henderson@gmail.com'],
            fail_silently=False,
        )

    return render(request, 'misc/contact.html')


def _albums(request, album_categories, category, complete_album_list,  data):
    paginator = Paginator(complete_album_list, 4)

    page = request.GET.get('page', 1)

    try:
        complete_album_list = paginator.page(page)
    except PageNotAnInteger:
        complete_album_list = paginator.page(1)
    except EmptyPage:
        complete_album_list = paginator.page(paginator.num_pages)

    # Get the index of the current page
    index = complete_album_list.number - 1
    # print(index)
    # This value is maximum index of pages, so the last page - 1
    max_index = len(paginator.page_range)
    # print(max_index)
    print("Index Length is: {}".format(max_index))
    # range of 7, calculate where to slice the list
    start_index = index - 3 if index >= 3 else 0
    end_index = index + 4 if index <= max_index - 4 else max_index
    # print(end_index)
    # new page range
    page_range = paginator.page_range[start_index:end_index]

    # showing first and last links in pagination
    if index >= 4:
        start_index = 1
    if end_index - index >= 4 and end_index != max_index:
        end_index = max_index
    else:
        end_index = None

    context = {
        'albums': complete_album_list,
        'insta': data,
        'album_cats': album_categories,
        'category': category,
        'page_range': page_range,
        'start_index': start_index,
        'end_index': end_index,
    }

    return render(request, 'photos/photo_home.html', context)


def photography_home(request):
    r = requests.get(
        "https://api.instagram.com/v1/users/self/media/recent/?access_token={}".format(insta_api_access_token))
    data = r.json()["data"]
    # for i in data["data"]:
    #     print(i["link"])

    complete_album_list = Album.objects.all()
    album_categories = AlbumCategory.objects.all()

    query = request.GET.get("q")
    category = request.GET.get('category')
    if query is not None and query != '' and category is not None and category != '':
        complete_album_list = complete_album_list.filter(
            Q(category__slug=category, title__icontains=query) |
            Q(category__slug=category, album_details__icontains=query) |
            Q(category__slug=category, category__name__icontains=query)
        )
    elif query is not None and query != '':
        complete_album_list = complete_album_list.filter(
            Q(title__icontains=query) |
            Q(album_details__icontains=query) |
            Q(category__name__icontains=query)
        )
    elif category is not None and category != '':
        complete_album_list = complete_album_list.filter(
            Q(category__slug=category) |
            Q(category__slug=category) |
            Q(category__slug=category)
        )

    # if query:
    #     complete_album_list = complete_album_list.filter(
    #         Q(title__icontains=query) |
    #         Q(album_details__icontains=query) |
    #         Q(category__name__icontains=query)
    #     )

    if request.method == "POST":
        # print(request.POST)
        # print(request.FILES)
        album = Album()
        cat, created = AlbumCategory.objects.get_or_create(name=request.POST.get('album_category'))
        album.category = cat
        album.owner = request.user
        album.title = request.POST.get('album_title')
        album.album_details = request.POST.get('album_details')
        album_poster = request.FILES.get('album_cover_image')
        album.alt_text = request.POST.get('album_alt_text')
        if album_poster:
            album.album_cover = album_poster

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

        return HttpResponseRedirect('/photography/galleries/{}/{}/'.format(album.category.slug, album.slug))
    return _albums(request, album_categories, category, complete_album_list, data)
    # return render(request, 'photos/photo_home.html', {"album_cats": album_categories, 'albums': complete_album_list, "insta": data})


def photo_album_view(request, cat, album_slug):
    album = Album.objects.get(category__slug=cat, slug=album_slug)
    # photos = Photo.objects.get(album=slug)
    return render(request, 'photos/photo_album_view.html', {"album": album})


def photo_single_view(request, cat, album_slug, slug):
    photo = get_object_or_404(Photo, album__category__slug=cat, album__slug=album_slug, slug=slug)
    album_categories = AlbumCategory.objects.all()
    album_list = Album.objects.all()
    return render(request, 'photos/single_photo_view.html',
                  {"album_cats": album_categories, "albums": album_list, "photo": photo})


def photo_ajax(request):
    if request.method == "POST":
        print('we are at post')
        album_response = Album.objects.filter(
            category__slug=request.POST.get("category")
        )
        response = []
        for album in album_response:
            response.append({
                "title": album.title,
                "owner": {
                    "username": album.owner.username
                },
                "slug": album.slug,
                "category": {
                    "name": album.category.name,
                    "slug": album.category.slug
                },
                "album_details": album.album_details,
                "alt_text": album.alt_text,
                "photo_album": [{"url": img.image.url, "alt_text": img.alt_text} for img in album.photo_album.all()]
            })

        return JsonResponse(response, safe=False)
    return JsonResponse({"message": "Must be POST"})


def photo_upload(request):
    if request.method == "POST":
        # print(request.POST)
        # print(request.FILES)
        album = Album()
        cat, created = AlbumCategory.objects.get_or_create(name=request.POST.get('album_category'))
        album.category = cat
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

        return HttpResponseRedirect('/photography/galleries/{}/{}/'.format(album.category.slug, album.slug))
    return render(request, 'photos/photo_upload_page.html', {'cat': AlbumCategory.objects.all()})


def _movies(request, movie_categories, category, complete_movie_list):
    paginator = Paginator(complete_movie_list, 3)

    try:
        page = int(request.GET.get('page', '1'))
    except:
        page = 1

    try:
        complete_movie_list = paginator.page(page)
    except PageNotAnInteger:
        complete_movie_list = paginator.page(1)
    except EmptyPage:
        complete_movie_list = paginator.page(paginator.num_pages)

    # Get the index of the current page
    index = complete_movie_list.number - 1
    # print(index)
    # This value is maximum index of pages, so the last page - 1
    max_index = len(paginator.page_range)
    # print(max_index)
    print("Index Length is: {}".format(max_index))
    # range of 7, calculate where to slice the list
    start_index = index - 2 if index >= 2 else 0
    end_index = index + 3 if index <= max_index - 3 else max_index
    # print(end_index)
    # new page range
    page_range = paginator.page_range[start_index:end_index]

    # showing first and last links in pagination
    if index >= 3:
        start_index = 1
    if end_index - index >= 3 and end_index != max_index:
        end_index = max_index
    else:
        end_index = None

    context = {
        'movies': complete_movie_list,
        'movie_cats': movie_categories,
        'category': category,
        'page_range': page_range,
        'start_index': start_index,
        'end_index': end_index,
    }

    return render(request, 'movies/movie_home.html', context)


def filmmaking_home(request):
    complete_movie_list = Movie.objects.order_by("date_built").reverse()
    movie_categories = MovieCategory.objects.all()

    query = request.GET.get("q")
    category = request.GET.get('category')

    if query is not None and query != '' and category is not None and category != '':
        complete_movie_list = complete_movie_list.filter(
            Q(category__slug=category, title__icontains=query) |
            Q(category__slug=category, tag_line__icontains=query) |
            Q(category__slug=category, movie_details__icontains=query) |
            Q(category__slug=category, category__name__icontains=query)
        )
    elif query is not None and query != '':
        complete_movie_list = complete_movie_list.filter(
            Q(title__icontains=query) |
            Q(tag_line__icontains=query) |
            Q(movie_details__icontains=query) |
            Q(category__name__icontains=query)
        )
    elif category is not None and category != '':
        complete_movie_list = complete_movie_list.filter(
            Q(category__slug=category) |
            Q(category__slug=category) |
            Q(category__slug=category)
        )

    # if query:
    #     complete_movie_list = complete_movie_list.filter(
    #         Q(title__icontains=query) |
    #         Q(tag_line__icontains=query) |
    #         Q(movie_details__icontains=query) |
    #         Q(category__name__icontains=query)
    #     )

    if request.method == "POST":
        # print(request.FILES)
        # print(request.POST)
        movie = Movie()
        movie.owner = request.user
        movie.title = request.POST.get('movie_title')
        cat, created = MovieCategory.objects.get_or_create(name=request.POST.get('movie_category'))
        movie.category = cat
        movie.tag_line = request.POST.get('movie_tag')
        movie.movie_details = request.POST.get('movie_details')
        movie.date_built = request.POST.get('movie_date')
        movie.youtube = request.POST.get('movie_youtube')
        movie.alt_text = request.POST.get('alt_text')

        poster = request.FILES.get('movie_poster')
        if poster:
            movie.movie_poster = poster

        script = request.FILES.get('movie_script')
        if script:
            movie.movie_script = script

        movie.save()

        for k, v in request.POST.items():
            if re.match('^image_\d+$', k):
                num = int(re.search(r'\d+', k).group())
                format, imgstr = v.split(';base64,')
                ext = format.split('/')[-1]
                data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

                photo = MovieStillPhoto()
                photo.image = data
                photo.movie_album = movie
                photo.owner = request.user
                photo.title = request.POST.get('image_name_{}'.format(num))
                photo.alt_text = request.POST.get('alt_text_{}'.format(num))
                photo.date_taken = request.POST.get('creation_date_{}'.format(num))
                photo.image_details = request.POST.get('image_details_{}'.format(num))
                photo.save()

        return HttpResponseRedirect(
            reverse("movie_single_view", kwargs={"cat": movie.category.slug, "slug": movie.slug}))
    return _movies(request, movie_categories, category, complete_movie_list)
    # return render(request, 'movies/movie_home.html', {"movie_cats": movie_categories, 'movies': complete_movie_list})


def movie_single_view(request, cat, slug):
    movie = Movie.objects.get(category__slug=cat, slug=slug)
    return render(request, "movies/movie_view.html", {"movie": movie})


def movie_ajax(request):
    if request.method == "POST":
        print(request.POST)
        movie_response = Movie.objects.filter(
            category__slug=request.POST.get("category")
        )
        response = []
        for movie in movie_response:
            response.append(
                {
                    "title": movie.title,
                    "owner": {
                        "username": movie.owner.username
                    },
                    "date_built": movie.date_built,
                    "movie_details": movie.movie_details,
                    "slug": movie.slug,
                    "tag_line": movie.tag_line,
                    "category": {
                        "name": movie.category.name,
                        "slug": movie.category.slug
                    },
                    "movie_poster": {
                        "url": movie.movie_poster.url
                    },
                    "movie_script": {
                        "url": movie.movie_script.url
                    },
                    "alt_text": movie.alt_text,
                    "youtube": movie.youtube
                }
            )
        return JsonResponse(response, safe=False)
    return JsonResponse({"message": "Must be POST"})


def movie_create(request):
    if request.method == "POST":
        # print(request.FILES)
        # print(request.POST)
        movie = Movie()
        movie.owner = request.user
        movie.title = request.POST.get('movie_title')
        cat, created = MovieCategory.objects.get_or_create(name=request.POST.get('movie_category'))
        movie.category = cat
        movie.tag_line = request.POST.get('movie_tag')
        movie.movie_details = request.POST.get('movie_details')
        movie.date_built = request.POST.get('movie_date')
        movie.youtube = request.POST.get('movie_youtube')
        movie.alt_text = request.POST.get('alt_text')

        poster = request.FILES.get('movie_poster')
        if poster:
            movie.movie_poster = poster

        script = request.FILES.get('movie_script')
        if script:
            movie.movie_script = script

        movie.save()

        for k, v in request.POST.items():
            if re.match('^image_\d+$', k):
                num = int(re.search(r'\d+', k).group())
                format, imgstr = v.split(';base64,')
                ext = format.split('/')[-1]
                data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

                photo = MovieStillPhoto()
                photo.image = data
                photo.movie_album = movie
                photo.owner = request.user
                photo.title = request.POST.get('image_name_{}'.format(num))
                photo.alt_text = request.POST.get('alt_text_{}'.format(num))
                photo.date_taken = request.POST.get('creation_date_{}'.format(num))
                photo.image_details = request.POST.get('image_details_{}'.format(num))
                photo.save()

        return HttpResponseRedirect(
            reverse("movie_single_view", kwargs={"cat": movie.category.slug, "slug": movie.slug}))
    return render(request, "movies/movie_create.html", {'cat': MovieCategory.objects.all()})


def _websites(request, website_categories, category, complete_website_list):
    paginator = Paginator(complete_website_list, 4)

    try:
        page = int(request.GET.get('page', '1'))
    except:
        page = 1

    try:
        complete_website_list = paginator.page(page)
    except PageNotAnInteger:
        complete_website_list = paginator.page(1)
    except EmptyPage:
        complete_website_list = paginator.page(paginator.num_pages)

    # Get the index of the current page
    index = complete_website_list.number - 1
    # print(index)
    # This value is maximum index of pages, so the last page - 1
    max_index = len(paginator.page_range)
    # print(max_index)
    print("Index Length is: {}".format(max_index))
    # range of 7, calculate where to slice the list
    start_index = index - 3 if index >= 3 else 0
    end_index = index + 4 if index <= max_index - 4 else max_index
    # print(end_index)
    # new page range
    page_range = paginator.page_range[start_index:end_index]

    # showing first and last links in pagination
    if index >= 4:
        start_index = 1
    if end_index - index >= 4 and end_index != max_index:
        end_index = max_index
    else:
        end_index = None

    context = {
        'websites': complete_website_list,
        'website_cats': website_categories,
        'category': category,
        'page_range': page_range,
        'start_index': start_index,
        'end_index': end_index,
    }

    return render(request, "web_dev/web_dev_home.html", context)


def webdev_home(request):
    website_categories = WebsiteCategory.objects.all()
    complete_website_list = Website.objects.order_by("date_built").reverse()

    query = request.GET.get("q")
    category = request.GET.get('category')
    if query is not None and query != '' and category is not None and category != '':
        complete_website_list = complete_website_list.filter(
            Q(category__slug=category, website_name__icontains=query) |
            Q(category__slug=category, website_details__icontains=query) |
            Q(category__slug=category, category__name__icontains=query)
        )
    elif query is not None and query != '':
        complete_website_list = complete_website_list.filter(
            Q(website_name__icontains=query) |
            Q(website_details__icontains=query) |
            Q(category__name__icontains=query)
        )
    elif category is not None and category != '':
        complete_website_list = complete_website_list.filter(
            Q(category__slug=category) |
            Q(category__slug=category) |
            Q(category__slug=category)
        )

    # if query:
    #     complete_website_list = complete_website_list.filter(
    #         Q(website_name__icontains=query) |
    #         Q(website_details__icontains=query) |
    #         Q(category__name__icontains=query)
    #     )
    if request.method == "POST":
        website = Website()
        website.owner = request.user
        website.website_name = request.POST.get('web_name')
        website.website_link = request.POST.get('web_link')
        cat, created = WebsiteCategory.objects.get_or_create(name=request.POST.get('website_category'))
        website.category = cat
        website.website_details = request.POST.get('web_details')
        website.date_built = request.POST.get('web_date')
        website.youtube = request.POST.get('web_youtube')
        website.alt_text = request.POST.get('web_alt_text')
        web_main_page = request.FILES.get('website_main_page')
        if web_main_page:
            website.main_page = web_main_page

        website.save()

        for k, v in request.POST.items():
            if re.match('^image_\d+$', k):
                num = int(re.search(r'\d+', k).group())
                format, imgstr = v.split(';base64,')
                ext = format.split('/')[-1]
                data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

                photo = WebsiteScreenShot()
                photo.website_screenshots = website
                photo.image = data

                photo.owner = request.user
                photo.screenshot_name = request.POST.get('image_name_{}'.format(num))
                photo.alt_text = request.POST.get('alt_text_{}'.format(num))
                photo.save()
        return HttpResponseRedirect(
            reverse("website_single_view", kwargs={"cat": website.category.slug, "slug": website.slug}))
    return _websites(request, website_categories, category, complete_website_list)
    # return render(request, "web_dev/web_dev_home.html", {"website_cats": website_categories, "websites": complete_website_list})


def website_ajax(request):
    if request.method == "POST":
        print(request.POST)
        website_response = Website.objects.filter(
            category__slug=request.POST.get("category")
        )
        response = []
        for website in website_response:
            response.append(
                {
                    "website_name": website.website_name,
                    "owner": {
                        "username": website.owner.username
                    },
                    "date_built": website.date_built,
                    "website_link": website.website_link,
                    "website_details": website.website_details,
                    "slug": website.slug,
                    "category": {
                        "name": website.category.name,
                        "slug": website.category.slug
                    },
                    "main_page": {
                        "url": website.main_page.url
                    },
                    "alt_text": website.alt_text,
                    "youtube": website.youtube
                }
            )
        return JsonResponse(response, safe=False)
    return JsonResponse({"message": "Must be POST"})


def webdev_view(request, cat, slug):
    website = Website.objects.get(category__slug=cat, slug=slug)
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


def _blogs(request, blog_list, category, cat):
    paginator = Paginator(blog_list, 9)

    try:
        page = int(request.GET.get('page', '1'))
    except:
        page = 1

    try:
        blog_list = paginator.page(page)
    except PageNotAnInteger:
        blog_list = paginator.page(1)
    except EmptyPage:
        blog_list = paginator.page(paginator.num_pages)

    # Get the index of the current page
    index = blog_list.number - 1
    # print(index)
    # This value is maximum index of pages, so the last page - 1
    max_index = len(paginator.page_range)
    # print(max_index)
    print("Index Length is: {}".format(max_index))
    # range of 7, calculate where to slice the list
    start_index = index - 8 if index >= 8 else 0
    end_index = index + 9 if index <= max_index - 9 else max_index
    # print(end_index)
    # new page range
    page_range = paginator.page_range[start_index:end_index]

    # showing first and last links in pagination
    if index >= 9:
        start_index = 1
    if end_index - index >= 9 and end_index != max_index:
        end_index = max_index
    else:
        end_index = None

    context = {
        'blog_list': blog_list,
        'cat': cat,
        'category': category,
        'page_range': page_range,
        'start_index': start_index,
        'end_index': end_index,
    }

    return render(request, "blog/blog_home.html", context)


def blog(request):
    blog_list = Blog.objects.order_by("date").reverse()
    cat = Category.objects.all()

    # Original Pagination
    # paginator = Paginator(blog_list, 9)
    # page = request.GET.get('page')
    # blogs = paginator.get_page(page)

    # Blog Search Function
    query = request.GET.get("q")
    category = request.GET.get('category')
    if query is not None and query != '' and category is not None and category != '':
        blog_list = blog_list.filter(
            Q(category__slug=category, title__icontains=query) |
            Q(category__slug=category, content__icontains=query) |
            Q(category__slug=category, category__name__icontains=query)
        )
    elif query is not None and query != '':
        blog_list = blog_list.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(category__name__icontains=query)
        )
    elif category is not None and category != '':
        blog_list = blog_list.filter(
            Q(category__slug=category) |
            Q(category__slug=category) |
            Q(category__slug=category)
        )
    # This is the Blog Create View Function and Renders to that completed Blog
    if request.method == 'POST':
        blog = Blog()
        cat, created = Category.objects.get_or_create(name=request.POST.get('category'))
        blog.title = request.POST.get('blog_title')
        blog.author = request.user
        blog.content = request.POST.get('blog_content')
        blog.category = cat
        blog_image = request.FILES.get('blog_image')
        if blog_image:
            # print("we got here")
            blog.image = blog_image

        blog.alt_text = request.POST.get('alt_text')
        blog.youtube_link = request.POST.get('youtube_link')
        blog.date = request.POST.get('blog_date')
        blog.save()
        return HttpResponseRedirect(reverse('blog_single_view', kwargs={'cat': blog.category.slug, 'slug': blog.slug}))
    return _blogs(request, blog_list, category, cat)
    # return render(request, "blog/blog_home.html", {'blogs': blogs, 'cat': cat})


def blog_ajax(request):
    if request.method == "POST":
        blog_response = Blog.objects.filter(
            category__slug=request.POST.get("category")
        )
        # print(len(blog_response))
        page_size = 3
        print(len(blog_response) // page_size)

        response = {
            "pages": ceil(len(blog_response) / page_size),
            "blogs": []
        }
        for b in blog_response:
            response["blogs"].append(
                {
                    "title": b.title,
                    "author": {
                        "username": b.author.username
                    },
                    "date": b.date.strftime('%b %e, %Y, %I:%M %p'),
                    "content": b.content,
                    "slug": b.slug,
                    "category": {
                        "name": b.category.name,
                        "slug": b.category.slug
                    },
                    "image": {
                        "url": b.image.url
                    },
                    "alt_text": b.alt_text,
                    "youtube_link": b.youtube_link
                }
            )

        return JsonResponse(response, safe=False)
    return JsonResponse({"message": "Must be POST"})


def blog_create(request):
    if request.method == 'POST':
        blog = Blog()
        cat, created = Category.objects.get_or_create(name=request.POST.get('category'))
        blog.title = request.POST.get('blog_title')
        blog.author = request.user
        blog.content = request.POST.get('blog_content')
        blog.category = cat
        blog_image = request.FILES.get('blog_image')
        if blog_image:
            # print("we got here")
            blog.image = blog_image

        blog.alt_text = request.POST.get('alt_text')
        blog.youtube_link = request.POST.get('youtube_link')
        blog.save()
        return HttpResponseRedirect(reverse('blog_single_view', kwargs={'cat': blog.category.slug, 'slug': blog.slug}))
    return render(request, 'blog/blog_create.html', {'cat': Category.objects.all()})


def instagram_api(request):
    r = requests.get(
        "https://api.instagram.com/v1/users/self/media/recent/?access_token={}".format(insta_api_access_token))
    return HttpResponse(r.text)
