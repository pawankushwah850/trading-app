from django import template
from django.contrib.auth import get_user_model
import json
from collections import Counter

register = template.Library()


@register.filter(name='user_data_set')
def user_data_set(value):
    User = get_user_model()
    data = list(Counter([e.created_at.strftime('%D') for e in User.objects.all()]).items())
    data.sort(key=lambda x: x[0])
    return json.dumps(data)


@register.filter(name='verified_users')
def verified_users(value):
    User = get_user_model()
    instance = User.objects.all()
    data = {
        'total_user': instance.count(),
        'verified_user': instance.filter(verification_status=True).count(),
        'unverified_user': instance.filter(verification_status=False).count()
    }

    return json.dumps(data)
