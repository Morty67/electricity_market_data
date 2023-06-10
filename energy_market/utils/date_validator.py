from datetime import datetime

from django.core.exceptions import ValidationError


def validate_date_format(value):
    try:
        datetime.strptime(value, "%d.%m.%Y")
    except ValueError:
        raise ValidationError(
            "Invalid date format. Use the format 'dd.mm.yyyy'."
        )
