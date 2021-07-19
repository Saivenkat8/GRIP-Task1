from django.db import models

# Create your models here.
class Customer(models.Model):
  name = models.CharField(max_length=100)
  email = models.EmailField(max_length=100)
  current_balance = models.FloatField()

  def __str__(self):
    return self.name

class Transaction(models.Model):
  sender_name = models.CharField(max_length=100)
  receiver_name = models.CharField(max_length=100)
  sender_email = models.CharField(max_length=100)
  receiver_email = models.CharField(max_length=100)
  amount_transfer = models.FloatField()

  def __str__(self):
    return str(self.id)
