import os
import numpy as np
import pandas as pd

data = pd.read_excel(r'2022_QS_World_University_Rankings_Results_public_version (1).xlsx', header=None)
data_np = np.array(data)
data_list = list(data_np)

doi_list = []
title_dict = {}
g_count_list = []
journal_list = []
affiliations_list = []
sjr_list = []
hindex_list = []
qs_list = []

with open("./rpi_with_count.csv") as f:
    for line in f:
        if 'DOI,Author,Title,Year,Source' in line:
            continue
        line = line.split('","')
        doi = line[0].replace('"', '')
        doi_list.append(doi)
        journal = line[4]
        journal_list.append(journal)
        affiliations = line[9]
        affiliations_list.append(journal)
f.close()

for i in range(len(doi_list)):
    sjr_status = 0
    year_sjr = 2021
    while sjr_status == 0 and year_sjr >= 2013:
        with open('scimagojr {}.csv'.format(year_sjr), 'r') as f_rank:
            for line in f_rank:
                line = line.split(';')
                if journal_list[i] in line[2]:
                    sjr = line[5]
                    if ',' in sjr:
                        sjr = sjr.replace(',', '.')
                    elif sjr != '':
                        sjr = '0.' + sjr
                    else:
                        sjr = '-'
                    sjr_list.append(sjr)
                    hindex_list.append(line[7])
                    sjr_status = 1
                    break
                else:
                    sjr_list.append('NA')
                    hindex_list.append('NA')

        year_sjr -= 1

print(len(sjr_list))
print(len(hindex_list))

for i in range(len(doi_list)):
    qs_status = 0
    for j in range(len(data_list)):
        institute = str(list(data_list[j])[4]).replace('The ', '').rstrip(' ').split('(')[0].split(' - ')[0]
        institute_eng = str(list(data_list[j])[26]).replace('The ', '').rstrip(' ').split('(')[0].split(' - ')[0]
        if (institute.lower() in affiliations_list[i].split(';')[0].lower() or institute_eng.lower() in
            affiliations_list[i].split(';')[0].lower()) and list(data_list[j])[2] != 2011.0 \
                and list(data_list[j])[2] != 2022.0 and str(list(data_list[j])[2]) != 'RANK' and str(
            list(data_list[j])[2]) != 'rank display':
            qs = str(list(data_list[j])[2])
            if '  ' in qs:
                if '=' in qs:
                    qs = qs.split('  ')[1].split('=')[0]
                else:
                    qs = qs.split('  ')[1]
            qs_list.append(qs)
            qs_status = 1
            break

        if 'Harvard' in affiliations_list[i] and qs_status == 0:
            qs_list.append(list(data_list[8])[2])
            qs_status = 1
            break
    if qs_status == 0:
        qs_list.append('NA')

print(len(qs_list))

temp = 'DOI,Author,Title,Year,Source,Volume,Number,Pages,Url,Affiliations,Abstract,Keywords,Author Keywords,PMID,Source Abbrev,Total Citation Count,SJR,H index,Org QS\n'
ct = 0
with open("./rpi_with_count.csv") as f:
    for line in f:
        if 'DOI,Author,Title,Year,Source' in line:
            continue
        line += ',"{}","{}","{}"\n'.format(sjr_list[ct], hindex_list[ct], qs_list[ct])
        temp += line
        ct += 1
f.close()

f = open('./rpi_with_sjr&qs.csv', 'w')
f.write(temp)
f.close()
