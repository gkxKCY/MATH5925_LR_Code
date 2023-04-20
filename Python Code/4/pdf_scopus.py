import os

doi_dict = {}
doi_list = []
doi_combine = ''
doi_count = 0

with open("./fail.csv") as f:
    for line in f:
        if line == 'DOI\n':
            continue
        doi = line.replace('\n', '')
        if doi_combine != '':
            doi_combine += ' OR '
        doi_combine += 'DOI(' + doi + ')'
        doi_list.append(doi)
        doi_dict[doi] = ''
        doi_count += 1
f.close()


with open('./rpi_with_count&lc.csv') as f:
    for line in f:
        if 'DOI,Author,Title,Year,Source' in line:
            continue
        line = line.split('","')
        doi_get = line[0].replace('"', '')
        title_get = line[2]
        if doi_get in doi_dict.keys():
            doi_dict[doi_get] = title_get

print(doi_combine)
print(doi_count)
print(doi_list)
print(len(doi_list))
print(doi_dict)
print(len(doi_dict))

path = './papers/3'
files = os.listdir(path)
for file in files:
    with open(path + '/' + file) as f:
        for keys in doi_dict:
            # if doi_dict[keys].replace(' ', '-').lower() in file.lower() and keys in doi_list:
            # s_with = doi_dict[keys].replace('-', '').replace(' ', '-').replace('(', '').replace(')', '').replace(',', '')\
            #     .replace(':', '').replace('/', '').replace('’', '').replace('.', '')
            s_with_curr = doi_dict[keys].replace('-', '').replace(' ', '-')
            s_with = ''
            for i in range(len(s_with_curr)):
                if 48 <= ord(s_with_curr[i]) <= 57 or 65 <= ord(s_with_curr[i]) <= 90 or 97 <= ord(s_with_curr[i]) <= 122 or ord(s_with_curr[i]) == 45:
                    s_with += s_with_curr[i]
            if file.lower().startswith(s_with.lower()) and keys in doi_list:
                doi_list.remove(keys)
                doi_first = keys.split('/')[0]
                doi_last = keys.replace(doi_first + '/', '')
                doi_last = doi_last.replace('/', '%252F').replace('(', '%2528').replace(')', '%2529')
                print(file)
                print(keys)
                os.rename("./papers/3/" + file, "./papers/3/" + doi_first + '_' + doi_last + ".pdf")
    f.close()

fail = open('./fail_3.csv', 'w')
fail.write('DOI\n')
for i in range(len(doi_list)):
    fail.write(doi_list[i] + '\n')
fail.close()
