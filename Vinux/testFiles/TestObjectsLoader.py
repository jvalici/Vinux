from Vinux.models import ContactInfo, WineProducer, WineProductionArea, WineType, WineBottle, WineCellar, StoredWineBottle, WineBottleReview

def loadExampleObjects():

    contactInfo = ContactInfo( 
        postalAdrress='125 rue aux Bourgeois, 1680 VINZELLES, FRANCE',
        email='contact@bretbrothers.com',
        webSiteAddress='http://www.bretbrothers.com',
        telephoneNumber = '+33 (0)3.85.35.67.72')
    contactInfo.save()
    
    wineProducer = WineProducer( name='Bret Brothers, la soufriandiere', contactInfo = contactInfo )
    wineProducer.save()
    
    wineProductionArea = WineProductionArea( name='Bourgundy')
    wineProductionArea.save()
    
    wineType = WineType( type='Pouilly Fuiss&eacute;', productionArea = wineProductionArea )
    wineType.save()
    
    wineBottle = WineBottle( producer = wineProducer, type = wineType, name = 'En Carementant', vintage = 2015 )
    wineBottle.save()
    return 0
    