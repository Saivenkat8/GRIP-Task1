from django.core.management.base import BaseCommand
from faker import Faker
from basicbankingsystem.models import Customer
import random

class Command(BaseCommand):
  help = "To Create Customers"

  def handle(self, *args, **kwargs):
    self.stdout.write("Deleting old data...")
    Customer.objects.all().delete()
    self.stdout.write("Creating new data...")
    fake = Faker()
    for _ in range(10):
      name = fake.name()
      email = fake.email()
      Customer.objects.create(
        name=name,
        email=email,
        current_balance=(round(random.uniform(100.99, 5000.99), 2)),
      )
