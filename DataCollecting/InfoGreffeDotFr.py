from DataCollecting.output.Departements import departements
import urllib3
import os, shutil

def browse_infogreffe_activity(activity):
    base_url = 'https://www.infogreffe.fr'
    http = urllib3.PoolManager()
    
    # create the output directory
    dir_path = os.path.dirname(os.path.realpath(__file__))
    dir_path = os.path.join(dir_path,activity)
    if os.path.exists(dir_path):
        shutil.rmtree(dir_path)
    os.makedirs(dir_path)
    
    all_out_path = os.path.join(dir_path, 'all.txt')
    all_out_file = open(all_out_path, "w")
    all_viti_index = 1
    # browse the department
    for d in departements:
        if d[0][0] == '0': # only the metropolitan
            dep_str = d[1]
            dep_str = dep_str.replace( ' ', '-')
            out_path = os.path.join(dir_path, dep_str + '.txt')
            out_file = open(out_path, "w")
            page_index = 1
            viti_index = 1
            while page_index > 0:# browse the pages for this departement
                r = http.request('GET', base_url + '/entreprises-departement/' + dep_str + '-1102B-'+d[0]+'-'+str(page_index)+'.html')
                if r.status == 200:
                    htmlFile = r.data.decode('utf-8')
                    pos = htmlFile.find(str(viti_index) + '&nbsp;-&nbsp;', 0)
                    if  pos == -1:
                        page_index = -1
                    else:
                        while pos > -1:
                            pos= htmlFile.find('.html', pos) + len('.html') + 2
                            end_pos = htmlFile.find('</a>', pos)
                            denomination = htmlFile[pos:end_pos]
                            pos= htmlFile.find('class="code">', pos) + len('class="code">')
                            end_pos = htmlFile.find('</span>', pos)
                            codePostal = htmlFile[pos:end_pos]
                            out_file.write(str(viti_index)+','+denomination + ',' + codePostal + '\n')
                            all_out_file.write(str(all_viti_index)+','+denomination + ',' + codePostal + '\n')
                            viti_index = viti_index + 1
                            all_viti_index = all_viti_index + 1
                            pos = htmlFile.find(str(viti_index) + '&nbsp;-&nbsp;', pos)
                    r.release_conn()
                    page_index = page_index + 1
                else:
                    page_index = 0
            out_file.close()
    all_out_file.close()
    
def browse_infogreffe_dot_fr():
    browse_infogreffe_activity('1102A')# Fabrication de vins effervescents
    browse_infogreffe_activity('1102B')# Vinification
    browse_infogreffe_activity('0121Z')# Culture de la Vigne
    