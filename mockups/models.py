from django.db import models
from django.core.cache import cache


# ---------------------------
# SHIRT MODEL
# ---------------------------
class Shirt(models.Model):
    color = models.CharField(max_length=50)
    existence = models.BooleanField(default=True)
    image = models.ImageField(upload_to='shirts/')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        cache.delete("shirts:list")

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        cache.delete("shirts:list")


# ---------------------------
# FONT MODEL
# ---------------------------
class Font(models.Model):
    name = models.CharField(max_length=100, blank=True)
    font = models.FileField(upload_to='fonts/')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        cache.delete("fonts:list")

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        cache.delete("fonts:list")


# ---------------------------
# COLOR MODEL
# ---------------------------
class Color(models.Model):
    color = models.CharField(max_length=50, blank=True)
    hex = models.CharField(max_length=7, unique=True)

    def __str__(self):
        return self.color

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        cache.delete("colors:list")

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        cache.delete("colors:list")


# Mockup Model
class Mockup(models.Model):

    task_id = models.CharField(max_length=100, db_index=True)
    text = models.TextField()

    font = models.ForeignKey('Font', verbose_name='Font', blank=True, on_delete=models.PROTECT)
    text_color = models.ForeignKey('Color', verbose_name='Color', blank=True, on_delete=models.PROTECT)
    shirt_color = models.ForeignKey('Shirt', verbose_name='Shirt', blank=True, on_delete=models.PROTECT)

    image = models.ImageField(upload_to='mockups/')
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def image_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url
        return ''
