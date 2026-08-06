from rest_framework import serializers
from .models import Card
import re

class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = '__all__'
        read_only_fields = ('user',)

    def validate_card_number(self, value):
        if not re.fullmatch(r'\d{16}', value):
            raise serializers.ValidationError("El número de tarjeta debe tener 16 dígitos.")
        return value

    def validate_expire_date(self, value):
        if not re.fullmatch(r'(0[1-9]|1[0-2])/\d{2}', value):
            raise serializers.ValidationError("La fecha de expiración debe tener el formato MM/YY.")
        return value

    def validate_weekly_limit(self, value):
        if value <= 0:
            raise serializers.ValidationError("El límite semanal debe ser mayor a 0.")
        return value
