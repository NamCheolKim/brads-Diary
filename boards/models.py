from django.db import models
from core import models as core_models
from users import models as user_models


class Board(core_models.TimeStampModel):
    title = models.CharField(max_length=50)
    content = models.CharField(max_length=250)
    user = models.ForeignKey(user_models.User, on_delete=models.CASCADE)
