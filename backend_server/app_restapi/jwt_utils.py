from app_restapi.serializers import UserSerializer
from django.utils import timezone
from app_restapi.models import UserLogin


def update_user_login(user):
    user.userlogin_set.create(timestamp=timezone.now())
    user.save()


def jwt_response_payload_handler(token, user=None, request=None):
    update_user_login(user)
    login_count = len(UserLogin.objects.filter(user=user))

    return {
        'token': token,
        'user': UserSerializer(user).data,
        'user_group': [x.name for x in user.groups.all()],
        'login_count': login_count,
    }
