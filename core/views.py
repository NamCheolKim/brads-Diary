from django.shortcuts import render


# 대문 페이지
def index(request):
    return render(request, "diarys/index.html")
