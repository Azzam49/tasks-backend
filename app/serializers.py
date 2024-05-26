from django.utils import timezone
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


class TaskCreateUpdateSerializer(serializers.ModelSerializer):
    # optional if want to make it more readable, as we are passing id values
    # also give ability to control if field is required or not on serializer level
    # serialzier level validation happens before the database level
    owner_id = serializers.CharField(
        max_length=10, required=False, allow_null=True)
    tag_id = serializers.CharField(
        max_length=10, required=False, allow_null=True)

    class Meta:
        model = Task
        fields = ['id', 'owner_id', 'title', 'description', 'tag_id', 'status']
        read_only_fields = ['id']

    def validate(self, attrs):
        # Add any additional validation here if needed
        title = attrs.get('title')
        #print(f"\ntitle : {title}\n")
        if len(title) > 90:
            raise serializers.ValidationError({"title": "Task title cannot be more than 90 characters."})
        return attrs

    def create(self, validated_data):
        # Perform any custom actions here if needed
        print(f"\nCreate, validated_data : {validated_data}\n")

        validated_data['created_at'] = timezone.now()

        # Call super to use the default create method
        return super().create(validated_data)

    def update(self, instance, validated_data):
        # Perform any custom actions here if needed
        print(f"\nUpdate, instance : {instance}")
        print(f"Update, validated_data : {validated_data}\n")

        # Call super to use the default update method
        return super().update(instance, validated_data)