from django.http import HttpResponse
from django.shortcuts import render
import json
from django.contrib.auth.decorators import login_required

# home view
@login_required(login_url='/accounts/login/')
def homeView(request):
    return render(request, 'homeView.html',  {}, content_type='html')

# test json
def testJson(request):
    resList = {'vin1':'a','vin2':'b'}
    return HttpResponse(json.dumps(resList))

# test html render
def testTicTacToe(request):
    return render(request, 'ticTacToe.html',  {}, content_type='html')