import json
import os

from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from salaweb.models import Access
from salaweb.forms import LoginForm
from salaweb.repository import Repository


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

    return render(request, 'salaweb/login.html', {
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
    accesses = Access.objects.filter(user=request.user)
    repositories = [Repository(a.repository) for a in accesses]

    return render(request, 'salaweb/index.html', {
        'repositories': repositories,
    })


def ajax_response(status, data):
    return HttpResponse(
        json.dumps(data),
        content_type='application/json',
        status=status,
    )


@login_required
def ajax(request, repository, path):
    from django.conf import settings

    if request.method != 'POST':
        return ajax_response(503, {'error': 'Allowed methods: POST'})

    try:
        data = json.loads(request.body)
    except ValueError:
        return ajax_response(400, {'error': 'Invalid JSON'})

    if not isinstance(data, dict):
        return ajax_response(400, {'error': 'Object expected'})

    password = data.get('password')
    if not isinstance(password, unicode):
        return ajax_response(400, {'error': 'String value required: password'})

    repositories_root = os.path.abspath(os.path.join(
        settings.SALAWEB_DATADIR,
        'repositories',
    ))
    repository_path = os.path.abspath(os.path.join(
        repositories_root,
        repository,
    ))

    if repository_path[:len(repositories_root)] != repositories_root:
        return ajax_response(400, {'error': 'Directory climbing'})

    print 'repository', repository_path
    print 'path', path
    print 'password', password

    return ajax_response(200, {'value': 'foo'})


@login_required
def settings(request):
    pass


@user_passes_test(lambda user: user.is_superuser)
def admin(request):
    pass
