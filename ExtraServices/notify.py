from user.models import *


def Notify(message=None, category=None, user=None):
    instance = Notification.objects.create(message=message, category=category, user=user)
    instance.save()
