from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# home view
@login_required(login_url='/accounts/login/')
def homeView(request):
    return render(request, 'homeView.html',  {}, content_type='html')

