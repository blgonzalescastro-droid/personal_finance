from rest_framework import serializers
from .models import Goal
from datetime import date

class GoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goal
        fields = '__all__'
        read_only_fields = ('user',)

    
    def validate_target_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("El monto de la meta debe ser mayor a 0.")
        return value

    
    def validate_target_date(self, value):
        if value < date.today():
            raise serializers.ValidationError("La fecha límite de la meta no puede estar en el pasado.")
        return value

    
    def validate(self, attrs):
        title = attrs.get('title', '')
        if len(title.strip()) < 3:
            raise serializers.ValidationError({"title": "El título de la meta debe tener al menos 3 caracteres."})
        return attrs