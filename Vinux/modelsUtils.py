
def remove_special_chars(the_str):
    tmp = the_str.replace('\u00e0', 'a').replace('\u00e2', 'a').replace('\u00e4', 'a').replace('\u00e7', 'c')
    tmp = tmp.replace('\u00e8', 'e').replace('\u00e9', 'e').replace('\u00ea', 'e').replace('\u00eb', 'e')
    tmp = tmp.replace('\u00ee', 'i').replace('\u00ef', 'i').replace('\u00f4', 'o').replace('\u00f6', 'o')
    tmp = tmp.replace('\u00f9', 'u').replace('\u00fb', 'u').replace('\u00fc', 'u')
    return tmp


def find_initials_and_replace(compagny_name, initials):
    compagny_name_lc = compagny_name.lower()
    pos = compagny_name_lc.find( initials + ' des ')
    if pos == 0:
        return 1, 'Les ' + compagny_name[len(initials+ ' des '):]
    pos = compagny_name_lc.find( initials + ' du ')
    if pos == 0:
        return 1, compagny_name[len(initials + ' du '):]
    pos = compagny_name_lc.find( initials)
    if pos == 0:
        return 1, compagny_name[len(initials):]
    pos = compagny_name_lc.find( ' ' + initials)
    if pos + len( ' ' + initials ) == len(compagny_name):
        return 1, compagny_name[:pos]
    return 0,''
    
def get_usual_name_from_compagny_name(compagny_name):
        initials_to_remove = [ 'earl', 'scea', 'sce ',' sce', 'sca', 'gaec','gfa', 'sas','scev']
        strings_to_remove = [    'indivision ',
            'societe a responsabilite limitee des ',
            'societe a responsabilite limitee ',
            'societe civile d\'exploitation agricole des ',
            'societe civile d\'exploitation agricole ',
            'groupement agricole d\'exploitation en commun reconnu ',
            'exploitation agricole a responsabilite limitee des ',
            'exploitation agricole a responsabilite limitee ',
            '"']
        
        for i in initials_to_remove:
            a,b = find_initials_and_replace(compagny_name, i)
            if a > 0:
                return b
            tmp = '.'.join(i)+'.'
            a,b = find_initials_and_replace(compagny_name, tmp)
            if a > 0:
                return b
        compagny_name_modified = remove_special_chars(compagny_name.lower())
        for s in strings_to_remove:
            pos = compagny_name_modified.find(s)
            if pos == 0:
                return compagny_name[len(s):]
        return compagny_name
