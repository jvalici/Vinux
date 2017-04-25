import os

def remove_special_chars(the_str):
    tmp = the_str.replace('\u00e0', 'a').replace('\u00e2', 'a').replace('\u00e4', 'a').replace('\u00e7', 'c')
    tmp = tmp.replace('\u00e8', 'e').replace('\u00e9', 'e').replace('\u00ea', 'e').replace('\u00eb', 'e')
    tmp = tmp.replace('\u00ee', 'i').replace('\u00ef', 'i').replace('\u00f4', 'o').replace('\u00f6', 'o')
    tmp = tmp.replace('\u00f9', 'u').replace('\u00fb', 'u').replace('\u00fc', 'u')
    return tmp

def check_inao_against_data_dot_gouv():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    inao_path = os.path.join(dir_path, 'denominations_inao.txt')
    data_gouv_path = os.path.join(dir_path, 'output', 'Inao-Aires_produits.txt')
    errors_path = os.path.join(dir_path, 'denominations_inao_errors.txt')
    errors = open(errors_path, "w")
    inao = open(inao_path, "r")
    data_gouv = open(data_gouv_path, "r")
    data_gouv_data = remove_special_chars(data_gouv.read().lower())
    data_gouv.close()
    for line in inao:
        pos1 = line.find(';')
        denom = remove_special_chars(line[:pos1].lower())
        pos2 = data_gouv_data.find(denom)
        if pos2 == -1: 
            denom = denom.replace( ' primeur', '')
            denom = denom.replace( ' rouge', '')
            denom = denom.replace( ' blanc', '')
            denom = denom.replace( ' rose', '')
            denom = denom.replace( ' rancio', '')
            denom = denom.replace( ' hors d\'age', '')
            denom = denom.replace( ' mousseux de qualite', '')
            denom = denom.replace( ' mousseux', '')
            denom = denom.replace( ' de qualite', '')
            denom = denom.replace( ' selection de grains nobles', '')
            denom = denom.replace( ' vendanges tardives', '')
            denom = denom.replace( ' petillant', '')
            denom = denom.replace( ' sec', '')
            if denom[-1:] == ' ':
                denom = denom[:len(denom)-1]
            pos2 = data_gouv_data.find(denom)
            if pos2 == -1: 
                errors.write( line[:pos1] + '\n')
    errors.close()
    data_gouv.close()
        
        