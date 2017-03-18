from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from Vinux.models import  WineCellar, StoredWineBottle

# home view
@login_required(login_url='/accounts/login/')
def homeView(request):
    return render(request, 'homeView.html',  {}, content_type='html')


# home view
@login_required(login_url='/accounts/login/')
def getCellar(request):
    cellars = WineCellar.objects.filter(owner=request.user)
    # if the user has no cellar, create one
    if  len(cellars) == 0:
        cellar = WineCellar(owner=request.user)
        cellar.save()
    else:
        #ignore that a user could have several cellars and that len(cellars) could be >  0
        cellar = cellars[0]
    storedWineBottles = StoredWineBottle.objects.filter(vineCellar=cellar)                                  
    resList = { 'storedWineBottles': [ {
                'appelation':s.bottle.type.appelation,
                'color':s.bottle.type.color,
                'productionArea':s.bottle.type.productionArea.name,
                'producer':s.bottle.producer.name,
                'name':s.bottle.name
               } for s in storedWineBottles ] }
    return JsonResponse(resList)

