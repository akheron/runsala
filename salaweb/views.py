from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render

from salaweb.models import Access
from salaweb.forms import LoginForm


def login_view(request):
    if request.method == 'POST':
        error = True
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None and user.is_active:
                login(request, user)
                return HttpResponseRedirect(request.GET.get('next', '/'))
    else:
        form = LoginForm()
        error = False

    return render(request, 'salaweb/login.html', {
        'form': form,
        'error': error,
    })


@login_required
def index(request):
    accesses = Access.objects.filter(user=request.user)
    repos = [a.repository for a in accesses]

    return render(request, 'salaweb/index.html', {
        'repositories': repos,
    })
