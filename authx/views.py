from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import AuthenticationFailed

from .jwt import create_jwt

from datetime import datetime, timedelta, timezone

User = get_user_model()


class LoginView(APIView):
    permission_classes = []
    authentication_classes = []

    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        user = User.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed(
                _('User not found'), code='user_not_found')
        if not user.check_password(password):
            raise AuthenticationFailed(
                _('Incorrect password'), code='user_wrong_password')
        if not user.is_active:
            raise AuthenticationFailed(
                _("User is inactive"), code="user_inactive")

        payload = {
            'id': user.id,
            'exp': datetime.now(timezone.utc) + timedelta(minutes=60),
            'iat': datetime.now(timezone.utc)
        }
        token = create_jwt(payload)
        return Response({'jwt': token})
