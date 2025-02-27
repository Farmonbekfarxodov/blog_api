from django.utils.timezone import now
from django.contrib.auth import get_user_model

User = get_user_model()

class UpdateLastActivityMiddleware:
    """Har safar so‘rov yuborilganda foydalanuvchi faoliyatini yangilash"""
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            user = request.user
            user.last_activity = now()
            user.save(update_fields=['last_activity'])

        return self.get_response(request)
