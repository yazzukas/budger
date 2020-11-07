#Budger
#Sten Ambus, Kaur Vali, 2020

import csv

# loeb andmebaasi järjendisse ja tagastab selle
def loe_andmebaas(failinimi):
    andmebaas = []
    with open(failinimi, encoding = "UTF-8") as fail:
        for rida in fail:
            andmebaas.append(rida.strip().split(","))
    return andmebaas

# võtab argumendiks csv faili, puhastab selle ning kirjutab uude faili
def puhasta_csv_fail(csv_fail, puhastatud_csv_fail):
    with open(csv_fail, 'r', newline='', encoding = "UTF-8") as csvread:
        reader = csv.reader(csvread, delimiter=';')
        with open(puhastatud_csv_fail, 'w', newline='', encoding = "UTF-8") as csvwrite:
            writer = csv.writer(csvwrite, delimiter=';')
            for row in reader:
                # 10 - algsaldo 20 - tehingud  82 - sissetulek/väljaminek 86 - lõppsaldo
                if row[1] == "20":
                    writer.writerow([row[2]] + [row[3]] + [row[5]] + [row[7]])
                elif row[1] == "82" and row[7] == "D":
                    writer.writerow([row[2]] + ['Väljaminekud'] + [row[5]] + [row[7]])
                elif row[1] == "82" and row[7] == "K":
                    writer.writerow([row[2]] + ['Sissetulekud'] + [row[5]] + [row[7]])
                elif row[1] == "86":
                    writer.writerow([row[2]] + ['Saldo'] + [row[5]] + [row[7]])

# loeb csv andmed järjendisse ja tagastab selle
def loe_andmed_csv(csv_fail):
    andmed = []
    with open(csv_fail, newline='', encoding = "UTF-8") as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        for row in reader:
            andmed.append(row)
    return andmed

def sorteeri_andmed(andmebaas, andmed):
    sorteeritud = {}
    for rida in andmed:
        #print(rida)
        if rida[1] == "Sissetulekud":
            if rida[1] not in sorteeritud:
                sorteeritud['Sissetulekud'] = rida[2]
            else:
                sorteeritud['Sissetulekud'] += rida[2]
        elif rida[1] == "Väljaminekud":
            if rida[1] not in sorteeritud:
                sorteeritud['Väljaminekud'] = rida[2]
            else:
                sorteeritud['Väljaminekud'] += rida[2]
        else:
            for i in andmebaas:
                if i[0] in rida[1]:
                    if rida[1] not in sorteeritud:
                        sorteeritud[i[1].strip()] = rida[2]
                        break
                    else:
                        sorteeritud[i[1].strip()] += rida[2]
                        break
    return sorteeritud
        
andmebaas = loe_andmebaas('test files/andmebaas.txt')

puhasta_csv_fail('test files/Budger sample.csv', 'test files/puhastatud.csv')

andmed = loe_andmed_csv('test files/puhastatud.csv')
sorteeritud_andmed = sorteeri_andmed(andmebaas, andmed)





print(andmebaas)
print(sorteeritud_andmed)
print()
print("Sellel perioodil oli sissetulek " + sorteeritud_andmed['Sissetulekud'] + " eurot.")
print("Sellel perioodil oli väljaminek " + sorteeritud_andmed['Väljaminekud'] + " eurot.")
print()

print(sorteeritud_andmed['Toidupood'])

for i in sorteeritud_andmed:
    print(i)
    print(sorteeritud_andmed[i])