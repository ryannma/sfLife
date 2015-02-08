from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from . import form


def new(request):
    if request.method == "POST":
        f = form.SearchForm(request.POST)
        if f.is_valid():
            return render(request, 'dashboard.html', {'hcp':f['hcp'],'food':f['food'],'schools':f['schools']})
    else:
        f = form.SearchForm()
    return render(request, 'new.html', {'form': f})