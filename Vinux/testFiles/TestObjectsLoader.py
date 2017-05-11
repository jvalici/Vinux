from Vinux.models import  WineProducer, WineProductionArea, WineAppelation, WineDenomination, WineBottle, Comment
from Vinux.models import  WineCellar, StoredWineBottle, BottleUserReview, BottleWebReview, CommentImage
from django.contrib.auth.models import User
from PIL import Image
import os

def load_example_objects():
    
    wineProducer = WineProducer( companyName='G.A.E.C. Bret Brothers, la soufriandiere', country='France', postCode='71680', city='VINZELLES')
    wineProducer.save()
    
    wineProducer2 = WineProducer( companyName='Bret Brothers, la soufriandiere EARL', country='France', postCode='71680', city='VINZELLES')
    wineProducer2.save()
    
    bourgogne = WineProductionArea( name='Bourgogne' )
    bourgogne.save()
    
    maconnais = WineProductionArea( name='Maconnais', parentArea = bourgogne )
    maconnais.save()
    
    pf = WineAppelation(name='Pouilly Fuiss\u00E9', area=bourgogne, euStatus='AOP', isAOC=True)
    pf.save()
    pfec = WineDenomination.create('Pouilly-Fuiss\u00E9 En Carmentrant', pf)
    pfec.save()
    
    wineBottle = WineBottle( producer = wineProducer, denomination = pfec, vintage = 2015 )
    wineBottle.save()
    
    # when using this function for the base, there will be some user already. For the test, create one
    users = User.objects.all()
    if len( users ) > 0:
        test_user=users[0]
    else:
        test_user = User.objects.create_user(username='testuser', password='12345')
    
    c = Comment(comment = 'glou glou', user = test_user, content_object = wineBottle)
    c.save()
    
    dir_path = os.path.dirname(os.path.realpath(__file__))
    image_path = os.path.join(dir_path, 'testImageData', 'etiquette_3.jpg')
    i = CommentImage(comment = c, image = image_path)
    i.save()
    
    review = BottleUserReview( mark = 15,  pairing = 'avec du caca boudin', comment = c)
    review.save()

    webReview = BottleWebReview( bottle=wineBottle, link='http://www.bretbrothers.com/vin/pouilly-fuisse-en-carementrant-bret-brothers-85.php')
    webReview.save()
    
    cellar = WineCellar(owner=test_user)
    cellar.save()
    
    storedBottle = StoredWineBottle( vineCellar=cellar, bottle=wineBottle,priceIn = 12.90)
    storedBottle.save()
    
    return 0
    