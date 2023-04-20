temp = 'DOI,Author,Title,Year,Source,Volume,Number,Pages,Url,Affiliations,Abstract,Keywords,Author Keywords,' \
       'PMID,Source Abbrev,Citation Count,SJR,H index,Org QS,Database,Searching Keyword'
temp += ',Title Frequency,Abstract Frequency,DB Keyword Frequency,Author Keyword Frequency\n'

with open('./rpi_update.csv') as f:
    for line in f:
        if "DOI,Author,Title,Year,Source" in line:
            continue
        line_list = line.split('","')
        keyword = []
        for i in range(8):
            keyword.append([])
        keyword[0] = line_list[20].replace('"\n', '')
        for i in range(1, 8):
            keyword[i] = '999999999'

        if keyword[0] == 'ai application':
            keyword[0] = '(ai)'
            keyword[1] = 'ai '
            keyword[2] = ' ai'
            keyword[3] = 'ai,'
            keyword[4] = 'ai-'
            keyword[5] = ' ai '
            keyword[6] = ' ai,'
            keyword[7] = ' ai-'
        elif keyword[0] == 'hydrogen energy':
            keyword[0] = 'hydrogen'
        title = line_list[2]
        abstract = line_list[10]
        keyword_sys = line_list[11]
        keyword_author = line_list[12]
        count_title = 0
        count_abstract = 0
        count_keyword_sys = 0
        count_keyword_author = 0
        for i in range(5):
            count_title += (title.count(keyword[i]) + title.count(keyword[i].capitalize()) + title.count(keyword[i].upper()))
            count_abstract += (abstract.count(keyword[i]) + abstract.count(keyword[i].capitalize()) + abstract.count(keyword[i].upper()))
            count_keyword_sys += keyword_sys.count(keyword[i])
            count_keyword_author += keyword_author.count(keyword[i])
        for i in range(5, 8):
            count_title -= (title.count(keyword[i]) + title.count(keyword[i].capitalize()) + title.count(keyword[i].upper()))
            count_abstract -= (abstract.count(keyword[i]) + abstract.count(keyword[i].capitalize()) + abstract.count(keyword[i].upper()))
            count_keyword_sys -= keyword_sys.count(keyword[i])
            count_keyword_author -= keyword_author.count(keyword[i])
        temp_line = line.replace('\n', '')
        temp_line += (',"{}"'.format(count_title))
        temp_line += (',"{}"'.format(count_abstract))
        temp_line += (',"{}"'.format(count_keyword_sys))
        temp_line += (',"{}"'.format(count_keyword_author))
        temp_line += '\n'
        temp += temp_line
    f.close()

f = open('./rpi_with_count.csv', 'w')
f.write(temp)
f.close()
