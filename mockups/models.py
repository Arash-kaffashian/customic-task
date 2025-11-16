from django.db import models
from django.utils.translation import gettext_lazy as _

import uuid


# Mockup Model
class Mockup(models.Model):
    # green code : why types
    COLOR_ONE = 1
    COLOR_TWO = 2
    COLOR_THREE = 3
    COLOR_FOUR = 4
    COLOR_TYPES = (
        (COLOR_ONE, _('white')),
        (COLOR_TWO, _('yellow')),
        (COLOR_THREE, _('blue')),
        (COLOR_FOUR, _('black'))
    )

    # orange code : must be change if Generation task changed
    task_id = models.CharField(max_length=100, db_index=True)
    text = models.TextField()
    font = models.CharField(max_length=100, blank=True, null=True)
    text_color = models.PositiveSmallIntegerField(_('text color'), choices=COLOR_TYPES, default=1)
    shirt_color = models.PositiveSmallIntegerField(_('shirt color'), choices=COLOR_TYPES, default=4)
    image = models.ImageField(upload_to='mockups/')
    # futures : update date for admin panel changes
    created_at = models.DateTimeField(auto_now_add=True)

    def image_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url
        return ''
