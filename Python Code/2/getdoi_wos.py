

author_list = []
year_list = []
journal_list = []
doi_list = []

author_status = 0
year_status = 0
journal_status = 0
doi_status = 0

kw = input('Please input keywords: ')
pnum = input('Please input number: ')

temp = ''
with open('./wos/wos_{}_{}_201322.bib'.format(kw, pnum)) as f:
    j = 0
    for line in f:
        if (line[0] == '@' or '}@' in line) and temp != '':  # get the start of each bib
            if author_status == 0:
                author_list.append('NA')
            if year_status == 0:
                year_list.append('NA')
            if journal_status == 0:
                journal_list.append('NA')
            if doi_status == 0:
                doi_list.append('NA')

            author_status = 0
            year_status = 0
            journal_status = 0
            doi_status = 0
            j += 1

        if 'Author = {' in line and line[0] == 'A':
            if '},\n' in line:
                author = line.split('{')[1].split('}')[0]
                author_list.append(author)
                author_status = 1
            else:
                author = line.split('{')[1].split('\n')[0]
                author_status = 11
        if author_status == 11:
            if '   ' in line:
                author += (' ' + line.split('   ')[1].split('\n')[0])
            elif 'Author = {' not in line:
                author = author.split('},')[0]
                author_list.append(author)
                author_status = 1
                author = ''

        if 'Title = {' in line:
            temp += '1'

        if 'Year = {' in line:
            year = line.split('{')[1].split('}')[0]
            if year == '2023':
                year_list.append('2022')
            else:
                year_list.append(year)
            year_status = 1

        if 'Journal = {' in line:
            if '},\n' in line:
                journal = line.split('{')[1].split('}')[0].replace('"', '""')
                journal_list.append(journal)
                journal_status = 1
            else:
                journal = line.split('{')[1].split('\n')[0].replace('"', '""')
                journal_status = 11
        if journal_status == 11:
            if '   ' in line:
                journal += (' ' + line.split('   ')[1].split('\n')[0].replace('"', '""'))
            elif 'Journal = {' not in line:
                journal = journal.split('},')[0]
                journal_list.append(journal)
                journal_status = 1
                journal = ''

        if 'Booktitle = {' in line:
            if '},\n' in line:
                journal = line.split('{')[1].split('}')[0].replace('"', '""')
                journal_list.append(journal)
                journal_status = 1
            else:
                journal = line.split('{')[1].split('\n')[0].replace('"', '""')
                journal_status = 11
        if journal_status == 11:
            if '   ' in line:
                journal += (' ' + line.split('   ')[1].split('\n')[0].replace('"', '""'))
            elif 'Booktitle = {' not in line:
                journal = journal.split('},')[0]
                journal_list.append(journal)
                journal_status = 1
                journal = ''

        if 'DOI = {' in line:
            doi = line.split('{')[1].split('}')[0].split(';')[0]  # maybe has not only one doi
            doi_list.append(doi)
            doi_status = 1


f.close()

# test the last one
if author_status == 0:
    author_list.append('NA')
if year_status == 0:
    year_list.append('NA')
if journal_status == 0:
    journal_list.append('NA')
if doi_status == 0:
    doi_list.append('NA')
j += 1

print(len(author_list))
print(len(year_list))
print(len(journal_list))
print(len(doi_list))


fa = open('./wos/wos_{}_{}_201322.csv'.format(kw, pnum), 'w')
fa.write('DOI\n')

doi_delete = 0
author_delete = 0
journal_delete = 0
year_delete = 0

for i in range(len(author_list)):
    if doi_list[i] != 'NA' and author_list[i] != 'NA' and journal_list[i] != 'NA' and year_list[i] != 'NA':
        info = ''
        info += ('"' + doi_list[i].replace('\\', '') + '"\n')

        fa.write(info)
    elif doi_list[i] == 'NA':
        doi_delete += 1
    elif author_list[i] == 'NA':
        author_delete += 1
    elif journal_list[i] == 'NA':
        journal_delete += 1
    elif year_list[i] == 'NA':
        year_delete += 1
fa.close()

print('The number of the removed literatures with no DOI information: {}'.format(doi_delete))
print('The number of the removed literatures with no author information: {}'.format(author_delete))
print('The number of the removed literatures with no journal information: {}'.format(journal_delete))
print('The number of the removed literatures with no year information: {}'.format(year_delete))

f = open('./wos/missing.csv', 'a')
database = 'wos'
count = j
f.write(kw + ',' + database + ',' + str(count) + ',' + str(doi_delete) + ','
        + str(author_delete) + ',' + str(journal_delete) + ',' + str(year_delete) + ','
        + str(count - doi_delete - author_delete - journal_delete - year_delete) + '\n')
f.close()
