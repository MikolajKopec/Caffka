from typing import Any
from django.contrib.auth import get_user_model
from django.utils.timezone import now

User = get_user_model()


class SetLastUserLoggin(object):

    def __init__(self, get_response) -> None:
        self.get_response = get_response

    def __call__(self, request) -> None:
        if request.user.is_authenticated:
            user = User.objects.get(id=request.user.id)
            user.last_login = now()
            user.save()
        return self.get_response(request)
