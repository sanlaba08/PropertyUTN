import os

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


# Create your models here.
class City(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = 'Cities'

    def __str__(self):
        return self.name


def get_image_path(instance, filename):
    return os.path.join('photos', filename)


class Property(models.Model):
    city = models.ForeignKey(City, null=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=500)
    description = models.CharField(max_length=1000)
    maxPax = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    image = models.ImageField(upload_to=get_image_path, blank=True, null=False)
    dailyCost = models.DecimalField(max_digits=10, decimal_places=2)
    owner = models.ForeignKey(User, null=False, on_delete=models.SET('null'))

    class Meta:
        verbose_name_plural = 'Properties'

    def __str__(self):
        return self.title


class Reservation(models.Model):
    property = models.ForeignKey(Property, on_delete=models.PROTECT, blank=False, null=False)
    name = models.CharField(max_length=120)
    lastName = models.CharField(max_length=120)
    email = models.EmailField(max_length=200)
    date = models.DateField(default=timezone.now())
    totalCost = models.FloatField(validators=[MinValueValidator(0.0)], default=0.0)
    code = models.IntegerField()
    pax = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])

    class Meta:
        verbose_name_plural = 'Reservations'

    def __str__(self):
        return str(self.date.strftime("%Y-%m-%d"))


class RentalDate(models.Model):
    date = models.DateField()
    property = models.ForeignKey(Property, on_delete=models.PROTECT, blank=False, null=False)
    reservation = models.ForeignKey(Reservation, on_delete=models.PROTECT, null=True, blank=True)

    class Meta:
        verbose_name_plural = 'RentalDates'
        ordering = ('date', 'property')

    # def __str__(self):
    #     return str(self.date.strftime("%Y-%m-%d"))
