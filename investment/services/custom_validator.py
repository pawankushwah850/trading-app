from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def PositiveQuantity(value):
    if value < 0:
        raise ValidationError(
            _("Asset quantity not be less then 0! %(value)"), params={'value': value}
        )
