from django.contrib import admin

from . import models


@admin.register(models.NewsCategory)
class NewsCategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(models.EventCategory)
class EventCategoryAdmin(admin.ModelAdmin):
    pass
