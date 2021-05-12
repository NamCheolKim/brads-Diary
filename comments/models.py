from django.db import models
from core import models as core_models


class Comment(core_models.TimeStampModel):

    """Comment Model Definition"""

    comment = models.TextField()
    user = models.ForeignKey(
        "users.User", related_name="comments", on_delete=models.CASCADE
    )
    diary = models.ForeignKey(
        "diarys.PostDiary", related_name="comments", on_delete=models.CASCADE
    )

    def __str__(self):
        return self.comment
