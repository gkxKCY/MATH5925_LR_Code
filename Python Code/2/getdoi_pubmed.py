import os

queryTest = input('Please input the keyword: ')  # get keyword
pnum = input('Please input number: ')  # get number
path = './pubmed/{}'.format(queryTest)
files = os.listdir(path)  # get all list

doi_list = []
temp = ''
nodoi_count = 0
doi_status = 0

for file in files:
    if 'pubmed_' not in file and '.DS_Store' not in file:
        f = open(path + '/' + file)
        content = f.read()
        temp += content
        temp += '\n'
        f.close()

f = open(path + '/pubmed_{}_{}_201322.txt'.format(queryTest, pnum), 'w')
f.write(temp)
f.close()

f = open(path + '/pubmed_{}_{}_201322.txt'.format(queryTest, pnum), 'r')
j = 0
for line in f:
    if 'PMID- ' in line and len(doi_list) != 0:
        if doi_status == 0:
            nodoi_count += 1
        doi_status = 0
        j += 1
    if 'LID - ' in line and '[doi]' in line:
        doi = line.split('LID - ')[1].split(' [doi]')[0]
        doi_list.append(doi)
        doi_status += 1
if doi_status == 0:
    nodoi_count += 1
j += 1
f.close()

f = open('./pubmed/pubmed_{}_{}_201322.csv'.format(queryTest, pnum), 'w')
f.write('DOI\n')
for i in range(len(doi_list)):
    f.write(doi_list[i] + '\n')
f.close()

f = open('./pubmed/missing.csv', 'a')
database = 'Pubmed'
count = j
f.write(queryTest + ',' + database + ',' + str(j) + ',' + str(nodoi_count) + ','
        + '0,0,0,' + str(count - nodoi_count) + '\n')
f.close()


