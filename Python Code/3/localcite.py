import os

doi_dict = {}
title_dict = {}
g_count_list = []

with open("./rpi_with_count.csv") as f:
    for line in f:
        if 'DOI,Author,Title,Year,Source' in line:
            continue
        line = line.split('","')
        doi = line[0].replace('"', '')
        doi_dict[doi] = 0
        title_dict[doi] = line[2]
        g_count = int(line[15])
        g_count_list.append(g_count)
f.close()

# print(doi_dict)
# print(len(doi_dict))

path = './ref_rpi'
files = os.listdir(path)
for file in files:
    with open(path + '/' + file) as f:
        for line in f:
            if 'DOI: 10.' in line:
                doi_test = line.split('DOI: ')[1].replace('\n', '')
                if doi_test in doi_dict:
                    doi_dict[doi_test] += 1
    f.close()

temp = 'DOI,Author,Title,Year,Source,Volume,Number,Pages,Url,Affiliations,Abstract,Keywords,Author Keywords,PMID,Source Abbrev,Total Citation Count,SJR,H index,Org QS,Database,Searching Keyword,Title Frequency,Abstract Frequency,DB Keyword Frequency,Author Keyword Frequency,Local Citation Count,Global Citation Count\n'
ct = 0
with open("./rpi_with_count.csv") as f:
    for line in f:
        if 'DOI,Author,Title,Year,Source' in line:
            continue
        line = line.replace('\n', '')
        doi_line = line.split('","')[0].replace('"', '')
        count = doi_dict[doi_line]
        line += ',"{}","{}"\n'.format(str(count), str(g_count_list[ct] - count))
        temp += line
        ct += 1
f.close()

f = open('./rpi_with_count&lc.csv', 'w')
f.write(temp)
f.close()

a1 = sorted(doi_dict.items(), key=lambda x: x[1], reverse=True)
prev_value = 999999
prev_rank = 0

lc = 'Rank,DOI,Title,Local Citation Count\n'
f = open('./raspberry_top10_localcite.csv', 'w')
for i in range(len(a1)):
    if i >= 10 and a1[i][1] < prev_value:
        break
    if a1[i][1] == prev_value:
        rank = prev_rank
    else:
        rank = i + 1
    lc += (str(rank) + ',' + a1[i][0] + ',' + title_dict[a1[i][0]] + ',' + str(a1[i][1]) + '\n')
    prev_value = a1[i][1]
    prev_rank = rank
f.write(lc)
f.close()
