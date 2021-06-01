from django.db import models
from django.shortcuts import reverse
from core import models as core_models
from users import models as user_models


# 기록하기, 상세내용
class PostDiary(core_models.TimeStampModel):

    """PostDiary Model Definition"""

    class Meta:
        ordering = ["-created_at"]

    author = models.ForeignKey(
        user_models.User, related_name="postdiarys", on_delete=models.CASCADE
    )
    title = models.CharField(max_length=30)
    content = models.TextField()
    photo = models.ImageField(upload_to="upload-img/%Y/%m/%d/", null=True, blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("diarys:detail", kwargs={"pk": self.pk})

    # def head_photo(self):
    #     try:
    #         (photo,) = self.photos.all()[:1]
    #         return photo.file.url
    #     except ValueError:
    #         return None


# # 이미지 첨부
# class Photo(core_models.TimeStampModel):

#     """Photo Model Definition"""

#     caption = models.CharField(max_length=80)
#     file = models.ImageField(upload_to="upload-img/%Y/%m/%d/", blank=True)
#     postdiary = models.ForeignKey(
#         PostDiary, related_name="photos", on_delete=models.CASCADE
#     )

#     def __str__(self):
#         return self.caption


# 댓글
class Comment(core_models.TimeStampModel):

    """Comment Model Definition"""

    class Meta:
        ordering = ["-created_at"]

    author = models.ForeignKey(
        "users.User", related_name="comments", on_delete=models.CASCADE
    )
    diary = models.ForeignKey(
        PostDiary, related_name="comments", on_delete=models.CASCADE
    )
    content = models.TextField()

    def __str__(self):
        return self.content
