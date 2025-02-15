import random
from django.core.mail import send_mail
from django.conf import settings

def generate_verification_code():
    """ 6 xonali tasdiqlash kodi yaratish """
    return str(random.randint(100000, 999999))

def send_verification_email(email, code):
    """ Emailga tasdiqlash kodini yuborish """
    subject = "Email Tasdiqlash Kodingiz"
    message = f"Sizning tasdiqlash kodingiz: {code}"
    sender_email = settings.EMAIL_HOST_USER

    send_mail(subject, message, sender_email, [email])
