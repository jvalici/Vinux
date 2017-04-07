import urllib3
import os
import re

def remove_special_chars(the_str):
    tmp = the_str.replace('\u00e0', 'a').replace('\u00e2', 'a').replace('\u00e4', 'a').replace('\u00e7', 'c')
    tmp = tmp.replace('\u00e8', 'e').replace('\u00e9', 'e').replace('\u00ea', 'e').replace('\u00eb', 'e')
    tmp = tmp.replace('\u00ee', 'i').replace('\u00ef', 'i').replace('\u00f4', 'o').replace('\u00f6', 'o')
    tmp = tmp.replace('\u00f9', 'u').replace('\u00fb', 'u').replace('\u00fc', 'u')
    return tmp

def browse_inao_dot_gouv_dot_fr():
    base_url = 'http://www.inao.gouv.fr/produit/'
    http = urllib3.PoolManager()
    
    # create the output directory
    dir_path = os.path.dirname(os.path.realpath(__file__))
    all_out_path = os.path.join(dir_path, 'inao_all.txt')
    all_out_file = open(all_out_path, "w")
    small_files_size = 500
    # browse the department
    for product_index in range(7000):
        if product_index%small_files_size == 0:
            out_path = os.path.join(dir_path, 'inao_'+str(product_index)+'.txt')
            out_file = open(out_path, "w")
        r = http.request('GET', base_url +str(product_index + 1))
        htmlFile = r.data.decode('utf-8')
        pos_prod = htmlFile.find('Produit</strong> : ', 0)
        if  pos_prod < 0:
            all_out_file.write('issue with '+str(product_index + 1)+'\n')
            out_file.write('issue with '+str(product_index + 1)+'\n')
        else:
            pos_prod = pos_prod + len('Produit</strong> : ')
            pos_prod_end = htmlFile.find('</li>', pos_prod)
            pos_prod_end = min( max( pos_prod, pos_prod_end), pos_prod + 1000 )
            pos_maj = htmlFile.find(' jour</strong> : ', pos_prod ) + len(' jour</strong> : ')
            pos_maj = min( max( pos_prod, pos_maj), pos_prod + 1000 )
            pos_maj_end = htmlFile.find('</li>', pos_maj)
            pos_maj_end = min( max( pos_prod, pos_maj_end), pos_prod + 1000 )
            pos_stfr = htmlFile.find('Statut FR</strong> : ', pos_prod )
            if pos_stfr > 0:
               pos_stfr = pos_stfr + len('Statut FR</strong> : ')
            pos_stfr_end = htmlFile.find('</li>', pos_stfr)
            pos_stfr_end = min( max( pos_prod, pos_stfr_end), pos_prod + 1000 )
            pos_stce = htmlFile.find('Statut CE</strong> : ', pos_prod ) + len('Statut CE</strong> : ')
            pos_stce = min( max( pos_prod, pos_stce), pos_prod + 1000 )
            pos_stc_end = htmlFile.find('</li>', pos_stce)
            pos_mc = htmlFile.find('Mots-cl', pos_prod) + len('Mots-cles</strong> : ')
            pos_mc_end = htmlFile.find('</li>', pos_mc)
            pos_ap = htmlFile.find('Appellation</strong> : ', pos_prod) + len('Appellation</strong> : ')
            pos_ap_end = htmlFile.find('</li>', pos_ap)
            pos_de = htmlFile.find('nomination</strong> : ', pos_prod) + len('nomination</strong> : ')
            pos_de_end = htmlFile.find('</li>', pos_de)
            mc = htmlFile[pos_mc:pos_mc_end]
            if mc.find('Vins ') > -1:
                tmp = htmlFile[pos_prod:pos_prod_end]+';'+htmlFile[pos_maj:pos_maj_end]+';'
                all_out_file.write(tmp)
                out_file.write(tmp)
                if pos_stfr > 0:
                    tmp = htmlFile[pos_stfr:pos_stfr_end]+';'
                    all_out_file.write(tmp)
                    out_file.write(tmp)
                else:
                    all_out_file.write(';')
                    out_file.write(';')
                tmp = htmlFile[pos_stce:pos_stc_end]+';'+mc+';'+htmlFile[pos_ap:pos_ap_end]+';'+htmlFile[pos_de:pos_de_end]+'\n'
                all_out_file.write(tmp)
                out_file.write(tmp)
        r.release_conn()
        if (product_index + 1)%small_files_size == 0:
            out_file.close()
    all_out_file.close()
    

def clean_denominations():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    denom_in_path = os.path.join(dir_path, 'denominations_inao.txt')
    denom_in =  open(denom_in_path, "r")
    denoms_out_path = os.path.join(dir_path, 'denominations_inao_cleaned.txt')
    denom_out = open(denoms_out_path, "w")
    errors_path = os.path.join(dir_path, 'denominations_inao_errors.txt')
    errors = open(errors_path, "w")
    prev =''
    for line in denom_in:
        pos1 = line.find(';')
        pos2 = line.find(';', pos1 + 1)
        pos3 = line.find(';', pos2 + 1)
        pos4 = line.find(';', pos3 + 1)
        pos5 = line.find(';', pos4 + 1)
        pos6 = line.find(';', pos5 + 1)
        denom1 = remove_special_chars(line[:pos1].lower())
        denom2 = line[pos6+1:len(line)-1]#-1 for \n char
        denom2_mod = remove_special_chars(denom2.lower())
        if denom1 != prev:
            if denom1.find(denom2_mod) == -1:
                errors.write(denom1+'-------' + denom2+'-------' + denom2_mod+ '\n')
            if  len(re.findall('[A-Z][A-Z]', denom2 ))>0:
                 errors.write(denom1+'-------' + denom2+'-------' + denom2_mod+ '\n')
            denom_out.write(denom2+line[len(denom2):])
        prev = denom1
    denom_in.close()
    denom_out.close()
    errors.close()