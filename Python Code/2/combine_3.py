queryTest = input('Please input the keyword: ')  # get keyword
snum = input('Please input scopus number: ')  # get scopus
if snum != '500':
    snum = '1000'

temp = 'DOI,Author,Title,Year,Source,Volume,Number,Pages,Url,Affiliations,Abstract,Keywords,'\
         'Author Keywords,PMID,Source Abbrev,Citation Count,SJR,H index,Org QS,Database,Searching Keyword\n'

with open('./scopus/scopus_{}_{}_201322.csv'.format(queryTest, snum)) as f:
    for line in f:
        if 'DOI,Author,Title,Year,Source' in line:
            continue
        temp += (line.replace('\n', '') + ',"{}"\n'.format(queryTest))
f.close()

with open('./scopus/scopus_{}_wos_201322.csv'.format(queryTest)) as f:
    for line in f:
        if 'DOI,Author,Title,Year,Source' in line:
            continue
        temp += (line.replace('\n', '') + ',"{}"\n'.format(queryTest))
f.close()

with open('./scopus/scopus_{}_pubmed_201322.csv'.format(queryTest)) as f:
    for line in f:
        if 'DOI,Author,Title,Year,Source' in line:
            continue
        temp += (line.replace('\n', '') + ',"{}"\n'.format(queryTest))
f.close()

f = open('./combine/combine_{}_201322.csv'.format(queryTest), 'w')
f.write(temp)
f.close()
