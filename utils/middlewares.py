from django.conf import settings
from django.contrib.sessions.middleware import SessionMiddleware
from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponseForbidden

class DummySession(dict):
    def save(self, must_create=False):
        pass  # Do nothing when saving

    def create(self):
        pass  # Do nothing when creating a session

class DisableSessionForAPIMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # Check if the request is for the API
        if request.path.startswith('/api/'):
            # Replace the session with a dummy session
            request.session = DummySession()

        return None
