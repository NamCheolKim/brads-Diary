from django.shortcuts import render


def index(request):
    return render(request, "diary/index.html")


def unfold(request):
    return render(request, "diary/album.html")


def detail(request):
    return render(request, "diary/detail.html")
