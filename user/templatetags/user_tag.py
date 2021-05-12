from django import template
from django.contrib.auth import get_user_model
import json
register = template.Library()

@register.filter(name='user_lables_set')
def user_lables_set(value):
    User = get_user_model()
    data = [e.created_at.strftime('%D') for e in User.objects.all()]
    return json.dumps(list(set(data)))

