from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify


def user_image_uh(instance, filename):
    return "users/{}/profile_image/{}".format(instance.username, filename)


class User(AbstractUser):
    phone_number = models.CharField(max_length=50)
    profile_bio = models.TextField(max_length=300, blank=True, null=True)
    image = models.ImageField(upload_to=user_image_uh, blank=True, null=True)


class Album(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="photo_albums")
    title = models.CharField(max_length=50, blank=True, null=True)
    slug = models.SlugField(blank=True, null=True, unique=True)
    album_details = models.TextField()
    alt_text = models.CharField(max_length=30, blank=True, null=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            number = 0
            slug_title = slugify(self.title)
            checking = True
            while checking:
                results = Album.objects.filter(slug=slug_title)
                if results.exists():
                    slug_title = slugify(self.title) + '_' + str(number + 1)
                    number += 1
                else:
                    checking = False
                self.slug = slug_title
        super().save(args, kwargs)


def photo_image_uh(instance, filename):
    return 'photography/{}/{}'.format(instance.album, filename)


class Photo(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="photos")
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name="photo_album")
    title = models.CharField(max_length=50, blank=True, null=True)
    slug = models.SlugField(blank=True, null=True, unique=True)
    image = models.ImageField(upload_to=photo_image_uh, blank=True, null=True)
    alt_text = models.CharField(max_length=50, blank=True, null=True)
    date_taken = models.CharField(max_length=50)
    image_details = models.TextField()

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            number = 0
            slug_title = slugify(self.title)
            checking = True
            while checking:
                results = Photo.objects.filter(slug=slug_title)
                if results.exists():
                    slug_title = slugify(self.title) + '_' + str(number + 1)
                    number += 1
                else:
                    checking = False
                self.slug = slug_title
        super().save(args, kwargs)


def website_image_uh(instance, filename):
    return 'websites/{}/{}'.format(instance.website_name, filename)


class Website(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="websites")
    website_name = models.CharField(max_length=50, blank=True, null=True)
    website_link = models.CharField(max_length=100, blank=True, null=True)
    website_details = models.TextField()
    slug = models.SlugField(blank=True, null=True, unique=True)
    date_built = models.CharField(max_length=50)
    youtube = models.CharField(max_length=255, blank=True, null=True)
    website_screenshot = models.ImageField(upload_to=website_image_uh, blank=True, null=True)
    alt_text = models.CharField(max_length=50, blank=True, null=True)
    image_details = models.TextField()

    def __str__(self):
        return self.website_name

    def save(self, *args, **kwargs):
        if not self.slug:
            number = 0
            slug_title = slugify(self.website_name)
            checking = True
            while checking:
                results = Website.objects.filter(slug=slug_title)
                if results.exists():
                    slug_title = slugify(self.website_name) + '_' + str(number + 1)
                    number += 1
                else:
                    checking = False
                self.slug = slug_title
        super().save(args, kwargs)


def blog_image_uh(instance, filename):
    return 'blog/{}/blog_image/{}'.format(instance.author, filename)


class Blog(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(User, related_name='blogs', on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    slug = models.SlugField(blank=True, null=True, unique=True)
    category = models.ForeignKey("Category", default=1, related_name='blogs', on_delete=models.SET_DEFAULT)
    image = models.ImageField(upload_to=blog_image_uh, blank=True, null=True)
    alt_text = models.CharField(max_length=30, blank=True, null=True)
    youtube_link = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            number = 0
            slug_title = slugify(self.title)
            checking = True
            while checking:
                results = Blog.objects.filter(slug=slug_title)
                if results.exists():
                    slug_title = slugify(self.title) + '_' + str(number + 1)
                    number += 1
                else:
                    checking = False
                self.slug = slug_title
        super().save(args, kwargs)

    class Meta:
        ordering = ['-pk']


class Category(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(blank=True, null=True, unique=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            number = 0
            slug_title = slugify(self.name)
            checking = True
            while checking:
                results = Category.objects.filter(slug=slug_title)
                if results.exists():
                    slug_title = slugify(self.name) + '_' + str(number + 1)
                    number += 1
                else:
                    checking = False
                self.slug = slug_title
            super().save(args, kwargs)

    class Meta:
        verbose_name_plural = 'Categories'


def movie_poster_image_uh(instance, filename):
    return 'movies/{}/{}'.format(instance.title, filename)


def movie_document_uh(instance, filename):
    return "movies/{}/{}".format(instance.title, filename)


class Movie(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="movies")
    title = models.CharField(max_length=50, blank=True, null=True)
    tag_line = models.TextField(max_length=300, blank=True, null=True)
    movie_details = models.TextField()
    slug = models.SlugField(blank=True, null=True, unique=True)
    # alt_text = models.CharField(max_length=50, blank=True, null=True)
    date_built = models.CharField(max_length=50)
    youtube = models.CharField(max_length=255, blank=True, null=True)
    movie_poster = models.ImageField(upload_to=movie_poster_image_uh, blank=True, null=True)
    movie_script = models.FileField(upload_to=movie_document_uh, blank=True, null=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            number = 0
            slug_title = slugify(self.title)
            checking = True
            while checking:
                results = Website.objects.filter(slug=slug_title)
                if results.exists():
                    slug_title = slugify(self.title) + '_' + str(number + 1)
                    number += 1
                else:
                    checking = False
                self.slug = slug_title
        super().save(args, kwargs)