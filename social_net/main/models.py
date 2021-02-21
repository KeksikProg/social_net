from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
from slugify import slugify

from main.util import get_timestamp_path


class Client(AbstractUser):
    is_active = models.BooleanField(
        default=False,
        db_index=True,
        verbose_name='Activated?'
    )
    slug = models.SlugField(
        unique=True
    )
    phone_valid = RegexValidator(regex=r'^\+?7?\d{9,15}$')
    phone_number = models.CharField(validators=[phone_valid],
                                    max_length=17,
                                    blank=True,
                                    verbose_name='Phone')

    def save(self, *args, **kwargs):
        self.slug = slugify(self.username)
        super().save(*args, **kwargs)

    class Meta(AbstractUser.Meta):
        pass


class Rubric(models.Model):
    title = models.CharField(
        max_length=255,
        verbose_name='rubric'
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'rubric'
        verbose_name_plural = 'rubrics'
        ordering = ['-title']


class Publics(models.Model):
    users = models.ManyToManyField(
        Client
    )

    rubric = models.ForeignKey(
        Rubric,
        on_delete=models.CASCADE,
        verbose_name='rubric',
    )

    title = models.CharField(
        max_length=255,
        unique=True,
        verbose_name='title'
    )
    desc = models.CharField(
        blank=True,
        verbose_name='description',
        max_length=600
    )
    image = models.ImageField(
        blank=True,
        upload_to=get_timestamp_path,
        verbose_name='photo'
    )
    author = models.CharField(
        verbose_name='author',
        max_length=255
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='slug'
    )

    def delete(self, *args, **kwargs):
        for ai in self.additionalimage_set.all():
            ai.delete()
        super().delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'public'
        verbose_name_plural = 'publics'
        ordering = ['-title']


class Posts(models.Model):
    public = models.ForeignKey(Publics,
                               on_delete=models.CASCADE,
                               verbose_name='public')
    content = models.CharField(
        blank=True,
        verbose_name='content',
        max_length=400
    )
    image = models.ImageField(
        blank=True,
        upload_to=get_timestamp_path,
        verbose_name='image',
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name='created_at',

    )

    def delete(self, *args, **kwargs):
        for ai in self.additionalimage_set.all():
            ai.delete()
        super().delete(*args, **kwargs)

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'
        ordering = ['-created_at']


class AdditionalImage(models.Model):
    post = models.ForeignKey(
        Posts,
        on_delete=models.CASCADE
    )
    image = models.ImageField(
        upload_to=get_timestamp_path,
        verbose_name='additional_image',
    )

    def __str__(self):
        return self.image.url

    class Meta:
        verbose_name = 'additional image'
        verbose_name_plural = 'additional images'


class Comments(models.Model):
    post = models.ForeignKey(
        Posts,
        on_delete=models.CASCADE
    )
    author = models.CharField(
        max_length=255,
        verbose_name='author'
    )
    content = models.CharField(
        max_length=400,
        verbose_name='content'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name='created_at'
    )

    def __str__(self):
        self.post.title

    class Meta:
        verbose_name = 'comment'
        verbose_name_plural = 'comments'
        ordering = ['-created_at']
