from django.views.generic import ListView, DetailView
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from . import models, forms


# 게시물 리스트
class AlbumPostView(ListView):
    """AlbumView Definition"""

    model = models.PostDiary
    paginate_by = 12
    paginate_orphans = 5
    ordering = "-created_at"
    context_object_name = "diarys"


# 상세 페이지
class AlbumPostDetailView(DetailView):
    """AlbumDetailView Definition"""

    model = models.PostDiary


# 게시물 작성
@login_required(login_url="users:login")
def diary_create(request):
    """Diary Create Definition"""

    if request.method == "POST":
        form = forms.DiaryForm(request.POST)
        if form.is_valid():
            diary = form.save()
            diary.photo = request.FILES.get("photo", None)
            diary.author = request.user
            diary.save()

            return redirect(reverse("diarys:list"))
    else:
        form = forms.DiaryForm()

    context = {"form": form}

    return render(request, "diarys/postdiary_create.html", context)


# 게시물 수정
@login_required(login_url="core:login")
def diary_modify(request, pk):
    """Diary Modify Definition"""

    diary = get_object_or_404(models.PostDiary, pk=pk)

    if request.user != diary.author:
        messages.error(request, "수정권한이 없습니다.")
        return redirect(reverse("diarys:detail", kwargs={"pk": diary.pk}))

    if request.method == "POST":
        form = forms.DiaryForm(request.POST, instance=diary)
        if form.is_valid():
            diary = form.save()
            diary.photo = request.FILES["photo"]
            diary.author = request.user
            diary.updated_at = timezone.now()
            diary.save()
            return redirect(reverse("diarys:detail", kwargs={"pk": diary.pk}))
    else:
        form = forms.DiaryForm(instance=diary)

    context = {"form": form}
    return render(request, "diarys/postdiary_create.html", context)


# 게시물 삭제
@login_required(login_url="core:login")
def diary_delete(request, pk):
    """Diary Delete Definition"""

    diary = get_object_or_404(models.PostDiary, pk=pk)

    if request.user != diary.author:
        messages.error(request, "삭제권한이 없습니다.")
        return redirect(reverse("diarys:detail", kwargs={"pk": diary.pk}))

    diary.delete()
    return redirect(reverse("diarys:list"))


# 댓글 작성
@login_required(login_url="core:login")
def create_comment(request, pk):
    diary = get_object_or_404(models.PostDiary, pk=pk)

    if request.method == "POST":
        form = forms.CreateCommentForm(request.POST)
        if form.is_valid():
            comment = form.save()
            comment.author = request.user
            comment.diary = diary
            comment.save()

            return redirect(
                reverse("diarys:detail", kwargs={"pk": diary.pk}), comment.pk
            )
    else:
        form = forms.CreateCommentForm()
    context = {"form": form}

    return render(request, "diarys/postdiary_detail.html", context)
