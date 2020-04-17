from django.db import models

# Create your models here.
#tables

class FuelPrices(models.Model):
    FUEL_TYPES = (
        (1, 'Petrol'),
        (2, 'Diesel'),
        (3, 'CNG')
    )

    id = models.AutoField(primary_key=True)
    state = models.AutoField(max_length=20)
    city = models.CharField(max_length=20)
    fuel_type = models.IntegerField(choices=FUEL_TYPES)
    price = models.FloatField(default=0)


