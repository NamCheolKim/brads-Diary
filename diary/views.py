from django.views.generic import ListView, DetailView, FormView
from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.utils import timezone
from . import models, forms


# 대문 페이지
def index(request):
    return render(request, "diary/index.html")


# 게시물 리스트
class AlbumPostView(ListView):
    """AlbumView Definition"""

    model = models.PostDiary
    ordering = "-created_at"


# 상세 페이지
class AlbumPostDetailView(DetailView):
    """AlbumDetailView Definition"""

    model = models.PostDiary


# 게시물 작성
class AlbumPostCreateView(FormView):
    """AlbumPostCreateView Definition"""

    # model = models.PostDiary
    # fields = ["title", "content", "image"]
    form_class = forms.AlbumPostCreateForm
    template_name = "diary/postdiary_create.html"

    def form_valid(self, form):
        diary = form.save()
        diary.created_at = timezone.now()
        diary.save()
        form.save_m2m()
        messages.success(self.request, "diary Uploaded")
        return redirect(reverse("diary:detail", kwargs={"pk": diary.pk}))
