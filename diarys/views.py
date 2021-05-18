from django.views.generic import ListView, DetailView, FormView
from django.shortcuts import render, redirect, reverse
from django.core.paginator import Paginator
from django.contrib import messages
from . import models, forms


# 게시물 리스트
class AlbumPostView(ListView):
    """AlbumView Definition"""

    def get(self, request):

        # 페이지
        page = request.GET.get("page", 1)

        # 조회
        postdiary_list = models.PostDiary.objects.order_by("-created_at")

        # 페이징
        paginator = Paginator(postdiary_list, 12)
        page_obj = paginator.get_page(page)

        context = {"postdiary_list": page_obj}

        return render(request, "diarys/postdiary_list.html", context)

    # model = models.PostDiary
    # ordering = "-created_at"


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
    template_name = "diarys/postdiary_create.html"

    def form_valid(self, form):
        diary = form.save()
        diary.save()
        form.save_m2m()
        messages.success(self.request, "diary Uploaded")
        return redirect(reverse("diarys:detail", kwargs={"pk": diary.pk}))
