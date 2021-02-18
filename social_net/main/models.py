from django.contrib.auth.models import AbstractUser
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

    rubic = models.ForeignKey(
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
        verbose_name='description'
    )
    image = models.ImageField(
        blank=True,
        upload_to=get_timestamp_path,
        verbose_name='photo'
    )
    author = models.CharField(
        verbose_name='author'
    )
    slug = models.SlugField(
        unique=True
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
    pass
