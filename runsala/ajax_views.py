import functools
import json
import os

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from runsala.forms import NewRepositoryForm
from runsala.gpg import gpg_decrypt_string

from runsala.models import Access

_missing = object()


class AjaxError(Exception):
    def __init__(self, status, body):
        self.status = status
        self.body = body


def ajax_view(func):
    @functools.wraps(func)
    def wrapper(*args, **kwds):
        try:
            data = func(*args, **kwds)
        except AjaxError as exc:
            data = (exc.status, exc.body)

        if isinstance(data, HttpResponse):
            return data

        status, body = data
        return HttpResponse(
            json.dumps(body),
            content_type='application/json',
            status=status,
        )

    return wrapper


def parse_body(request, access):
    try:
        data = json.loads(request.body)
    except ValueError:
        raise AjaxError(400, {'error': 'Invalid JSON'})

    if not isinstance(data, dict):
        raise AjaxError(400, {'error': 'Object expected'})

    # Password is always required when there's a body
    password = data.get('password', _missing)
    if password is _missing:
        raise AjaxError(400, {'error': 'Value required: password'})

    if not isinstance(password, unicode):
        raise AjaxError(400, {'error': 'String required: password'})

    master_password = gpg_decrypt_string(access.key, data['password'])
    if not master_password:
        raise AjaxError(400, {'error': 'Invalid password'})

    data['master_password'] = master_password
    return data


@login_required
@ajax_view
def repository_create(request):
    if request.method != 'POST':
        return 503, {'error': 'Allowed methods: POST'}

    form = NewRepositoryForm(request.POST)
    if not form.is_valid():
        return 400, {'error': dict(form.errors)}

    repository = form.save()
    return 200, {
        'name': repository.name,
        'description': repository.description,
    }


@login_required
@ajax_view
def secret(request, repository, path):
    if request.method not in ('POST', 'PUT', 'DELETE'):
        return 503, {'error': 'Allowed methods: POST, PUT, DELETE'}

    try:
        access = Access.objects.get(user=request.user, repository=repository)
    except Access.DoesNotExist:
        return 404, {
            'error': 'Not found: %s' % os.path.join(repository, path),
        }

    repository_path = os.path.abspath(os.path.join(
        settings.RUNSALA_DATADIR,
        'repositories',
        repository,
    ))

    if request.method == 'POST':
        return read_secret(request, access, repository_path, path)
    elif request.method == 'PUT':
        return write_secret(request, access, repository_path, path)
    else:
        return delete_secret(repository_path, path)


def read_secret(request, access, repository_path, path):
    data = parse_body(request, access)
    repository = Repository(repository_path, data['master_password'])
    return 200, {'secret': repository.get(path)}


def write_secret():
    pass


def delete_secret():
    pass

    # elif request.method == 'PUT':
    #     secret = 
    #     sala.Repository(repository_path, master_password).get(path)

    # try:
    # except Exception:
    #     return ajax_response(404, {
    #         'error': 'Not found: %s' % os.path.join(repository, path),
    #     })

    # if not secret:
    #     # Should not happen
    #     return 500, {'error': 'Unable to decrypt secret'}

    # return 200, {'secret': secret}
