from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm

def register(request):
    '''registration page for new users'''
    if request.method != 'POST':
        # render a blank form for users to register
        form = UserCreationForm()
    else:
        # create a form with users data behind the scene
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            new_user = form.save()
            # log in the user before redirect back to home page
            # note that login() takes in request as a default argument
            login(request, new_user)
            return redirect('learning_logs:index')
    
    # render a blank form or form errors
    context = {'form': form}
    return render(request, 'registration/register.html', context)
