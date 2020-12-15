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


#lisab poe ja kategooria andmebaasi
def lisa_andmebaasi(failinimi, kategooria, nimi):
    with open(failinimi, "a", encoding = "UTF-8") as fail:
        fail.write(nimi+", "+kategooria.lower().capitalize())


#lisab tundmatud ajutisse andmebaasi
def lisa_tundmatute_andmebaasi(nimi, failinimi = "data/temp.txt"):
    with open(failinimi, "a+", encoding="UTF-8") as fail:
        if len(nimi)>0:
            fail.write(nimi+"\n")


#loeb tundmatud asjutisest andmebaasis
def loe_tundmatute_andmebaasi(failinimi = "data/temp.txt"):
    with open(failinimi, "r", encoding="UTF-8") as fail:
        andmebaas=[]
        for rida in fail:
            rida = rida.strip()
            if rida not in andmebaas:
                andmebaas.append(rida)
        return andmebaas


# https://stackoverflow.com/questions/3276180/extracting-date-from-a-string-in-python
import re
#from datetime import datetime
def leia_kuupäev_tekstist(tekst):
    try:
        if "." in tekst:
            kp = re.search(r'\d{2}-\d{2}-\d{2}', tekst.replace('.','-')).group(0).replace('-','.')
            kp = kp[:6] + "20" + kp[6:] # fix
        else:
            kp = re.search(r'\d{2}/\d{2}/\d{4}', tekst).group(0).replace('/','.')
        return kp
    except:
        return None


def swedbank_või_seb(csvlugemiseks):
    for rida in csv.reader(csvlugemiseks, delimiter=';'):
        if rida[1] == "Reatüüp":
            return "Swedbank"
        return "SEB"
            
def swedbank_csv(csvlugemiseks, csvkirjutamiseks):
    uus_csv_fail = csv.writer(csvkirjutamiseks, delimiter=';')
    uus_csv_fail.writerow(['Kuupäev'] + ['Saaja/Maksja'] + ['Summa'] + ['Deebet/Krediit'])
    for rida in csv.reader(csvlugemiseks, delimiter=';'):
        
        # 10 - algsaldo 20 - tehingud  82 - sissetulek/väljaminek 86 - lõppsaldo
        kategooria = rida[1]
        kuupäev = rida[2]
        saaja_maksja = rida[3]
        selgitus = rida[4]
        summa = round(float(rida[5].replace(',','.')), 2)
        deebet_krediit = rida[7]
        
        # proovib selgitusest võtta kuupäeva
        kuupäev_temp = leia_kuupäev_tekstist(selgitus)
        if kuupäev_temp != None:
            kuupäev = kuupäev_temp
                
        # 10 - algsaldo 20 - tehingud  82 - sissetulek/väljaminek 86 - lõppsaldo
        if kategooria == "20":
            uus_csv_fail.writerow([kuupäev] + [saaja_maksja] + [summa] + [deebet_krediit])
        elif kategooria == "82" and deebet_krediit == "D":
            uus_csv_fail.writerow([kuupäev] + ['Väljaminekud'] + [summa] + [deebet_krediit])
        elif kategooria == "82" and deebet_krediit == "K":
            uus_csv_fail.writerow([kuupäev] + ['Sissetulekud'] + [summa] + [deebet_krediit])
        elif kategooria == "86":
            uus_csv_fail.writerow([kuupäev] + ['Saldo'] + [summa] + [deebet_krediit])
            
def seb_csv(csvlugemiseks, csvkirjutamiseks):
    uus_csv_fail = csv.writer(csvkirjutamiseks, delimiter=';')
    uus_csv_fail.writerow(['Kuupäev'] + ['Saaja/Maksja'] + ['Summa'] + ['Deebet/Krediit'])
    deebet = 0
    krediit = 0
    kuupäev = 0
    for rida in csv.reader(csvlugemiseks, delimiter=';'):
        try:  
            kuupäev = rida[2]
            saaja_maksja = rida[4]
            selgitus = rida[11]
            summa = round(float(rida[8].replace(',','.')), 2)
            deebet_krediit = rida[7]
                
            # proovib selgitusest võtta kuupäeva
            kuupäev_temp = leia_kuupäev_tekstist(selgitus)
            if kuupäev_temp != None:
                kuupäev = kuupäev_temp
                
            uus_csv_fail.writerow([kuupäev] + [saaja_maksja] + [summa] + [deebet_krediit])
            if deebet_krediit == "D":
                deebet += summa
            elif deebet_krediit == "C":
                krediit += summa
        except:
            pass
    uus_csv_fail.writerow([kuupäev] + ['Väljaminekud'] + [round(deebet, 2)] + ["D"])
    uus_csv_fail.writerow([kuupäev] + ['Sissetulekud'] + [round(krediit, 2)] + ["K"])
    uus_csv_fail.writerow([kuupäev] + ['Saldo'] + ["0"] + ["K"])

# võtab argumendiks csv faili, puhastab selle ning kirjutab uude faili
def puhasta_csv_fail(csv_fail, puhastatud_csv_fail):
    with open(csv_fail, 'r', newline='', encoding = "UTF-8") as csvlugemiseks:
        with open(puhastatud_csv_fail, 'w', newline='', encoding = "UTF-8") as csvkirjutamiseks:
            if swedbank_või_seb(csvlugemiseks) == "Swedbank":
                swedbank_csv(csvlugemiseks, csvkirjutamiseks)
            else: # SEB
                seb_csv(csvlugemiseks, csvkirjutamiseks)
                

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
    lisa_tundmatute_andmebaasi(nimi)
    return "Teadmata"
    
def sorteeri_andmed(andmebaas, andmed):
    sorteeritud = {}
    sorteeritud['Väljeminekute kategooria'] = {}
    sorteeritud['Sissetulekute kategooria'] = {}
    
    for rida in andmed: 
        kategooria = rida[1]
        summa = float(rida[2])
        deebet_krediit = rida[3]
        if kategooria == "Sissetulekud":
            sorteeritud['Sissetulekud'] = summa
        elif kategooria == "Väljaminekud":
            sorteeritud['Väljaminekud'] = summa
        elif kategooria == "Saldo":
            sorteeritud['Saldo'] = summa
        else:
            valdkond = leia_valdkond_andmebaasist(andmebaas, kategooria)

            # kulutused
            if deebet_krediit == "D":
                if valdkond not in sorteeritud['Väljeminekute kategooria']:
                    sorteeritud['Väljeminekute kategooria'][valdkond] = summa
                else:
                    sorteeritud['Väljeminekute kategooria'][valdkond] += summa

            # sissetulekud | K - Swedbank | C - SEB
            if deebet_krediit == "K" or deebet_krediit == "C":
                if valdkond not in sorteeritud['Sissetulekute kategooria']:
                    sorteeritud['Sissetulekute kategooria'][valdkond] = summa
                else:
                    sorteeritud['Sissetulekute kategooria'][valdkond] += summa

    return sorteeritud