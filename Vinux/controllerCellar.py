from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from Vinux.models import  WineCellar, StoredWineBottle, WineDenomination, WineProductionArea, WineProducer, WineBottle, WineCellar, StoredWineBottle
from Vinux.modelsUtils import remove_special_chars
from datetime import datetime 

# home view
@login_required(login_url='/accounts/login/')
def cellarView(request):
    return render(request, 'cellarView.html',  {}, content_type='html')

# home view
@login_required(login_url='/accounts/login/')
def goneBottlesView(request):
    return render(request, 'goneBottlesView.html',  {}, content_type='html')


# get the bottles in the cellar of the user or those which used to be
def getCellarInOrGone(request, true_when_only_in_or_false_for_only_gone ):
    cellars = WineCellar.objects.filter(owner=request.user)
    # if the user has no cellar, create one
    if  len(cellars) == 0:
        cellar = WineCellar(owner=request.user)
        cellar.save()
    else:
        #ignore that a user could have several cellars and that len(cellars) could be >  0
        cellar = cellars[0]                                 
    resList = { 'bottles': [ {
                'id': str(s.id),
                'denomination':s.bottle.denomination.name,
                'vintage':s.bottle.vintage,
                'productionArea':s.bottle.denomination.appelation.area.name,
                'producer':s.bottle.producer.companyName,
                'name':s.bottle.name,
                'priceIn':s.priceIn,
                'additionDate':s.additionDate.strftime('%d-%m-%Y'),
                'removalDate': '' if (s.removalDate is  None) else s.removalDate.strftime('%d-%m-%Y'),
               } for s in StoredWineBottle.objects.filter(vineCellar=cellar, removalDate__isnull=true_when_only_in_or_false_for_only_gone) ] }
    return JsonResponse(resList)


# get the bottles in the cellar of the user
@login_required(login_url='/accounts/login/')
def getCellar(request):
    return getCellarInOrGone(request, True)

# get the bottles in the cellar of the user
@login_required(login_url='/accounts/login/')
def getGoneBottles(request):
    return getCellarInOrGone(request, False)

# home view
@login_required(login_url='/accounts/login/')
def getDenominations(request):
    hint = remove_special_chars( request.GET['hint'] )
    denoms = WineDenomination.objects.filter(searchName__icontains=hint)
    tmp = [{ 'id':d.id, 'label':d.name } for d in denoms]
    resList = { 'denoms': tmp  }
    return JsonResponse(resList)

# get all the producers 
@login_required(login_url='/accounts/login/')
def getProducers(request):
    hint = remove_special_chars( request.GET['hint'] )
    producers = WineProducer.objects.filter(searchName__icontains=hint)
    resList = { 'prods': [ { 'id':p.id, 'label':p.companyName } for p in producers ] }
    return JsonResponse(resList)

# add a bottle to the cellar
@login_required(login_url='/accounts/login/')
def addBottle(request):
    denomination_id = request.POST['denomination_id']
    producer_id = request.POST['producer_id']
    price = float(request.POST['price'])
    vintage = int(request.POST['vintage'])
    if 'name' in request.POST:
        has_a_name = True
        name = request.POST['name']
        bottles = WineBottle.objects.filter( producer__id = producer_id, denomination__id = denomination_id, name = name, vintage = vintage )
    else:
        has_a_name =  False
        bottles = WineBottle.objects.filter( producer__id = producer_id, denomination__id = denomination_id, vintage = vintage )
    if len(bottles) != 1:
        producer = WineProducer.objects.get(id = producer_id)
        denom = WineDenomination.objects.get(id = denomination_id)
        if has_a_name:
            b = WineBottle( producer = producer, denomination = denom, name = name, vintage = vintage )
        else:
            b = WineBottle( producer = producer, denomination = denom, vintage = vintage )
        b.save()
    else:
        b = bottles[0]
    cellars = WineCellar.objects.filter( owner = request.user )
    if len(cellars) != 1:
        cellar = WineCellar(owner = request.user )
        cellar.save()
    else:
        cellar = cellars[0]
    nb = StoredWineBottle(vineCellar=cellar, bottle=b, priceIn=price)
    nb.save()
    return redirect('/Vinux/getCellar')


@login_required(login_url='/accounts/login/')
def removeBottle(request):
    bottle_ids = request.POST.getlist('bottle_ids')
    for b in bottle_ids:
        b = StoredWineBottle.objects.get( id=int(b) )
        b.removalDate = datetime.now()
        b.save()
    return redirect('/Vinux/getGoneBottles')

@login_required(login_url='/accounts/login/')
def deleteBottle(request):
    bottle_ids = request.POST.getlist('bottle_ids')
    for b in bottle_ids:
        b = StoredWineBottle.objects.get( id=int(b) )
        b.delete()
    return redirect('/Vinux/getGoneBottles')
     