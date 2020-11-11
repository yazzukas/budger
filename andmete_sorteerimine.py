import csv

# loeb andmebaasi järjendisse ja tagastab selle
def loe_andmebaas(failinimi):
    andmebaas = []
    with open(failinimi, encoding = "UTF-8") as fail:
        for rida in fail:
            andmebaas.append(rida.strip().split(","))
    return andmebaas

# https://stackoverflow.com/questions/3276180/extracting-date-from-a-string-in-python
import re
#from datetime import datetime
def leia_kuupäev_tekstist(tekst):
    try:
        kp = re.search(r'\d{2}-\d{2}-\d{2}', tekst.replace('.','-')).group(0).replace('-','.')
        kp = kp[:6] + "20" + kp[6:] # fix
    except:
        kp = None
    return str(kp)


# võtab argumendiks csv faili, puhastab selle ning kirjutab uude faili
def puhasta_csv_fail(csv_fail, puhastatud_csv_fail):
    with open(csv_fail, 'r', newline='', encoding = "UTF-8") as csvlugemiseks:
        with open(puhastatud_csv_fail, 'w', newline='', encoding = "UTF-8") as csvkirjutamiseks:
            uus_csv_fail = csv.writer(csvkirjutamiseks, delimiter=';')
            uus_csv_fail.writerow(['Kuupäev'] + ['Saaja/Maksja'] + ['Summa'] + ['Deebet/Krediit'])
            for rida in csv.reader(csvlugemiseks, delimiter=';'):
                
                kuupäev = rida[2]
                saaja_maksja = rida[3]
                selgitus = rida[4]
                summa = rida[5]
                deebet_krediit = rida[7]
                
                # 10 - algsaldo 20 - tehingud  82 - sissetulek/väljaminek 86 - lõppsaldo
                if rida[1] == "20":
                    # proovib selgitusest võtta kuupäeva
                    kuupäev = leia_kuupäev_tekstist(selgitus)
                    if kuupäev == str(None): # kui ei leidnud selgitusest kuupäeva, siis loeb vana väärtuse tagasi
                        kuupäev = rida[2]
                    uus_csv_fail.writerow([kuupäev] + [saaja_maksja] + [summa] + [deebet_krediit])
                elif rida[1] == "82" and deebet_krediit == "D":
                    uus_csv_fail.writerow([kuupäev] + ['Väljaminekud'] + [summa] + [deebet_krediit])
                elif rida[1] == "82" and deebet_krediit == "K":
                    uus_csv_fail.writerow([kuupäev] + ['Sissetulekud'] + [summa] + [deebet_krediit])
                elif rida[1] == "86":
                    uus_csv_fail.writerow([kuupäev] + ['Saldo'] + [summa] + [deebet_krediit])

# loeb csv andmed järjendisse ja tagastab selle, csv peab olema puhastatud
def loe_andmed_csv(csv_fail):
    andmed = []
    with open(csv_fail, newline='', encoding = "UTF-8") as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        next(reader, None) # jätab esimese rea vahele
        for rida in reader:
            andmed.append(rida)
    return andmed

# leiab andmebaasist saaja nime järgi valdkonna
def leia_valdkond_andmebaasist(andmebaas, nimi):
    for rida in andmebaas:
        if rida[0].lower() in nimi.lower():
            return rida[1].strip()
    #print(nimi) # kuvab ekraanile, mis pole andmebaasis
    return "Teadmata"
    
def sorteeri_andmed(andmebaas, andmed):
    sorteeritud = {}
    sorteeritud['Väljeminekute kategooria'] = {}
    sorteeritud['Sissetulekute kategooria'] = {}
    for rida in andmed:
        summa = float(rida[2].replace(',','.'))
        if rida[1] == "Sissetulekud":
            sorteeritud['Sissetulekud'] = summa
        elif rida[1] == "Väljaminekud":
            sorteeritud['Väljaminekud'] = summa
        elif rida[1] == "Saldo":
            sorteeritud['Saldo'] = summa
        else:
            valdkond = leia_valdkond_andmebaasist(andmebaas, rida[1])

            # kulutused
            if rida[3] == "D":
                if valdkond not in sorteeritud['Väljeminekute kategooria']:
                    sorteeritud['Väljeminekute kategooria'][valdkond] = summa
                else:
                    sorteeritud['Väljeminekute kategooria'][valdkond] += summa

            # sissetulekud
            if rida[3] == "K":
                if valdkond not in sorteeritud['Sissetulekute kategooria']:
                    sorteeritud['Sissetulekute kategooria'][valdkond] = summa
                else:
                    sorteeritud['Sissetulekute kategooria'][valdkond] += summa

    return sorteeritud