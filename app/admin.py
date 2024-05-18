from django.contrib import admin

from app.models import Tag

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):

    # displays selected fields
    list_display = [
        'name',
    ]