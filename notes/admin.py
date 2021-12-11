from django.contrib import admin

from . import models

@admin.register(models.Notes)
class Notes(admin.ModelAdmin):
    list_display = ('user', 'noteName')