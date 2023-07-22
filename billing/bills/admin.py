from django.contrib import admin

from . import models


@admin.register(models.Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("name", "user")


@admin.register(models.Edition)
class EditionAdmin(admin.ModelAdmin):
    list_display = ("name", "current")


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(models.ItemGroup)
class ItemGroupAdmin(admin.ModelAdmin):
    list_display = ("description",)


@admin.register(models.Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ("scheme", "code", "description", "units")
    list_filter = ("scheme", "edition")
    search_field = ("code",)


@admin.register(models.Case)
class CaseAdmin(admin.ModelAdmin):
    list_display = ("date", "procedure", "profile")
    list_filter = ("profile",)
