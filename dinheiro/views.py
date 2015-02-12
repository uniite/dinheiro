from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import ensure_csrf_cookie
from django.shortcuts import render_to_response


@login_required
@ensure_csrf_cookie
def home(request):
    return render_to_response('app.html', {'user': request.user})
