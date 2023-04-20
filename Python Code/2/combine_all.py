import os

path = './combine'
temp = 'DOI,Author,Title,Year,Source,Volume,Number,Pages,Url,Affiliations,Abstract,Keywords,'\
         'Author Keywords,PMID,Source Abbrev,Citation Count,SJR,H index,Org QS,Database,Searching Keyword\n'
f = open(path + '/combine_all.csv', 'w')

files = os.listdir(path)  # get all list
for file in files:
    if 'combine_' in file and '_old' not in file and '_all' not in file:
        with open(path + '/' + file) as file_alone:
            for line in file_alone:
                kw = file.split('_')[1]
                if 'DOI,Author,Title,Year,Source' in line:
                    continue
                temp += (line.split('\n')[0] + ',"' + kw + '"\n')
            file_alone.close()

f.write(temp)
f.close()
