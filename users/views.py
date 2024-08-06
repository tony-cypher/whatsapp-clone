from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import RegistrationForm

# Create your views here.
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.save()
            login(request, new_user)
            return redirect('home')
    else:
        form = RegistrationForm()
    return render(request, 'users/register.html', {'form':form})