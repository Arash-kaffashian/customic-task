from django.db import models
from django.utils.translation import gettext_lazy as _


# shirts
class Shirt(models.Model):
    color = models.CharField(max_length=50)
    existence = models.BooleanField(default=True)
    image = models.ImageField(upload_to='shirts/')


# fonts
class Font(models.Model):
    name = models.CharField(max_length=100, blank=True)
    font = models.FileField(upload_to='fonts/')


# colors
class Color(models.Model):
    color = models.CharField(max_length=50, blank=True)


# Mockup Model
class Mockup(models.Model):

    task_id = models.CharField(max_length=100, db_index=True)
    text = models.TextField()
    font = models.OneToOneField('Font', verbose_name='Font', blank=True, on_delete=models.PROTECT)
    text_color = models.OneToOneField('Color', verbose_name='Color', blank=True, on_delete=models.PROTECT)
    shirt_color = models.OneToOneField('Shirt', verbose_name='Shirt', blank=True, on_delete=models.PROTECT)
    image = models.ImageField(upload_to='mockups/')
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def image_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url
        return ''
