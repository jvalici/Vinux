from Vinux.models import ContactInfo, WineProducer, WineProductionArea, WineType, WineBottle, WineCellar, StoredWineBottle, BottleUserReview, BottleWebReview
from django.contrib.auth.models import User

def loadExampleObjects():

    contactInfo = ContactInfo( 
        postalAdrress='125 rue aux Bourgeois, 1680 VINZELLES, FRANCE',
        email='contact@bretbrothers.com',
        webSiteAddress='http://www.bretbrothers.com',
        telephoneNumber = '+33 (0)3.85.35.67.72')
    contactInfo.save()
    
    wineProducer = WineProducer( name='Bret Brothers, la soufriandiere', contactInfo=contactInfo )
    wineProducer.save()
    
    france = WineProductionArea( name='France')
    france.save()
    
    bourgogne = WineProductionArea( name='Bourgundy', includingArea = france )
    bourgogne.save()
    
    pouilly = WineType( appelation='Pouilly Fuiss&eacute;', color='b',  productionArea = bourgogne )
    pouilly.save()
    
    genericBlanc = WineType( appelation='Generique', color='b',  productionArea = bourgogne )
    genericBlanc.save()

    wineBottle = WineBottle( producer = wineProducer, type = pouilly, name = 'En Carementant', vintage = 2015 )
    wineBottle.save()
    
    users = User.objects.all()
    review = BottleUserReview( user=users[0], bottle = wineBottle,  mark = 15,  pairing = 'avec du caca boudin', comment = 'Demander a francois comment va le fragin mort' )
    review.save()
    
    webReview = BottleWebReview( bottle=wineBottle, link='http://www.bretbrothers.com/vin/pouilly-fuisse-en-carementrant-bret-brothers-85.php')
    webReview.save()
    
    cellar = WineCellar(owner=users[0])
    cellar.save()
    
    storedBottle = StoredWineBottle( vineCellar=cellar, bottle=wineBottle,priceIn = 12.90)
    storedBottle.save()
    
    return 0
    