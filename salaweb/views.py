from salaweb.models import Access
from salaweb.forms import LoginForm


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            qs = Access.objects.filter(user__email=email)
            if not qs.exists():
                # Unknown email
                pass

            # Try to decrypt one key
            access = qs[0]
            if not try_decrypt(access.key, password):
                # Invalid password
                pass

