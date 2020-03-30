import sys, csv

infile = sys.argv[1]

file = open(infile,'r',encoding='utf8')
file2 = open('adjusted_output.csv','w+',encoding='utf8',newline='')
writer = csv.writer(file2,delimiter=',')

for line in file:
    items = line.split(',',4)

    #print(items)
    items[4] = items[4].replace(',','').strip(r'\n').strip()
    print(items[4])
    writer.writerow([items[0],items[1],items[2],items[3],items[4]])

file.close()
file2.close()
