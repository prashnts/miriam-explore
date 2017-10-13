import base64

from django.http import HttpResponse
from django.conf import settings


def render_auth_required():
    response = HttpResponse("""<html><title>Auth required</title><body>
                            <h1>Authorization Required</h1></body></html>""")
    response['WWW-Authenticate'] = 'Basic realm="Development"'
    response.status_code = 401
    return response


def naive_lockdown_middleware(get_response):

    def middleware(request):
        if 'HTTP_AUTHORIZATION' not in request.META:
            return render_auth_required()
        else:
            authentication = request.META['HTTP_AUTHORIZATION']
            (authmeth, auth) = authentication.split(' ', 1)
            if 'basic' != authmeth.lower():
                return render_auth_required()
            auth = base64.b64decode(auth.strip())
            username, password = auth.decode().split(':', 1)

            if username == settings.BASICAUTH_USERNAME and password == settings.BASICAUTH_PASSWORD:
                return get_response(request)

            return render_auth_required()

    return middleware

