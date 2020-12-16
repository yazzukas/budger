# Budger
# Sten Ambus, Kaur Vali, 2020

from tkinter import *
from tkinter import filedialog
from tkinter import scrolledtext
import os
import andmete_sorteerimine as a


global esimene
esimene = True

def vali_fail():
    global fail
    fail = filedialog.askopenfilename(filetypes=(("CSV failid", "*.csv"), ("all files", "*.*")))
    if fail:
        l2.configure(text="Nüüd vali kuhu puhastatud fail salvestada!")
        b.configure(text="Salvesta fail", command=vali_kaust)


def vali_kaust():
    global kaust
    kaust = filedialog.askdirectory()
    if kaust:
        b.pack_forget()
        kuvamine()


def sulge_fail():
    if os.path.exists("data/temp.txt"):
        os.remove("data/temp.txt")


def sulge():
    sulge_fail()
    raam.destroy()


def re_kuvamine():
    global esimene
    esimene=False
    kuvamine()


def kuvamine():
    sulge_fail()

    global fail, kaust
    global l3, l4
    global esimene
    if not esimene:
        b2.pack_forget()
        b3.pack_forget()
        l5.pack_forget()
        ent1.pack_forget()
        lbl1.pack_forget()
        ent1.delete(0, 'end')
        l5.delete(0, 'end')
        l5.destroy()

    # backendis sorteerimine
    andmebaas = a.loe_andmebaas('data/andmebaas.txt')
    salvestuskaust = kaust + "/puhastatud.csv"
    a.puhasta_csv_fail(fail, salvestuskaust)
    sorteeritud_andmed = a.sorteeri_andmed(andmebaas, a.loe_andmed_csv(salvestuskaust))

    # peainfo ekraanile kuvamine
    l2.configure(text="Sellel perioodil oli sissetulek " + str(sorteeritud_andmed['Sissetulekud']) + " eurot.\n"
                    "Sellel perioodil oli väljaminek " + str(sorteeritud_andmed['Väljaminekud']) + " eurot.\n"
                    "Sellel perioodil oli kasum/kahju " + str(round(sorteeritud_andmed['Sissetulekud'] - sorteeritud_andmed['Väljaminekud'], 2)) + " eurot.\n"
                    "Sellel perioodi lõpuks oli kontojääk " + str(sorteeritud_andmed['Saldo']) + " eurot.")

    l3_text = StringVar()
    l3 = Label(raam, text="Väljaminekute kategooriad: ", textvariable=l3_text)
    l4_text = StringVar()
    l4 = Label(raam, text="Sissetulekute kategooriad: ", textvariable=l4_text)

    # https://stackoverflow.com/questions/613183/how-do-i-sort-a-dictionary-by-value
    kategooriad_väljaminek = {k: v for k, v in sorted(sorteeritud_andmed['Väljeminekute kategooria'].items(), key=lambda item: item[1], reverse=True)}
    kategooriad_sissetulek = {k: v for k, v in sorted(sorteeritud_andmed['Sissetulekute kategooria'].items(), key=lambda item: item[1], reverse=True)}
    for i in kategooriad_väljaminek:
        s = l3_text.get()
        s = s + str(i) + ": " + str(round(kategooriad_väljaminek[i], 2)) + " eurot.\n"
        l3_text.set(s)

    for i in kategooriad_sissetulek:
        s = l4_text.get()
        s = s + str(i) + ": " + str(round(kategooriad_sissetulek[i], 2)) + " eurot.\n"
        l4_text.set(s)

    b2.configure(text="Vaata teadmatuid", command=näita_tundmatu)
    l3.config(font=("Avenir", 12))
    l4.config(font=("Avenir", 12))
    l2.pack(pady=(10, 10))
    l3.pack()
    l4.pack()
    b2.pack()
    raam.geometry("800x700")


# kuvab tundmatud ja võimaldab lisada tundmatu
def näita_tundmatu():
    global l5

    l2.pack_forget()
    l3.destroy()
    l4.destroy()
    b2.pack_forget()

    l2.configure(text="Andmebaasi lisamiseks vali listist nimi ning kirjuta alla kasti sellele kategooria!")
    b3.configure(command=vali_tundmatu)

    l2.pack()
    l5 = Listbox(raam)
    l5.pack(padx=50, pady=(10, 0))
    l5.config(width=200)
    b2.configure(text="Tagasi", command=re_kuvamine)

    for i in a.loe_tundmatute_andmebaasi():
        l5.insert(END, i+"\n")

    lbl1.pack()
    ent1.pack()
    b3.pack()
    b2.pack()
    raam.geometry("800x600")


# lisab valitud tundmatu andmebaasi
def vali_tundmatu():
    nimi = l5.get(l5.curselection())
    kategooria = ent1.get()

    if len(nimi)>0 and len(kategooria)>0:
        l2.configure(text="Andmebaasi lisamine oli edukas!")
        ent1.pack_forget()
        lbl1.pack_forget()
        l5.pack_forget()
        b3.pack_forget()
        b2.pack_forget()
        b2.pack()
        a.lisa_andmebaasi(kategooria, nimi)


# tkinteri alustamine
raam = Tk()
raam.title("Budger")
# raam.iconitmap("link pildile") icon nurka
raam.geometry("800x400")

# sisu
logo = Label(raam, text="Budger")
l1 = Label(raam, text="Aitab sul planeerida raha ning seeläbi täita unistused!")
l2 = Label(raam, text="Budger kuvab sulle ekraanile sissetulekud, väljaminekud koos kategooriatega ning kontosaldo\n\n"
                      "Alustuseks avame .csv faili, mille sa saad pangast*!\n"
                      "(*hetkel teadaolevalt toimib Swedbank ja SEB)")

# kategooriatesse lisamine
lbl1 = Label(raam, text="Kategooria")
ent1 = Entry(raam)

# nupud
b = Button(raam, text="Ava fail", command=vali_fail)
b2 = Button(raam, text="Vaata teadmatuid", command=näita_tundmatu)
b3 = Button(raam, text="Saada", command=näita_tundmatu)

# font jms info
l1.config(font=("Avenir", 16))
l2.config(font=("Avenir", 16))
logo.config(font=("Avenir", 48))

# widgetite tekitamine
logo.pack(pady=(10, 10))
l1.pack()
l2.pack(pady=(10, 10))
b.pack(pady=(0, 10))

# jooksutamine ja sulgemisel temp.txt kustutamine
raam.protocol("WM_DELETE_WINDOW", sulge)
raam.mainloop()
