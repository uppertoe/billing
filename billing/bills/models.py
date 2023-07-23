from django.conf import settings
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


class ItemGroup(models.Model):
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
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)
    description = models.CharField(max_length=255)
    code = models.CharField(max_length=20)
    units = models.IntegerField(blank=True, null=True)
    edition = models.ForeignKey(Edition, on_delete=models.CASCADE, blank=True, null=True)
    item_group = models.ForeignKey(ItemGroup, on_delete=models.CASCADE, related_name="items", blank=True, null=True)
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
        return cls.objects.filter(scheme=scheme, category__name="Base")

    @classmethod
    def get_procedures(cls, scheme=ASA):
        return cls.objects.filter(scheme=scheme, category__name="Procedures")

    @classmethod
    def get_modifiers(cls, scheme=ASA):
        return cls.objects.filter(scheme=scheme, category__name="Modifiers")

    def __str__(self):
        return f"{self.code}: {self.description}"


class Case(models.Model):
    date = models.DateTimeField(default=timezone.now, verbose_name="Procedure date")
    initials = models.CharField(max_length=10, verbose_name="Patient initials")
    dob = models.DateField(verbose_name="Patient date of birth")
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

    def assign_time_item(self):
        pass

    def __str__(self):
        return f"{self.procedure} on {self.date:%d-%m-%Y}"
