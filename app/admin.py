from django.contrib import admin

from app.models import (
    Tag,
    Task,
)

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):

    # displays selected fields
    list_display = [
        'name',
    ]

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'owner', 'title', 'description', 'tag', 'created_at', 'status')
    list_filter = ('status', 'created_at', 'tag')
    search_fields = ('title', 'description', 'owner__username')
    raw_id_fields = ('owner', 'tag')

# Alternatively, you can register the models using the `admin.site.register` method:

# admin.site.register(Tag, TagAdmin)
# admin.site.register(Task, TaskAdmin)