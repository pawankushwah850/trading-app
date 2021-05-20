from django import template
from investment.models import Asset
import json

register = template.Library()

@register.filter(name="asset_price_per_unit")
def asset_price_per_unit(value):
    asset = {e.name: e.price for e in Asset.objects.filter(is_public=True)}
    return json.dumps(asset)
