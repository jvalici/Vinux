from Vinux.models import  WineProducer, WineProductionArea, WineAppelation, WineDenomination
import os

def init_data_base_with_known_objects():
    
    path_to_files = os.path.dirname(os.path.realpath(__file__))
    path_to_files = os.path.join(path_to_files, '..', '..', 'DataCollecting', 'output')
    
    #area
    path_to_arreas = os.path.join(path_to_files, 'regions_perso.txt')
    arreas = open(path_to_arreas, "r")
    for a in arreas:
        if a != '':
            pos = a.find(';')
            parentAreaStr = a[pos+1:len(a)-1].lower()#-1 for the \n character
            if parentAreaStr == 'na':
                wpa = WineProductionArea( name = a[:pos] )
            else:
                parentArea = WineProductionArea.objects.get(name__iexact = parentAreaStr)
                wpa = WineProductionArea( name = a[:pos].title(), parentArea = parentArea)
            wpa.save()
    
    # appellation
    path_to_appelations = os.path.join(path_to_files, 'appelations_inao.txt')
    appelations = open(path_to_appelations, "r")
    errors_path = os.path.join(path_to_files, 'denominations_inao_errors2.txt')
    errors = open(errors_path, "w")
    for a in appelations:
        if a != '':
            alc = a[:len(a)-1].lower()# - 1 to remove \n
            aop_igp = 'i' if ( alc.find('igp') > -1) else 'a'
            is_aoc = alc.find('aoc ') > -1
            pos1 = alc.find(';')
            pos2 = alc.find(';', pos1 + 1)
            area_name = alc[ pos2+1:]
            try:
                area = WineProductionArea.objects.get(name__iexact = area_name)
            except:
                errors.write(area_name+'\n')
            app = WineAppelation( name= a[:pos1].title(), area=area, euStatus = aop_igp, isAOC=is_aoc)
            app.save()
        
    # denomination
    path_to_denominations = os.path.join(path_to_files, 'denominations_inao.txt')
    denominations = open(path_to_denominations, "r")
    for d in denominations:
        if d != '':
            dlc = d.lower()
            pos1 = d.find(';')
            pos2 = d.find(';', pos1 + 1)
            pos3 = d.find(';', pos2 + 1)
            pos4 = d.find(';', pos3 + 1)
            pos5 = d.find(';', pos4 + 1)
            pos6 = d.find(';', pos5 + 1)
            appelation_name = dlc[pos5+1:pos6]
            try:
                app = WineAppelation.objects.get(name__iexact = appelation_name)
            except:
                errors.write('appelation_name: '+appelation_name+'-----'+d)
            den = WineDenomination.create( name=d[:pos1].title(), appelation=app)
            den.save()
            
    path_to_growers = os.path.join(path_to_files,'0121Z - inao - Culture de la Vigne', '0121Z - Culture de la Vigne.txt')
    growers = open(path_to_growers, "r")
    for g in growers:
        pos1 = g.find(';')
        pos2 = g.find(';', pos1 + 1)
        pos3 = g.find(';', pos2 + 1)
        pos4 = g.find(';', pos3 + 1)
        if  pos4 > - 1:
            errors.write(g)
        name = g[pos1+1:pos2].title()
        city = g[pos3+1:len(g)-1].title()
        p = WineProducer.create(inputName = name, country = 'France', postCode = g[pos2+1:pos3], city = city, producerType='v' )
        p.save()
        
    path_to_fves = os.path.join(path_to_files,'1102A - inao - Fabrication de vins effervescents','1102A - Fabrication de vins effervescents.txt')
    fves = open(path_to_fves, "r")
    for f in fves:
        pos1 = f.find(';')
        pos2 = f.find(';', pos1 + 1)
        pos3 = f.find(';', pos2 + 1)
        pos4 = f.find(';', pos3 + 1)
        if  pos4 > - 1:
            errors.write(f)
        p = WineProducer.create(inputName = f[pos1+1:pos2].title(), country = 'France', postCode = f[pos2+1:pos3], city = f[pos3+1:len(g)-1], producerType='e' )
        p.save()
        
    path_to_coops = os.path.join(path_to_files,'1102B - inao - Vinification','1102B - Vinification.txt')
    coops = open(path_to_coops, "r")
    for c in coops:
        pos1 = c.find(';')
        pos2 = c.find(';', pos1 + 1)
        pos3 = c.find(';', pos2 + 1)
        pos4 = c.find(';', pos3 + 1)
        if  pos4 > - 1:
            errors.write(c)
        p = WineProducer.create(inputName = c[pos1+1:pos2].title(), country = 'France', postCode = c[pos2+1:pos3], city = c[pos3+1:len(g)-1], producerType='e' )
        p.save()
        
    errors.close()
        
        
        