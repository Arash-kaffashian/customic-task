from django.db import models
from django.utils.translation import gettext_lazy as _

import uuid


# orange code : do we need tasks model ?
# Tasks Model
class GenerationTask(models.Model):
    # orange code : do we realy need to generate task_id ?
    task_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    status = models.CharField(max_length=50, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.task_id


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
    gen_task = models.ForeignKey(GenerationTask, related_name='results', on_delete=models.CASCADE)
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
