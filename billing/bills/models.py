from datetime import date, datetime, timedelta

from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone


class Profile(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True, related_name="profile"
    )

    def __str__(self):
        return self.name


class Edition(models.Model):
    name = models.CharField(max_length=255)
    current = models.BooleanField(default=False, verbose_name="Set this as the current Edition")

    def reset_current_edition(self):
        # Set all Edition.current to False
        Edition.objects.all().update(current=False)

    def save(self, *args, **kwargs):
        if self.current:  # Ensure only one Edition.current == True
            self.reset_current_edition()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class EquivalentItem(models.Model):
    description = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return f"Group: {self.description}"


class Item(models.Model):
    ASA = "AS"
    MBS = "MB"
    SCHEME_CHOICES = [
        (ASA, "ASA Relative Value Guide"),
        (MBS, "Medicare Benefits Scheme"),
    ]

    scheme = models.CharField(
        max_length=2,
        choices=SCHEME_CHOICES,
        default=ASA,
    )

    BASIC = "BA"
    TIME = "TI"
    MOD = "MO"
    EXTRA = "EX"
    ITEM_TYPE_CHOICES = [
        (BASIC, "Basic Unit"),
        (TIME, "Time Unit"),
        (MOD, "Modifying Unit"),
        (EXTRA, "Therapeutic or Diagnostic Unit"),
    ]

    item_type = models.CharField(
        max_length=2,
        choices=ITEM_TYPE_CHOICES,
        default=BASIC,
    )

    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)
    description = models.CharField(max_length=255)
    code = models.CharField(max_length=20)
    units = models.IntegerField(blank=True, null=True)
    edition = models.ForeignKey(Edition, on_delete=models.CASCADE, blank=True, null=True)
    equivalent_items = models.ForeignKey(
        EquivalentItem, on_delete=models.CASCADE, related_name="items", blank=True, null=True
    )
    duplicate_allowed = models.BooleanField(
        default=False, help_text="Used to determine whether multiple of this item can be claimed per case"
    )

    @classmethod
    def search(cls, query, scheme=ASA, category=None):
        objects = cls.objects.filter(scheme=scheme)
        if category:
            objects = objects.filter(category=category)
        return objects.filter(models.Q(description__icontains=query) | models.Q(code__icontains=query))

    @classmethod
    def get_base_items(cls, scheme=ASA):
        return cls.objects.filter(scheme=scheme, item_type=cls.BASIC)

    @classmethod
    def get_modifier_items(cls, scheme=ASA):
        return cls.objects.filter(scheme=scheme, item_type=cls.MOD)

    @classmethod
    def get_extra_items(cls, scheme=ASA):
        return cls.objects.filter(scheme=scheme, item_type=cls.EXTRA)

    def __str__(self):
        return f"{self.code}: {self.description}"


class Case(models.Model):
    MONTHS = "MO"
    YEARS = "YE"
    AGE_UNIT_CHOICES = [
        (MONTHS, "Months"),
        (YEARS, "Years"),
    ]

    date = models.DateTimeField(default=timezone.now, verbose_name="Procedure date")
    age = models.PositiveIntegerField(
        validators=[
            MinValueValidator(0, message="Age must be a positive number or zero."),
            MaxValueValidator(150, message="Age cannot exceed 150."),
        ]
    )
    age_unit = models.CharField(max_length=2, choices=AGE_UNIT_CHOICES, default=YEARS)
    procedure = models.CharField(max_length=255, verbose_name="Procedure details")
    start = models.TimeField(verbose_name="Case start time")
    end = models.TimeField(verbose_name="Case end time")
    items = models.ManyToManyField(Item)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="cases")
    processed = models.DateTimeField(blank=True, null=True, verbose_name="The date this bill was processed")
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def calc_case_duration(self):
        pass

    def calc_time_delta(self):
        start_datetime = datetime.combine(date.min, self.start)
        end_datetime = datetime.combine(date.min, self.end)
        if end_datetime < start_datetime:
            end_datetime = end_datetime + timedelta(hours=24)
        return end_datetime - start_datetime

    def assign_time_item(self, scheme=Item.ASA):
        time_item_numbers = list(Item.filter(scheme=scheme, item_type=Item.TIME).order_by("-code"))
        duration = self.calc_time_delta()

        # Time item numbers increment 15 minutely for the first 2 hours, then 10 minutely
        index = 0
        time_counter = timedelta(minutes=0)
        while time_counter < duration:
            if time_counter < timedelta(hours=2):
                time_counter += timedelta(minutes=15)
            else:
                time_counter += timedelta(minutes=10)
            index += 1

        return time_item_numbers[index]

    def total_units(self):
        return self.items.aggregate(total_units=models.Sum("units"))["total_units"] or 0

    def __str__(self):
        return f"{self.procedure} on {self.date:%d-%m-%Y}"
