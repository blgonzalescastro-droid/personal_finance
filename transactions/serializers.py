from rest_framework import serializers
from .models import Transaction

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'
        read_only_fields = ('user', 'date')

    
    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("El monto de la transacción debe ser mayor a 0.")
        return value

    
    def validate(self, attrs):
        if attrs.get('receiver') == "":
            raise serializers.ValidationError({"receiver": "El receptor no puede estar vacío."})
        return attrs