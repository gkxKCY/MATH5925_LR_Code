
import re
import os
import urllib.request
import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36',
}


def getPaperPdf(url):
    pattern = '/.*?\.pdf'
    content = requests.get(url, headers=headers)
    download_url = re.findall(pattern, content.text)
    print(download_url)
    d_url = ""
    if '/pdf" src="' in download_url[1]:
        d_url = download_url[1].replace('/pdf" src="', '')
    d_url = "https:" + d_url
    print(d_url)
    path = r"papers"
    if os.path.exists(path):
        pass
    else:
        os.makedirs(path)

    req = urllib.request.Request(d_url, headers=headers)

    u = urllib.request.urlopen(req, timeout=5)

    file_name = download_url[1].split('/')[-2] + '_' + download_url[1].split('/')[-1]
    f = open(path + '/' + file_name, 'wb')


    block_sz = 8192
    while True:
        buffer = u.read(block_sz)
        if not buffer:
            break
        f.write(buffer)
    f.close()
    print("Sucessful to download" + " " + file_name)
    doi_get = url.replace("https://sci-hub.ren/", "")
    doi_first = doi_get.split('/')[0]
    doi_last = doi_get.replace(doi_first + '/', '')
    doi_last = doi_last.replace('/', '%252F').replace('(', '%2528').replace(')', '%2529')
    os.rename("./papers/" + file_name, "./papers/" + doi_first + '_' + doi_last + ".pdf")


if __name__ == '__main__':
    sci_Hub_Url = "https://sci-hub.ren/"
    fail = open('./fail_2.csv', 'w')
    fail.write('DOI\n')
    with open('./doi.csv') as f:
        for line in f:
            if line == 'DOI\n':
                continue
            doi = line.replace('\n', '')
            paper_url = sci_Hub_Url + doi
            print(paper_url)
            try:
                getPaperPdf(paper_url)  # get pdf
            except Exception:
                print("Failed to get pdf")
                fail.write(doi + '\n')
    f.close()
    fail.close()

