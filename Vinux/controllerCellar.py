from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from Vinux.models import  WineCellar, StoredWineBottle, WineDenomination, WineProductionArea, WineProducer, WineBottle, WineCellar, StoredWineBottle
from Vinux.models import  UserComment, BottleUserReview, ProducerUserReview
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
                'underlying_id': str(s.bottle.id),
                'denomination':s.bottle.denomination.name,
                'vintage':s.bottle.vintage,
                'productionArea':s.bottle.denomination.appelation.area.name,
                'producer':s.bottle.producer.companyName,
                'producer_id':s.bottle.producer.id,
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
    price = None if request.POST['price'] =='' else float(request.POST['price'])
    vintage = int(request.POST['vintage'])
    name = None if request.POST['name'] == '' else request.POST['name']
    bottles = WineBottle.objects.filter( producer__id = producer_id, denomination__id = denomination_id, name = name, vintage = vintage )

    if len(bottles) != 1:
        producer = WineProducer.objects.get(id = producer_id)
        denom = WineDenomination.objects.get(id = denomination_id)
        b = WineBottle( producer = producer, denomination = denom, name = name, vintage = vintage )
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
def addTheSameBottle(request):
    bottle_id = request.POST['bottle_id']
    b = StoredWineBottle.objects.get( id=bottle_id )
    nb = StoredWineBottle(vineCellar=b.vineCellar, bottle=b.bottle, priceIn=b.priceIn)
    nb.save()
    return redirect('/Vinux/getCellar')

@login_required(login_url='/accounts/login/')
def deleteBottle(request):
    bottle_ids = request.POST.getlist('bottle_ids')
    for b in bottle_ids:
        b = StoredWineBottle.objects.get( id=int(b) )
        b.delete()
    return redirect('/Vinux/getGoneBottles')
     
@login_required(login_url='/accounts/login/')
def commentProducer(request):
    producer_id = request.POST['producer_id']
    producer = WineProducer.objects.get(id = producer_id)
    c = UserComment( comment = request.POST['comment'], author = request.user )
    c.save()
    mark = None if request.POST['mark'] == '' else request.POST['mark']
    pc = ProducerUserReview( comment = c, producer = producer, mark = mark)
    pc.save()
    return JsonResponse({})


@login_required(login_url='/accounts/login/')
def commentBottle(request):
    bottle_id = request.POST['bottle_id']
    bottle = WineBottle.objects.get(id = bottle_id)
    c = UserComment( comment = request.POST['comment'], author = request.user )
    c.save()
    mark = None if request.POST['mark'] == '' else request.POST['mark']
    pairing = None if request.POST['pairing'] == '' else request.POST['pairing']
    flavor = None if request.POST['flavor'] == '' else request.POST['flavor']
    bc = BottleUserReview( comment = c, bottle = bottle, mark = mark, pairing = pairing, flavor = flavor)
    bc.save()
    return JsonResponse({})

# get all the comments 
@login_required(login_url='/accounts/login/')
def getComments(request):
    producer_id=remove_special_chars( request.GET['producer_id'] )
    producer = WineProducer.objects.get(id = producer_id)
    producerComments = ProducerUserReview.objects.filter(producer=producer)
    producerCommentList =  [ {
        'comment_id':c.comment.id,
        'comment':c.comment.comment,
        'author':c.comment.author.username,
        'mark':'' if c.mark is None else c.mark,
        'date':c.comment.commentDate.strftime('%d-%m-%Y'),
        'is_from_user':c.comment.author.id== request.user.id
        } for c in producerComments ]
    bottle_id=remove_special_chars( request.GET['bottle_id'] )
    bottle = WineBottle.objects.get(id = bottle_id)
    bottleComments = BottleUserReview.objects.filter(bottle=bottle)
    bottleCommentList =  [ {
        'comment_id':b.comment.id,
        'comment':b.comment.comment,
        'author':b.comment.author.username,
        'mark':'' if b.mark is None else b.mark,
        'pairing':'' if b.pairing is None else b.pairing,
        'flavor':'' if b.flavor is None else b.flavor,
        'date':b.comment.commentDate.strftime('%d-%m-%Y'),
        'is_from_user':b.comment.author.id== request.user.id
        } for b in bottleComments ]
    return JsonResponse( { 'producerComments': producerCommentList, 'bottleComments':bottleCommentList } )

@login_required(login_url='/accounts/login/')
def deleteSelectedComments(request):
    comment_ids = request.POST.getlist('comment_ids')
    for c in comment_ids:
        c = UserComment.objects.get( id=int(c) )
        if c.author == request.user: 
            c.delete()
    return JsonResponse({})

