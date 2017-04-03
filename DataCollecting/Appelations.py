from DataCollecting.Regions import regionsAppellations, regions
import urllib3
import os, shutil


def find_region(appelation):
    index = 0
    for appForRegions in regionsAppellations:
        for app in appForRegions:
            if app.find(appelation) > -1:
                return regions[index]
        index = index + 1
    return 'Not found'



def complete_appelations_region():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    appelations_in_path = os.path.join(dir_path, 'appelations_in.txt')
    appelations_in =  open(appelations_in_path, "r")
    appelations_out_path = os.path.join(dir_path, 'appelations_out2.txt')
    appelations_out = open(appelations_out_path, "w")
    for line in appelations_in:
        pos = line.find(';')
        appelation = line[:pos].lower()
        region = find_region(appelation)
        appelations_out.write(line[:len(line)-1]+';' + region + '\n')
    appelations_in.close()
    appelations_out.close()

    
def complete_appelations():
    complete_appelations_region()