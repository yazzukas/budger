#Budger
#Sten Ambus, Kaur Vali, 2020

import andmete_sorteerimine as a

#failinimi = input("Sisestage faili nimi, millest soovite lugeda: ")
andmebaas = a.loe_andmebaas('test files/andmebaas.txt')
a.puhasta_csv_fail('test files/statement.csv', 'test files/puhastatud.csv')
sorteeritud_andmed = a.sorteeri_andmed(andmebaas, a.loe_andmed_csv('test files/puhastatud.csv'))

#print(andmebaas)
#print(sorteeritud_andmed)
#print()
print("Sellel perioodil oli sissetulek " + str(sorteeritud_andmed['Sissetulekud']) + " eurot.")
print("Sellel perioodil oli väljaminek " + str(sorteeritud_andmed['Väljaminekud']) + " eurot.")
print()
print("Kulutuste kategooriad:")

kategooriad = {k: v for k, v in sorted(sorteeritud_andmed.items(), key=lambda item: item[1], reverse=True)}
for i in kategooriad:
    print(i+":", round(kategooriad[i],2), "eurot.")
