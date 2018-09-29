from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify
from martor.models import MartorField


class Post(models.Model):
    description = MartorField()


def user_image_uh(instance, filename):
    return "users/{}/profile_image/{}".format(instance.username, filename)


class User(AbstractUser):
    phone_number = models.CharField(max_length=50)
    profile_bio = models.TextField(max_length=300, blank=True, null=True)
    image = models.ImageField(upload_to=user_image_uh, blank=True, null=True)


def album_cover_image_uh(instance, filename):
    return 'movies/{}/{}'.format(instance.slug, filename)


class Album(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="photo_albums")
    title = models.CharField(max_length=100, blank=True, null=True)
    category = models.ForeignKey("AlbumCategory", default=1, related_name='albums', on_delete=models.SET_DEFAULT)
    slug = models.SlugField(blank=True, null=True, unique=True)
    album_cover = models.ImageField(upload_to=album_cover_image_uh, blank=True, null=True)
    album_details = models.TextField()
    alt_text = models.CharField(max_length=100, blank=True, null=True)

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


class AlbumCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(blank=True, null=True, unique=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            number = 0
            slug_title = slugify(self.name)
            checking = True
            while checking:
                results = AlbumCategory.objects.filter(slug=slug_title)
                if results.exists():
                    slug_title = slugify(self.name) + '_' + str(number + 1)
                    number += 1
                else:
                    checking = False
                self.slug = slug_title
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'AlbumCategories'


def photo_image_uh(instance, filename):
    return 'photography/{}/{}'.format(instance.album.slug, filename)


class Photo(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="photos")
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name="photo_album")
    title = models.CharField(max_length=100, blank=True, null=True)
    slug = models.SlugField(blank=True, null=True, unique=True)
    image = models.ImageField(upload_to=photo_image_uh, blank=True, null=True)
    alt_text = models.CharField(max_length=100, blank=True, null=True)
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


class WebsiteCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(blank=True, null=True, unique=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            number = 0
            slug_title = slugify(self.name)
            checking = True
            while checking:
                results = WebsiteCategory.objects.filter(slug=slug_title)
                if results.exists():
                    slug_title = slugify(self.name) + '_' + str(number + 1)
                    number += 1
                else:
                    checking = False
                self.slug = slug_title
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'WebsiteCategories'


def website_image_uh(instance, filename):
    return 'websites/{}/{}'.format(instance.slug, filename)


class Website(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="websites")
    website_name = models.CharField(max_length=100, blank=True, null=True)
    website_link = models.CharField(max_length=100, blank=True, null=True)
    category = models.ForeignKey("WebsiteCategory", default=1, related_name='websites', on_delete=models.SET_DEFAULT)
    website_details = models.TextField()
    slug = models.SlugField(blank=True, null=True, unique=True)
    date_built = models.CharField(max_length=50)
    youtube = models.CharField(max_length=255, blank=True, null=True)
    main_page = models.ImageField(upload_to=website_image_uh, blank=True, null=True)
    alt_text = models.CharField(max_length=100, blank=True, null=True)

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


def website_screen_shot_image_uh(instance, filename):
    return 'websites/{}/{}'.format(instance.website_screenshots.slug, filename)


class WebsiteScreenShot(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="website_photos")
    website_screenshots = models.ForeignKey(Website, on_delete=models.CASCADE, related_name="website_screenshots")
    screenshot_name = models.CharField(max_length=100, blank=True, null=True)
    slug = models.SlugField(blank=True, null=True, unique=True)
    image = models.ImageField(upload_to=website_screen_shot_image_uh, blank=True, null=True)
    alt_text = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.screenshot_name

    def save(self, *args, **kwargs):
        if not self.slug:
            number = 0
            slug_title = slugify(self.screenshot_name)
            checking = True
            while checking:
                results = WebsiteScreenShot.objects.filter(slug=slug_title)
                if results.exists():
                    slug_title = slugify(self.screenshot_name) + '_' + str(number + 1)
                    number += 1
                else:
                    checking = False
                self.slug = slug_title
        super().save(args, kwargs)


def blog_image_uh(instance, filename):
    return 'blog/{}/blog_image/{}'.format(instance.author.username, filename)


class Blog(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(User, related_name='blogs', on_delete=models.CASCADE)
    date = models.CharField(max_length=50)
    content = MartorField()
    slug = models.SlugField(blank=True, null=True, unique=True)
    category = models.ForeignKey("Category", default=1, related_name='blogs', on_delete=models.SET_DEFAULT)
    image = models.ImageField(upload_to=blog_image_uh, blank=True, null=True)
    alt_text = models.CharField(max_length=100, blank=True, null=True)
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
    name = models.CharField(max_length=100)
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
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Categories'


def movie_poster_image_uh(instance, filename):
    return 'movies/{}/{}'.format(instance.slug, filename)


def movie_document_uh(instance, filename):
    return "movies/{}/{}".format(instance.slug, filename)


class Movie(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="movies")
    title = models.CharField(max_length=100, blank=True, null=True)
    category = models.ForeignKey("MovieCategory", default=1, related_name='movies', on_delete=models.SET_DEFAULT)
    tag_line = models.TextField(max_length=300, blank=True, null=True)
    movie_details = models.TextField()
    slug = models.SlugField(blank=True, null=True, unique=True)
    date_built = models.CharField(max_length=50)
    youtube = models.CharField(max_length=255, blank=True, null=True)
    movie_poster = models.ImageField(upload_to=movie_poster_image_uh, blank=True, null=True)
    alt_text = models.CharField(max_length=100, blank=True, null=True)
    movie_script = models.FileField(upload_to=movie_document_uh, blank=True, null=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            number = 0
            slug_title = slugify(self.title)
            checking = True
            while checking:
                results = Movie.objects.filter(slug=slug_title)
                if results.exists():
                    slug_title = slugify(self.title) + '_' + str(number + 1)
                    number += 1
                else:
                    checking = False
                self.slug = slug_title
        super().save(args, kwargs)


class MovieCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(blank=True, null=True, unique=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            number = 0
            slug_title = slugify(self.name)
            checking = True
            while checking:
                results = MovieCategory.objects.filter(slug=slug_title)
                if results.exists():
                    slug_title = slugify(self.name) + '_' + str(number + 1)
                    number += 1
                else:
                    checking = False
                self.slug = slug_title
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'MovieCategories'


def movie_still_photo_image_uh(instance, filename):
    return 'movies/{}/{}'.format(instance.movie_album.slug, filename)


class MovieStillPhoto(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="movie_photos")
    movie_album = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="movie_photo_album")
    title = models.CharField(max_length=100, blank=True, null=True)
    slug = models.SlugField(blank=True, null=True, unique=True)
    image = models.ImageField(upload_to=movie_still_photo_image_uh, blank=True, null=True)
    alt_text = models.CharField(max_length=100, blank=True, null=True)
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
                results = MovieStillPhoto.objects.filter(slug=slug_title)
                if results.exists():
                    slug_title = slugify(self.title) + '_' + str(number + 1)
                    number += 1
                else:
                    checking = False
                self.slug = slug_title
        super().save(args, kwargs)
