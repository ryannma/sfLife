from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from . import form


def new(request):
    return render(request, 'dashboard.html')