import requests
import time
import os
import urllib.request

type_ref = ['modern-language-association']
type_ref.append('apa')
type_ref.append('chicago-author-date')
type_ref.append('harvard-cite-them-right')
type_ref.append('elsevier-vancouver-author-date')

fr = open('./rpi_reference.csv', 'w')
temp = 'DOI,MLA,APA,Chicago,Harvard,Vancouver\n'
count = 1
with open('./rpi_with_count&lc&ftc.csv') as f:
    for line in f:
        start_time = time.time()
        if 'DOI,Author,Title,Year,Source' in line:
            continue
        line = line.split('","')
        doi = line[0].replace('"', '')
        doi_r = doi.replace('/', '%2F').replace('(', '%28').replace(')', '%29')
        # print(doi_r)
        temp_line = '"{}",'.format(doi)
        for i in range(len(type_ref)):
            url = 'https://citation.crosscite.org/format?doi={}&style={}&lang=en-US'.format(doi_r, type_ref[i])
            # print(url)
            content = requests.get(url, verify=False)
            content.encoding = "utf-8"
            # print(content.text)
            temp_line += '"{}"'.format(content.text.replace('\n', ''))
            if i != len(type_ref) - 1:
                temp_line += ','
            else:
                temp_line += '\n'
        temp += temp_line
        end_time = time.time()
        print('No.{} reference deal time: {}'.format(count, end_time - start_time))
        count += 1

f.close()
fr.write(temp)
fr.close()


