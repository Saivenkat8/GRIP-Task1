from django import forms
from .models import Transaction, Customer
from django.contrib import messages

class TransactionForm(forms.ModelForm):
  class Meta:
    model = Transaction
    fields = ['sender_name', 'receiver_name', 'amount_transfer']

  def clean(self):
    cleaned_data = super().clean()
    sender_name = cleaned_data.get('sender_name')
    receiver_name = cleaned_data.get('receiver_name')
    transfer_amount = cleaned_data.get('amount_transfer')
    try:
      user_amount = Customer.objects.get(name=sender_name).current_balance
    except:
      user_amount = None

    if not Customer.objects.filter(name=sender_name).count():
      raise forms.ValidationError("Please fill all the fields correctly")

    if not Customer.objects.filter(name=receiver_name).count():
      raise forms.ValidationError("Please fill all the fields correctly")

    if not transfer_amount:
      raise forms.ValidationError("Please provide the amount to be transferred")

    if transfer_amount and transfer_amount <= 0:
      raise forms.ValidationError("Amount to be transferred cannont be less than or equal to 0")

    if transfer_amount and user_amount and user_amount < transfer_amount:
      raise forms.ValidationError(("Amount to be transferred (%(transfer_amount)s) exceeds %(sender_name)s's current balance (%(user_amount)s)"),
        params={'transfer_amount': transfer_amount,
                'user_amount': user_amount,
                'sender_name': sender_name}
                )

  def save(self, commit=True):
    transaction = super(TransactionForm, self).save(commit=False)
    sender = self.cleaned_data.get('sender_name')
    transaction.sender_email = Customer.objects.get(name=sender).email
    receiver = self.cleaned_data.get('receiver_name')
    transaction.receiver_email = Customer.objects.get(name=receiver).email
    amount_transfer = self.cleaned_data.get('amount_transfer')
    sender_name = Customer.objects.get(name=sender)
    sender_current_balance = sender_name.current_balance
    sender_name.current_balance = sender_current_balance - float(amount_transfer)
    sender_name.save()
    receiver_name = Customer.objects.get(name=receiver)
    receiver_current_balance = receiver_name.current_balance
    receiver_name.current_balance = receiver_current_balance + float(amount_transfer)
    receiver_name.save()
    if commit:
      transaction.save()
    return transaction
