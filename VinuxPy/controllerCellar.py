from django.http import HttpResponse
import json

def getTestJson(request):
    resList = {'vin1':'a','vin2':'b'}
    return HttpResponse(json.dumps(resList))
