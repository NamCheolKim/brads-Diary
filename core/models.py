from django.db import models


class TimeStampModel(models.Model):

    """TimeStamp Model Definition"""

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        abstract = True
