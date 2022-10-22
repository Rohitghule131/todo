from rest_framework import serializers
from todo.models import ToDoTaskModel


class TaskSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)

    class Meta:
        fields = [
            'id',
            'user',
            'task',
            'status',
            'created_at',
            'estimated_time',
            'priority_level',
            'end_date_of_task',
            'task_complete_time',
            'start_date_of_task',
        ]
        model = ToDoTaskModel
