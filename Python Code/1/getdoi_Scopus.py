import numpy as np
import pandas as pd

data = pd.read_excel(r'2022_QS_World_University_Rankings_Results_public_version (1).xlsx', header=None)
data_np = np.array(data)
data_list = list(data_np)

author_list = []
title_list = []
year_list = []
journal_list = []
volume_list = []
number_list = []
pages_list = []
doi_list = []
url_list = []
affiliations_list = []
abstract_list = []
keywords_list = []
author_keywords_list = []
pmid_list = []
abbr_list = []
cited_list = []

qs_list = []
sjr_list = []
hindex_list = []

author_status = 0
year_status = 0
journal_status = 0
volume_status = 0
number_status = 0
pages_status = 0
doi_status = 0
affiliations_status = 0
abstract_status = 0
keywords_status = 0
author_keywords_status = 0
pmid_status = 0
abbr_status = 0

# kw = input('Please input keywords: ')
# pnum = input('Please input number: ')

temp = ''
count = 1
# with open('./scopus/scopus_{}_{}_201322.bib'.format(kw, pnum)) as f:
with open('./bib/raspberry pi_201322.bib') as f:
    j = 0
    for line in f:

        if (line[0] == '@' or '}@' in line) and temp != '':  # get the start of each bib
            if author_status == 0:
                author_list.append('NA')
            if year_status == 0:
                year_list.append('NA')
            if journal_status == 0:
                journal_list.append('NA')
            if volume_status == 0:
                volume_list.append('NA')
            if number_status == 0:
                number_list.append('NA')
            if pages_status == 0:
                pages_list.append('NA')
            if doi_status == 0:
                doi_list.append('NA')
            if affiliations_status == 0:
                affiliations_list.append('NA')
            if abstract_status == 0:
                abstract_list.append('NA')
            if keywords_status == 0:
                keywords_list.append('NA')
            if author_keywords_status == 0:
                author_keywords_list.append('NA')
            if pmid_status == 0:
                pmid_list.append('NA')
            if abbr_status == 0:
                abbr_list.append('NA')

            author_status = 0
            year_status = 0
            journal_status = 0
            volume_status = 0
            number_status = 0
            pages_status = 0
            doi_status = 0
            affiliations_status = 0
            abstract_status = 0
            keywords_status = 0
            author_keywords_status = 0
            pmid_status = 0
            abbr_status = 0

            temp = ''
            j += 1
            if len(author_list) != len(author_keywords_list):
                print(doi_list[j])
            count += 1
        if '	author = {' in line:
            author_list.append(line.split('{')[1].split('}')[0])
            author_status = 1
        if '	title = {' in line:
            temp += '1'
            title_list.append(line.split('{')[1].split('}')[0].replace('"', '""'))
        if '	year = {' in line:
            year = line.split('{')[1].split('}')[0]
            if year == '2023':
                year_list.append('2022')
            else:
                year_list.append(year)
            year_status = 1
        if '	journal = {' in line:
            journal_list.append(line.split('{')[1].split('}')[0].replace('"', '""'))
            journal_status = 1
        if '	volume = {' in line:
            volume_list.append(line.split('{')[1].split('}')[0])
            volume_status = 1
        if '	number = {' in line:
            number_list.append(line.split('{')[1].split('}')[0])
            number_status = 1
        if '	pages = {' in line:
            pages_list.append(line.split('{')[1].split('}')[0])
            pages_status = 1
        if '	doi = {' in line:
            doi = line.split('{')[1].split('}')[0]
            # if doi not in doi_list:
            #     doi_list.append(doi)
            #     doi_status = 1
            doi_list.append(doi)
            doi_status = 1
        if '	url = {' in line:
            url_list.append(line.split('{')[1].split('}')[0])
        if '	affiliations = {' in line:
            affiliations_list.append(line.split('{')[1].split('}')[0])
            affiliations_status = 1
        if '	abstract = {' in line:
            abstract_list.append(line.split('{')[1].split('}')[0].replace('"', '""'))
            abstract_status = 1
        if '	keywords = {' in line:
            keywords_list.append(line.split('{')[1].split('}')[0].lower())
            keywords_status = 1
        if '	author_keywords = {' in line:
            author_keywords_list.append(line.split('{')[1].split('}')[0].lower())
            author_keywords_status = 1
        if '	pmid = {' in line:
            pmid_list.append(line.split('{')[1].split('}')[0])
            pmid_status = 1
        if '	abbrev_source_title = {' in line:
            abbr_list.append(line.split('{')[1].split('}')[0].replace('"', '""'))
            abbr_status = 1
        if '	note = {' in line:
            cited_value = line.split('Cited by: ')[1]
            if ';' not in cited_value:
                cited_value = cited_value.split('}')[0]
            else:
                cited_value = cited_value.split(';')[0]
            cited_list.append(cited_value)

f.close()

# test the last one
if author_status == 0:
    author_list.append('NA')
if year_status == 0:
    year_list.append('NA')
if journal_status == 0:
    journal_list.append('NA')
if volume_status == 0:
    volume_list.append('NA')
if number_status == 0:
    number_list.append('NA')
if pages_status == 0:
    pages_list.append('NA')
if doi_status == 0:
    doi_list.append('NA')
if affiliations_status == 0:
    affiliations_list.append('NA')
if abstract_status == 0:
    abstract_list.append('NA')
if keywords_status == 0:
    keywords_list.append('NA')
if author_keywords_status == 0:
    author_keywords_list.append('NA')
if pmid_status == 0:
    pmid_list.append('NA')
if abbr_status == 0:
    abbr_list.append('NA')

# for i in range(len(author_list)):
#     print(author_list[i])

print(len(author_list))
print(len(title_list))
print(len(year_list))
print(len(journal_list))
print(len(volume_list))
print(len(number_list))
print(len(pages_list))
print(len(doi_list))
print(len(url_list))
print(len(affiliations_list))
print(len(abstract_list))
print(len(keywords_list))
print(len(author_keywords_list))
print(len(pmid_list))
print(len(abbr_list))
print(len(cited_list))

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
        year_sjr -= 1

    if sjr_status == 0:
        sjr_list.append('NA')
        hindex_list.append('NA')

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

fa = open('./rpi_update.csv', 'w')
fa.write('DOI,Author,Title,Year,Source,Volume,Number,Pages,Url,Affiliations,Abstract,Keywords,'
         'Author Keywords,PMID,Source Abbrev,Citation Count,SJR,H index,Org QS,Database\n')

doi_delete = 0
author_delete = 0
journal_delete = 0

for i in range(len(author_list)):
    if doi_list[i] != 'NA' and author_list[i] != 'NA' and journal_list[i] != 'NA':
        info = ''
        info += ('"' + doi_list[i] + '",')
        info += ('"' + author_list[i] + '",')
        info += ('"' + title_list[i] + '",')
        info += ('"' + year_list[i] + '",')
        info += ('"' + journal_list[i] + '",')
        info += ('"' + volume_list[i] + '",')
        info += ('"' + number_list[i] + '",')
        info += ('"' + pages_list[i] + '",')
        info += ('"' + url_list[i] + '",')
        info += ('"' + affiliations_list[i].replace('"', '""') + '",')
        info += ('"' + abstract_list[i].replace('"', '""') + '",')
        info += ('"' + keywords_list[i] + '",')
        info += ('"' + author_keywords_list[i] + '",')
        info += ('"' + pmid_list[i] + '",')
        info += ('"' + abbr_list[i] + '",')
        info += ('"' + cited_list[i] + '",')

        info += ('"' + sjr_list[i] + '",')
        info += ('"' + hindex_list[i] + '",')
        info += ('"' + qs_list[i] + '",')
        # if pnum != 'wos' and pnum != 'pubmed':
        #     info += '"Scopus"\n'
        # elif pnum == 'wos':
        #     info += '"WOS"\n'
        # elif pnum == 'pubmed':
        #     info += '"Pubmed"\n'
        info += '"Scopus"\n'

        fa.write(info)
    elif doi_list[i] == 'NA':
        print(title_list[i])
        doi_delete += 1
    elif author_list[i] == 'NA':
        print(doi_list[i])
        author_delete += 1
    elif journal_list[i] == 'NA':
        print(doi_list[i])
        journal_delete += 1
fa.close()

print('doi delete num: {}'.format(doi_delete))
print('author delete num: {}'.format(author_delete))
print('journal delete num: {}'.format(journal_delete))

# f = open('./scopus/missing_rpi1.csv', 'a')
# database = 'Scopus'
# if pnum == 'wos':
#     database = 'Scopus+WOS'
# elif pnum == 'pubmed':
#     database = 'Scopus+WOS+Pubmed'
# f.write(kw + ',' + database + ',' + str(count) + ',' + str(doi_delete) + ','
#         + str(author_delete) + ',' + str(journal_delete) + ',0,'
#         + str(count - doi_delete - author_delete - journal_delete) + '\n')
# f.close()
