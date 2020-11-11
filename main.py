#Budger
#Sten Ambus, Kaur Vali, 2020

import andmete_sorteerimine as a

#failinimi = input("Sisestage faili nimi, millest soovite lugeda: ")
andmebaas = a.loe_andmebaas('test files/andmebaas.txt')
a.puhasta_csv_fail('test files/Budger sample.csv', 'test files/puhastatud.csv')
sorteeritud_andmed = a.sorteeri_andmed(andmebaas, a.loe_andmed_csv('test files/puhastatud.csv'))

#print(andmebaas)
#print(sorteeritud_andmed)
#print()
print("Sellel perioodil oli sissetulek " + str(sorteeritud_andmed['Sissetulekud']) + " eurot.")
print("Sellel perioodil oli väljaminek " + str(sorteeritud_andmed['Väljaminekud']) + " eurot.")
print("Sellel perioodi lõpuks oli kontojääk " + str(sorteeritud_andmed['Saldo']) + " eurot.")
print()
print("Kulutuste kategooriad:")

# https://stackoverflow.com/questions/613183/how-do-i-sort-a-dictionary-by-value
kategooriad_väljaminek = {k: v for k, v in sorted(sorteeritud_andmed['Väljeminekute kategooria'].items(), key=lambda item: item[1], reverse=True)}
for i in kategooriad_väljaminek:
    print(i+":", round(kategooriad_väljaminek[i],2), "eurot.")

print()
print("Sissetulekute kategooriad:")

# https://stackoverflow.com/questions/613183/how-do-i-sort-a-dictionary-by-value
kategooriad_sissetulek = {k: v for k, v in sorted(sorteeritud_andmed['Sissetulekute kategooria'].items(), key=lambda item: item[1], reverse=True)}
for i in kategooriad_sissetulek:
    print(i+":", round(kategooriad_sissetulek[i],2), "eurot.")
