from rest_framework import serializers
from .models import Task

class TaskSerializer(serializers.ModelSerializer):
    # this first way
    # owner = serializers.ReadOnlyField(source='owner.username')  # To display owner's username instead of ID
    # other way to use SerializerMethodField as:
    owner = serializers.SerializerMethodField('get_owner')

    # To display tag's name instead of ID
    # this uses the __str__ of Tag model
    tag = serializers.StringRelatedField()

    # Custom field to format created_at
    # by default it looks for field name as ('get' + <field_name>), eg.get_created_at
    # can use argument to excplicty mention function name
    # created_at = serializers.SerializerMethodField()
    created_at = serializers.SerializerMethodField('get_created_at')

    class Meta:
        model = Task
        fields = ['id', 'owner', 'title', 'description', 'tag', 'created_at', 'status']

    def get_owner(self, obj):
        return obj.owner.username

    def get_created_at(self, obj):
        # return obj.created_at.date().isoformat()  # Convert datetime to date and format as YYYY-MM-DD
        return obj.created_at.strftime('%Y-%m-%d')  # Convert datetime to date and format as YYYY-MM-DD


class TaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'owner', 'title', 'description', 'tag', 'status']
        read_only_fields = ['id']

    def validate(self, attrs):
        # Add any additional validation here if needed
        title = attrs.get('title')
        print(f"\ntitle : {title}\n")
        if len(title) > 90:
            raise serializers.ValidationError({"title": "Task title cannot be more than 90 characters."})
        return attrs