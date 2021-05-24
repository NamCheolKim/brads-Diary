from django.db import models
from core import models as core_models
from users import models as user_models


# 기록하기, 상세내용
class PostDiary(core_models.TimeStampModel):

    """PostDiary Model Definition"""

    author = models.ForeignKey(
        user_models.User, related_name="author_post", on_delete=models.CASCADE
    )
    title = models.CharField(max_length=30)
    content = models.TextField()
    photo = models.ImageField(upload_to="upload-img/%Y/%m/%d/", blank=True)

    def __str__(self):
        return self.title

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
