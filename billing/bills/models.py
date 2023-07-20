import datetime

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


# Create your models here.
class Profile(models.Model):
    pass


class Item(models.Model):
    category = models.CharField(max_length=255, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    asa_code = models.CharField(max_length=20, blank=True, null=True)
    asa_units = models.IntegerField()
    mbs_code = models.CharField(max_length=20, blank=True, null=True)
    mbs_units = models.IntegerField()
    year = models.IntegerField(
        validators=[MinValueValidator(1900), MaxValueValidator(datetime.date.today().year + 1)],
        default=datetime.date.today().year,
        blank=True,
        null=True,
    )


class Case(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    initials = models.CharField(max_length=10)
    dob = models.DateField()
    procedure = models.CharField(max_length=255)
    items = models.ManyToManyField(Item)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    processed = models.DateTimeField(blank=True, null=True)
