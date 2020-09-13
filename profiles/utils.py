from django.contrib.auth.models import User

######################## BASIC FIND USER FUNCTIONS ########################
def get_user_by_email(email):
    try:
        return User.objects.get(email=email.capitalize())
    except User.DoesNotExist:
        return None

def get_user_by_username(username):
    try:
        return User.objects.get(username=username)
    except User.DoesNotExist:
        return None