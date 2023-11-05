from django.contrib.auth import get_user_model
from rest_framework.serializers import ModelSerializer
from rest_framework.exceptions import ValidationError

User = get_user_model()


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        try:
            print(validated_data, flush=True)
            username = validated_data.pop('username', None)
            password = validated_data.pop('password', None)
            email = validated_data.pop('email', None)
            return User.objects.create_user(username=username, password=password, email=email)
        except (ValidationError, ValueError) as e:
            raise ValidationError(f"{e}")
