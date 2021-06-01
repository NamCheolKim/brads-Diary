from django.views.generic import ListView, DetailView
from django.shortcuts import render, redirect, reverse, get_object_or_404, resolve_url
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from . import models, forms


# 게시물 리스트
class AlbumPostView(ListView):

    model = models.PostDiary
    paginate_by = 12
    paginate_orphans = 5
    ordering = "-created_at"
    context_object_name = "diarys"


# 상세 페이지
class AlbumPostDetailView(DetailView):

    model = models.PostDiary


# 게시물 작성
# users
@login_required(login_url="login")
def diary_create(request):

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
# users
@login_required(login_url="login")
def diary_modify(request, pk):

    diary = get_object_or_404(models.PostDiary, pk=pk)

    if request.user != diary.author:
        messages.error(request, "수정권한이 없습니다.")
        return redirect(reverse("diarys:detail", kwargs={"pk": diary.pk}))

    if request.method == "POST":
        form = forms.DiaryForm(request.POST, instance=diary)
        if form.is_valid():
            diary = form.save()
            diary.photo = request.FILES.get("photo", diary.photo)
            diary.author = request.user
            diary.updated_at = timezone.now()
            diary.save()
            return redirect(reverse("diarys:detail", kwargs={"pk": diary.pk}))
    else:
        form = forms.DiaryForm(instance=diary)

    context = {"form": form}
    return render(request, "diarys/postdiary_create.html", context)


# 게시물 삭제
# users
@login_required(login_url="login")
def diary_delete(request, pk):
    """Diary Delete Definition"""

    diary = get_object_or_404(models.PostDiary, pk=pk)

    if request.user != diary.author:
        messages.error(request, "삭제권한이 없습니다.")
        return redirect(reverse("diarys:detail", kwargs={"pk": diary.pk}))

    diary.delete()
    return redirect(reverse("diarys:list"))


@login_required(login_url="login")
def create_comment(request, pk):

    diary = get_object_or_404(models.PostDiary, pk=pk)

    if request.method == "POST":
        form = forms.CommentForm(request.POST)
        if form.is_valid():
            comment = form.save()
            comment.author = request.user
            comment.diary = diary
            comment.save()

            return redirect(
                "{}#comment_{}".format(
                    resolve_url("diarys:detail", pk=diary.pk), comment.pk
                )
            )
    else:
        form = forms.CommentForm()
    context = {"form": form}
    return render(request, "diarys/detail.html", context)


@login_required(login_url="login")
def comment_modify(request, pk):

    comment = get_object_or_404(models.Comment, pk=pk)

    if request.user != comment.author:
        messages.error(request, "수정권한이 없습니다.")
        return redirect(reverse("diarys:detail", kwargs={"pk": comment.diary.pk}))

    if request.method == "POST":
        form = forms.CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save()
            comment.author = request.user
            comment.updated_at = timezone.now()
            comment.save()

            return redirect(
                "{}#answer_{}".format(
                    resolve_url("diarys:detail", pk=comment.diary.pk), comment.pk
                )
            )
    else:
        form = forms.CommentForm(instance=comment)

    context = {"comment": comment, "form": form}

    return render(request, "diarys/comment_form.html", context)


@login_required(login_url="login")
def comment_delete(request, pk):

    comment = get_object_or_404(models.Comment, pk=pk)

    if request.user != comment.author:
        messages.error(request, "삭제권한이 없습니다.")
    else:
        comment.delete()

    return redirect(
        "{}#answer_{}".format(
            resolve_url("diarys:detail", pk=comment.diary.pk), comment.pk
        )
    )
