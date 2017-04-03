import urllib3
import os, shutil

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
    denom_in_path = os.path.join(dir_path, 'denominations_inao_all.txt')
    denom_in =  open(denom_in_path, "r")
    denoms_out_path = os.path.join(dir_path, 'denominations_inao_all_cleaned.txt')
    denom_out = open(denoms_out_path, "w")
    prev = ''
    for line in denom_in:
        pos = line.find(';')
        denom = line[:pos].lower()
        if denom != prev:
            denom_out.write(line)
        prev = denom
    denom_in.close()
    denom_out.close()
            
    