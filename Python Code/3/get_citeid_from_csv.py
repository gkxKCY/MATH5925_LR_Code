count = 0
eid_list = []

with open("./bib/raspberry pi_201322.bib") as f:
    for line in f:
        if "	url = {" in line:
            eid = line.replace("	url = {https://www.scopus.com/inward/record.uri?eid=2-s2.0-", "")
            eid = eid.split("&doi")[0]
            if eid not in eid_list:
                eid_list.append(eid)

print(len(eid_list))
f.close()

f = open("./eid_1.txt", 'w')
for i in range(len(eid_list)):
    f.write(eid_list[i] + '\n')
f.close()
