from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseRedirect
from django.shortcuts import render

from runsala.models import Access
from runsala.forms import LoginForm


def login(request):
    from django.contrib.auth import authenticate, login

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

    return render(request, 'runsala/login.html', {
        'form': form,
        'error': error,
    })


def logout(request):
    from django.contrib.auth import logout
    from django.conf import settings

    logout(request)
    return HttpResponseRedirect(settings.LOGIN_URL)


@login_required
def index(request):
    accesses = Access.objects \
        .select_related('repository') \
        .filter(user=request.user)

    repositories = sorted(
        [access.repository for access in accesses],
        key=lambda repository: repository.name,
    )

    return render(request, 'runsala/index.html', {
        'repositories': repositories,
    })


@login_required
def settings(request):
    pass


@user_passes_test(lambda user: user.is_superuser)
def admin(request):
    pass
