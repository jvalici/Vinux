from django.http import HttpResponse
from django.shortcuts import render
import json


# test
def getTestJson(request):
    resList = {'vin1':'a','vin2':'b'}
    return HttpResponse(json.dumps(resList))


# test
def testView(request):
    return render(request, 'test.html',  {'vin1':'a','vin2':'b'} , content_type='html')


# test
def testTicTacToe(request):
    return render(request, 'ticTacToe.html',  {}, content_type='html')