from Vinux.models import  WineProducer, WineProductionArea, WineAppelation, WineDenomination
import os

def init_data_base_with_known_objects():
    
    path_to_files = os.path.dirname(os.path.realpath(__file__))
    path_to_files = os.path.join(path_to_files, '..', '..', 'DataCollecting', 'output')
    
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
                wpa = WineProductionArea( name = a[:pos], parentArea = parentArea)
            wpa.save()
    
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
            pos3 = alc.find(';', pos2 + 1)
            area_name = alc[ pos3+1:]
            try:
                area = WineProductionArea.objects.get(name__iexact = area_name)
            except:
                errors.write(area_name+'\n')
            app = WineAppelation( name= a[pos1+1:pos2], area=area, euStatus = aop_igp, isAOC=is_aoc)
            app.save()
        
        
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
            den = WineDenomination( name=d[:pos1], appelation=app)
            den.save()
    errors.close()
        
        
        