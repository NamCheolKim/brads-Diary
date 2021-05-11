from django.db import models


# 기록하기, 상세내용
class PostDiary(models.Model):
    title = models.CharField(max_length=30)
    content = models.TextField()
    image = models.ImageField(upload_to="upload/%Y/%m/%d/", blank=True)
    created_at = models.DateTimeField()
