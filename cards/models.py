from django.db import models
from django.contrib.auth.models import User

class Card(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cards')
    card_number = models.CharField(max_length=16)
    card_holder = models.CharField(max_length=100)
    expire_date = models.CharField(max_length=5) # MM/YY
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    weekly_limit = models.DecimalField(max_digits=10, decimal_places=2, default=4000.0)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.card_holder} - {self.card_number[-4:]}"