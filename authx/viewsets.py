from django.core.mail import EmailMessage
from django.contrib.auth import get_user_model, logout
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.translation import gettext_lazy as _
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.response import Response


from authx.permissions import IsOwnerUser
from .serializers import UserSerializer

User = get_user_model()


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsOwnerUser]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        logout(request)
        self.perform_destroy(instance)
        return Response(status=HTTP_204_NO_CONTENT)

    def send_auth_email(self, user):
        current_site = get_current_site(self.request)
        domain = current_site.domain
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        mail_subject = _("Actuvate your blog account.")
        protocol = "http"
        url = f"{protocol}://{domain}/rest-api/v1/authx/activate/{uid}/{token}"
        message = f"<p>Click on link to actiavate your account - <a href='{url}'>{url}</a></p>"
        email = EmailMessage(mail_subject, message, to=[user.email])
        email.content_subtype
        email.send()

    def perform_create(self, serializer):
        user = serializer.save()
        self.send_auth_email(user)


class ActivationUserEmailView(APIView):
    permission_classes = []
    authentication_classes = []

    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return Response(_('Thank you for your email confirmation. Now you can log in your account.'))
        else:
            return Response(_('Activation link is invalid!'), status=HTTP_204_NO_CONTENT)
