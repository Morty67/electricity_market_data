from django.db import models

from energy_market.utils.date_validator import validate_date_format


class MarketClosingData(models.Model):
    date = models.CharField(max_length=10, validators=[validate_date_format])
    hour = models.CharField(max_length=5)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    volume = models.DecimalField(max_digits=10, decimal_places=1)

    def __str__(self):
        return f"MarketClosingData: {self.date} {self.hour}"
