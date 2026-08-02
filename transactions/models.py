from django.db import models
from django.contrib.auth.models import User

class Transaction(models.Model):
    CATEGORY_CHOICES = [
        ('Shopping', 'Shopping'),
        ('Electronics', 'Electronics'),
        ('Travels', 'Travels'),
        ('Food', 'Food'),
        ('Sport', 'Sport'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
    receiver = models.CharField(max_length=100)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.receiver} - ${self.amount}"