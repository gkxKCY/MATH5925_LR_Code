import os


def begin(line):
    temp = ''
    if line[0] == '@':
        line = line.split('{')[0]
        temp += line
    else:
        line = line.split('}')[1].split('{')[0]
        temp += line
    return temp


def deal(doi_list, author_list, year_list, abbr_list, type, kw):
    doi_exist = []
    temp0 = ''
    temp1 = ''
    temp_all = ''
    doi = ''
    author = ''
    year = ''
    abbr = ''
    count = 0
    signal = 0
    # i = 0
    database = ''
    if type != 'wos' and type != 'pubmed':
        database = 'scopus'
    else:
        database = type
    print(database)
    with open('./scopus/scopus_{}_{}_201322.bib'.format(kw, type)) as f:
        for line in f:
            if line[0] == '@' or '}@' in line:
                if temp0 == '':  # get the start of each bib
                    temp0 += begin(line)
                else:
                    if doi != '' and author != '' and abbr != '' and year != '':
                        temp0 += ('{' + doi.replace('(', '_LB_').replace(')', '_RB_') + ',\n')
                        temp0 += temp1
                        if '}\n}\n' not in temp0:
                            temp0 += '}\n'
                        # if not os.path.exists('./collect/{}/bib/{}/'.format(kw, type)):
                        #     os.makedirs('./collect/{}/bib/{}/'.format(kw, type))
                        f_bib = open('./bib/{}/{}/{}_{}_{}_{}.bib'.format(kw, database, author, year, abbr, doi), 'w')
                        f_bib.write(temp0)
                        count += 1
                        f_bib.close()
                        temp_all += temp0
                        # print(i)
                        # print(cnt)
                        # i += 1
                    temp0 = ''
                    temp1 = ''
                    doi = ''
                    author = ''
                    year = ''
                    abbr = ''

                    temp0 += begin(line)
            elif temp0 != '':
                if '@' in line:
                    temp1 += line.replace('@', '_at_')  # avoid @ error in bibtex
                else:
                    temp1 += line

                for i in range(len(doi_list)):
                    if doi_list[i] in line and '	doi = {' in line and doi_list[i] not in doi_exist:
                        if type == 'pubmed' and kw == 'hydrogen energy':
                            print(doi_list[i])
                        doi_exist.append(doi_list[i])
                        # print(1)
                        # print(doi_list[i])
                        doi = doi_list[i].replace('/', '_')
                        author = author_list[i].replace('/', '-')
                        year = year_list[i]
                        abbr = abbr_list[i].replace('/', '-')
                        if 'Proc. - IEEE' in abbr_list[i]:
                            abbr = abbr_list[i].split(', ')[-1].replace('/', '-')
                        if 'IEEE Int. Symp. Parallel Distrib. Process. Appl., IEEE Int. Conf. Big Data Cloud Comput., IEEE Int. Conf. Soc. Comput. Netw. IEEE Int. Conf. Sustain. Comput. Commun., ISPA/BDCloud/SocialCom/SustainCom' in \
                                abbr_list[i]:
                            abbr = 'ISPA-BDCloud-SocialCom-SustainCom'
                        break

            # print(doi_list[i])

        f.close()

        if doi != '' and author != '' and abbr != '' and year != '':
            temp0 += ('{' + doi.replace('(', '_LB_').replace(')', '_RB_') + ',\n')
            temp0 += temp1
            if '}\n}\n' not in temp0:
                temp0 += '}\n'
            # if not os.path.exists('./collect/{}/bib/{}/'.format(kw, type)):
            #     os.makedirs('./collect/{}/bib/{}/'.format(kw, type))
            f_bib = open('./bib/{}/{}/{}_{}_{}_{}.bib'.format(kw, database, author, year, abbr, doi), 'w')
            f_bib.write(temp0)
            count += 1
            f_bib.close()
            temp_all += temp0

    # print('1l{}'.format(cnt))
    # print(i)
    print(count)
    print(len(doi_exist))
    return temp_all


# num = [1000, 1000, 1000, 1000, 500, 1000, 1000]
num = [1000]

kw_list = []
kw_count = -1

doi_list_scopus = []
doi_list_wos = []
doi_list_pubmed = []
author_list_scopus = []
author_list_wos = []
author_list_pubmed = []
abbr_list_scopus = []
abbr_list_wos = []
abbr_list_pubmed = []
year_list_scopus = []
year_list_wos = []
year_list_pubmed = []

for i in range(1):
    doi_list_scopus.append([])
    doi_list_wos.append([])
    doi_list_pubmed.append([])
    author_list_scopus.append([])
    author_list_wos.append([])
    author_list_pubmed.append([])
    abbr_list_scopus.append([])
    abbr_list_wos.append([])
    abbr_list_pubmed.append([])
    year_list_scopus.append([])
    year_list_wos.append([])
    year_list_pubmed.append([])

current_kw = ''
current_db = ''
with open('./combine/combine_raspberry pi_201322.csv') as f:
    for line in f:
        if 'DOI,Author,Title,Year,Source' in line:
            continue
        kw = line.split('","')[-1].split('"\n')[0]  # access keyword
        db = line.split('","')[-2]
        doi = line.split('","')[0].split('"')[1]
        author = line.split('","')[1].split(',')[0]
        abbr = line.split('","')[14]
        year = line.split('","')[3]
        if kw not in kw_list:  # create dir
            current_kw = kw
            kw_list.append(kw)
            kw_count += 1
            # if not os.path.exists('./bib/' + kw):
            #     os.makedirs('./bib/' + kw)
            #     os.makedirs('./bib/' + kw + '/scopus')
            #     os.makedirs('./bib/' + kw + '/wos')
            #     os.makedirs('./bib/' + kw + '/pubmed')
        if db == 'Scopus':
            doi_list_scopus[kw_count].append(doi)
            author_list_scopus[kw_count].append(author)
            abbr_list_scopus[kw_count].append(abbr)
            year_list_scopus[kw_count].append(year)
        elif db == 'WOS':
            doi_list_wos[kw_count].append(doi)
            author_list_wos[kw_count].append(author)
            abbr_list_wos[kw_count].append(abbr)
            year_list_wos[kw_count].append(year)
        elif db == 'Pubmed':
            doi_list_pubmed[kw_count].append(doi)
            author_list_pubmed[kw_count].append(author)
            abbr_list_pubmed[kw_count].append(abbr)
            year_list_pubmed[kw_count].append(year)
    f.close()

print(kw_list)
print(num)
# print(doi_list_scopus[6])
# print(doi_list_wos[6])
# print(doi_list_pubmed[6])
# print(len(doi_list_scopus[4]))
# print(len(doi_list_wos[4]))
# print(len(doi_list_pubmed[4]))

temp_all = ''
for i in range(len(kw_list)):
    print(i)
    temp_scopus = deal(doi_list_scopus[i], author_list_scopus[i], year_list_scopus[i], abbr_list_scopus[i], num[i], kw_list[i])
    temp_wos = deal(doi_list_wos[i], author_list_wos[i], year_list_wos[i], abbr_list_wos[i], 'wos', kw_list[i])
    temp_pubmed = deal(doi_list_pubmed[i], author_list_pubmed[i], year_list_pubmed[i], abbr_list_pubmed[i], 'pubmed', kw_list[i])
    temp_kw_all = temp_scopus + temp_wos + temp_pubmed
    f = open('./bib/{}_201322.bib'.format(kw_list[i]), 'w')
    f.write(temp_kw_all)
    f.close()
    temp_all += temp_kw_all

# f = open('./bib/all_201322.bib', 'w')
# f.write(temp_all)
# f.close()



