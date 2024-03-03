from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.contrib.auth.models import User

# Create your models here.
class MovieCategory(models.Model):
    name = models.CharField(max_length=250,unique=True)
    slug = models.SlugField(max_length=250, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'movie category'
        verbose_name_plural = 'movie categories'
    
    def get_url(self):
        return reverse('movies:movies_by_category', args=[self.slug])
    
    def __str__(self):
        return '{}'.format(self.name)


class Movie(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    poster = models.ImageField(upload_to='movie_posters', blank=True, null=True)
    description = models.TextField()
    release_date = models.DateField()
    actors = models.CharField(max_length=255)
    category = models.ForeignKey('MovieCategory', on_delete=models.CASCADE)
    trailer_link = models.URLField()
    added_by = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ('title',)
    
    def save(self, *args, **kwargs):
        if not self.slug:  # Check if the slug is not already set
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('movie_detail', args=[str(self.slug)])
    
    def get_absolute_url2(self):
        return reverse('edit_my_movie', args=[str(self.slug)])

    def __str__(self):
        return self.title

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey('Movie', on_delete=models.CASCADE)
    text = models.TextField()
    rating = models.PositiveIntegerField()