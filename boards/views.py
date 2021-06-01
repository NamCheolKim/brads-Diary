from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView
from . import models, forms

# 게시판 리스트


class BoardListView(ListView):
    model = models.Board
    paginate_by = 12
    paginate_orphans = 5
    ordering = "-created_at"
