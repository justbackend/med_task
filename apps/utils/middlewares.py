from django.contrib.auth import get_user_model
from django.utils.deprecation import MiddlewareMixin

User = get_user_model()


class DummySession(dict):
    def save(self, *, must_create=False):
        pass

    def create(self):
        pass


class DisableSessionForAPIMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.path.startswith("/api/"):
            request.session = DummySession()
