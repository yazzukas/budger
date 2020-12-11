from tkinter import *
from tkinter import filedialog
from tkinter import scrolledtext
import andmete_sorteerimine as a

def kuvamine():
    global fail, kaust

    #backendis sorteerimine
    andmebaas = a.loe_andmebaas('test files/andmebaas.txt')
    salvestuskaust = kaust + "/puhastatud.csv"
    a.puhasta_csv_fail(fail, salvestuskaust)
    print(kaust, salvestuskaust)
    sorteeritud_andmed = a.sorteeri_andmed(andmebaas, a.loe_andmed_csv(salvestuskaust))

    #peainfo ekraanile kuvamine
    l2.configure(text="Sellel perioodil oli sissetulek " + str(sorteeritud_andmed['Sissetulekud']) + " eurot.\n"
                    "Sellel perioodil oli väljaminek " + str(sorteeritud_andmed['Väljaminekud']) + " eurot.\n"
                    "Sellel perioodil oli kasum/kahju " + str(round(sorteeritud_andmed['Sissetulekud']-sorteeritud_andmed['Väljaminekud'],2)) + " eurot.\n"                                                                               
                    "Sellel perioodi lõpuks oli kontojääk " + str(sorteeritud_andmed['Saldo']) + " eurot.")

    # https://stackoverflow.com/questions/613183/how-do-i-sort-a-dictionary-by-value
    kategooriad_väljaminek = {k: v for k, v in
                              sorted(sorteeritud_andmed['Väljeminekute kategooria'].items(), key=lambda item: item[1],
                                     reverse=True)}
    kategooriad_sissetulek = {k: v for k, v in
                              sorted(sorteeritud_andmed['Sissetulekute kategooria'].items(), key=lambda item: item[1],
                                     reverse=True)}
    for i in kategooriad_väljaminek:
        global l3_text
        s = l3_text.get()
        s = s + str(i) + ": " + str(round(kategooriad_väljaminek[i], 2)) + " eurot.\n"
        l3_text.set(s)

    for i in kategooriad_sissetulek:
        global l4_text
        s = l4_text.get()
        s = s + str(i) + ": " + str(round(kategooriad_sissetulek[i], 2)) + " eurot.\n"
        l4_text.set(s)

    l3.pack()
    l4.pack()
    raam.geometry("800x600")



def vali_fail():
    global fail
    fail = filedialog.askopenfilename(filetypes=(("CSV failid", "*.csv"),("all files","*.*")))
    if fail:
        l2.configure(text = "Nüüd vali kuhu puhastatud fail salvestada!")
        b.configure(text="Salvesta fail", command = vali_kaust)


def vali_kaust():
    global kaust
    kaust = filedialog.askdirectory()
    if kaust:
        b.pack_forget()
        kuvamine()

#tkinteri alustamine
raam = Tk()
raam.title("Budger")
#raam.iconitmap("link pildile") icon nurka
raam.geometry("800x400")

#sisu
logo = Label(raam, text="Budger")
l1 = Label(raam, text = "Aitab sul planeerida raha ning seeläbi täita unistused!")
l2 = Label(raam, text = "Budger kuvab sulle ekraanile sissetulekud, väljaminekud koos kategooriatega ning kontosaldo\n\n"
                        "Alustuseks avame .csv faili, mille sa saad pangast*!\n(*hetkel teadaolevalt toimib swedbank)")
l3_text = StringVar()
l3 = Label(raam, text="Väljaminekute kategooriad: ", textvariable=l3_text)

l4_text = StringVar()
l4 = Label(raam,  text="Sissetulekute kategooriad: ", textvariable=l4_text)

b = Button(raam, text="Ava fail", command = vali_fail)

#font jms info
l1.config(font =("Avenir", 16))
l2.config(font =("Avenir", 16))
l3.config(font =("Avenir", 12))
l4.config(font =("Avenir", 12))
logo.config(font =("Avenir", 48))

#widgetite tekitamine
logo.pack(pady=(10, 10))
l1.pack()
l2.pack(pady=(10, 10))
b.pack(pady=(0, 10))

raam.mainloop()
