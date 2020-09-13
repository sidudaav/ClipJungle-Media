from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token

######################## BASIC FIND USER FUNCTIONS ########################
def get_user_by_email(email):
    try:
        return User.objects.get(email=email)
    except User.DoesNotExist:
        return None

def get_user_by_username(username):
    try:
        return User.objects.get(username=username)
    except User.DoesNotExist:
        return None


###################### EMAIL FUNCTIONS ##########################
def send_verification_email(domain, id):
    user = get_object_or_404(User, id=id)

    email_subject = 'Activate your ClipJungle account.'
    email_body = render_to_string('profiles/activation_email.html', {
    'user': user,
    'domain': domain,
    'uid':urlsafe_base64_encode(force_bytes(user.id)),
    'token':account_activation_token.make_token(user),
    })

    email = EmailMessage(
            email_subject, email_body, to=[user.email]
    )

    email.send()