#Budger
#Sten Ambus, Kaur Vali, 2020

import andmete_sorteerimine as a

andmebaas = a.loe_andmebaas('test files/andmebaas.txt')
a.puhasta_csv_fail('test files/Budger sample.csv', 'test files/puhastatud.csv')
sorteeritud_andmed = a.sorteeri_andmed(andmebaas, a.loe_andmed_csv('test files/puhastatud.csv'))

print(andmebaas)
print(sorteeritud_andmed)
print()
print("Sellel perioodil oli sissetulek " + str(sorteeritud_andmed['Sissetulekud']) + " eurot.")
print("Sellel perioodil oli väljaminek " + str(sorteeritud_andmed['Väljaminekud']) + " eurot.")
print()


"""
print(sorteeritud_andmed['Toidupood'])

for i in sorteeritud_andmed:
    print(i)
    print(sorteeritud_andmed[i])"""