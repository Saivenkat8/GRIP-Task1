from django.shortcuts import render, redirect
from .models import Customer, Transaction
from .forms import TransactionForm
from django.contrib import messages

# Create your views here.
def home(request):
  args = {}
  customers = Customer.objects.all
  if request.method == "POST":
    form = TransactionForm(request.POST or None)
    if form.is_valid():
      form.save()
      messages.success(request, "Your Transaction was successful")
      return redirect('transaction')
  else:
    form = TransactionForm()
  args['form'] = form
  args['customers'] = customers
  return render(request, 'home.html', args)

def customers(request):
  customers = Customer.objects.all
  return render(request, 'customers.html', {'customers': customers})

def transaction(request):
  if(Transaction.objects):
    transactions = Transaction.objects.all
    return render(request, 'transaction.html', {'transactions': transactions})
  else:
    return render(request, 'transaction.html', {'transactions': None})
