import time
from django.conf import settings
from django.contrib.sessions.backends.base import UpdateError
from django.contrib.sessions.exceptions import SessionInterrupted
from django.utils.cache import patch_vary_headers
from django.utils.http import http_date
from django.middleware.csrf import CsrfViewMiddleware, CSRF_SESSION_KEY
from django.contrib.sessions.middleware import SessionMiddleware
from funix.utils.request import is_iframe

class CustomSessionMiddleware(SessionMiddleware):

    def process_response(self, request, response):
        """
        If request.session was modified, or if the configuration is to save the
        session every time, save the changes and set a session cookie or delete
        the session cookie if the session has been emptied.
        """
        try:
            accessed = request.session.accessed
            modified = request.session.modified
            empty = request.session.is_empty()
        except AttributeError:
            return response
        # First check if we need to delete this cookie.
        # The session should be deleted only if the session is entirely empty.
        if settings.SESSION_COOKIE_NAME in request.COOKIES and empty:
            if is_iframe(request) == True:
                response.delete_cookie(
                    settings.IFRAME_SESSION_COOKIE_NAME,
                    path=settings.SESSION_COOKIE_PATH,
                    domain=settings.SESSION_COOKIE_DOMAIN,
                    samesite=settings.SESSION_COOKIE_SAMESITE,
                )
            else: 
                response.delete_cookie(
                    settings.SESSION_COOKIE_NAME,
                    path=settings.SESSION_COOKIE_PATH,
                    domain=settings.SESSION_COOKIE_DOMAIN,
                    samesite=settings.SESSION_COOKIE_SAMESITE,
                )
            patch_vary_headers(response, ('Cookie',))
        else:
            if accessed:
                patch_vary_headers(response, ('Cookie',))
            if (modified or settings.SESSION_SAVE_EVERY_REQUEST) and not empty:
                if request.session.get_expire_at_browser_close():
                    max_age = None
                    expires = None
                else:
                    max_age = request.session.get_expiry_age()
                    expires_time = time.time() + max_age
                    expires = http_date(expires_time)
                # Save the session data and refresh the client cookie.
                # Skip session save for 500 responses, refs #3881.
                if response.status_code != 500:
                    try:
                        request.session.save()
                    except UpdateError:
                        raise SessionInterrupted(
                            "The request's session was deleted before the "
                            "request completed. The user may have logged "
                            "out in a concurrent request, for example."
                        )
                    if is_iframe(request):
                        response.set_cookie(
                            settings.IFRAME_SESSION_COOKIE_NAME,
                            request.session.session_key, max_age=max_age,
                            expires=expires, domain=settings.SESSION_COOKIE_DOMAIN,
                            path=settings.SESSION_COOKIE_PATH,
                            secure=settings.SESSION_COOKIE_SECURE or None,
                            httponly=settings.SESSION_COOKIE_HTTPONLY or None,
                            samesite=settings.SESSION_COOKIE_SAMESITE,
                    )
                    else:
                        response.set_cookie(
                            settings.SESSION_COOKIE_NAME,
                            request.session.session_key, max_age=max_age,
                            expires=expires, domain=settings.SESSION_COOKIE_DOMAIN,
                            path=settings.SESSION_COOKIE_PATH,
                            secure=settings.SESSION_COOKIE_SECURE or None,
                            httponly=settings.SESSION_COOKIE_HTTPONLY or None,
                            samesite=settings.SESSION_COOKIE_SAMESITE,
                        )

        return response


class CustomCsrfViewMiddleware(CsrfViewMiddleware):

    def _set_token(self, request, response):
        if settings.CSRF_USE_SESSIONS:
            if request.session.get(CSRF_SESSION_KEY) != request.META['CSRF_COOKIE']:
                request.session[CSRF_SESSION_KEY] = request.META['CSRF_COOKIE']
        else:
            if is_iframe(request):
                response.set_cookie(
                    settings.IFRAME_CSRF_COOKIE_NAME,
                    request.META['CSRF_COOKIE'],
                    max_age=settings.CSRF_COOKIE_AGE,
                    domain=settings.CSRF_COOKIE_DOMAIN,
                    path=settings.CSRF_COOKIE_PATH,
                    secure=settings.CSRF_COOKIE_SECURE,
                    httponly=settings.CSRF_COOKIE_HTTPONLY,
                    samesite=settings.CSRF_COOKIE_SAMESITE,
                )
            else:
                response.set_cookie(
                    settings.CSRF_COOKIE_NAME,
                    request.META['CSRF_COOKIE'],
                    max_age=settings.CSRF_COOKIE_AGE,
                    domain=settings.CSRF_COOKIE_DOMAIN,
                    path=settings.CSRF_COOKIE_PATH,
                    secure=settings.CSRF_COOKIE_SECURE,
                    httponly=settings.CSRF_COOKIE_HTTPONLY,
                    samesite=settings.CSRF_COOKIE_SAMESITE,
                )
            # Set the Vary header since content varies with the CSRF cookie.
            patch_vary_headers(response, ('Cookie',))


class IframeIsolationMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request = self.process_request(request)
        response = self.get_response(request)

        return response
    
    def _replace_cookie(self, request, original_name, name_to_replace):
        if request.COOKIES.get(name_to_replace): 
            request.COOKIES[original_name] = request.COOKIES.get(name_to_replace)
        else: 
            if request.COOKIES.get(original_name):
                del request.COOKIES[original_name]

    def process_request(self, request):
        if is_iframe(request):
            self._replace_cookie(request, settings.LANGUAGE_COOKIE_NAME, settings.IFRAME_LANGUAGE_COOKIE_NAME)
            self._replace_cookie(request, settings.CSRF_COOKIE_NAME, settings.IFRAME_CSRF_COOKIE_NAME)
            self._replace_cookie(request, settings.LANGUAGE_COOKIE_NAME, settings.IFRAME_LANGUAGE_COOKIE_NAME)
            self._replace_cookie(request, settings.SESSION_COOKIE_NAME, settings.IFRAME_SESSION_COOKIE_NAME)

        return request
    
            

