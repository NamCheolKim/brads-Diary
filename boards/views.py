from django.shortcuts import render

# 게시판 리스트


def board_list(request):
    return render(request, "boards/board_list.html")
