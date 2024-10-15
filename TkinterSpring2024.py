import tkinter as tk
from tkinter import ttk
import pandas as pd
import matplotlib.pyplot as plt


class dataFramesGui:
    def __init__(self, dataName, dataPanda):
        self.dataPanda = dataPanda
        print(self.dataPanda)

        self.root = tk.Tk()
        self.root.title(dataName)
        self.root.geometry("600x310")

        self.tabControl = ttk.Notebook(self.root)
        self.tabControl.pack(expand=True, fill="both")

        self.style = ttk.Style(self.root)
        self.style.theme_use('clam')
        self.style.configure("Treeview.Heading",
                             background="#a4b0cb",
                             foreground="black",
                             relief="flat")
        self.style.configure("Treeview",
                             background="white smoke",
                             fieldbackground="white smoke",
                             rowheight=25)
        self.style.map('Treeview', background=[('selected', 'gray')])

        self.createPage1()
        self.createPage2()
        self.createPage3()

    def createPage1(self):
        page1 = ttk.Frame(self.tabControl)
        self.tabControl.add(page1, text="Page 1")

        label = tk.Label(page1, text="DataFrame View", bg="#dbdad5")
        label.pack()

        pandaText = tk.Text(page1)
        pandaText.insert('1.0', self.dataPanda.to_string())
        pandaText.pack(expand=True, fill='both')

    def createPage2(self):
        page2 = ttk.Frame(self.tabControl)
        self.tabControl.add(page2, text="Page 2")

        label = tk.Label(page2, text="Column and row headers",  bg="#dbdad5")
        label.pack()

        listbox = ttk.Treeview(page2, columns=('Name', 'Distance', 'Orbital Period'), show='headings')

        listbox.heading('Name', text='   Name', anchor='w')
        listbox.heading('Distance', text='Distance (AU)', anchor='center')
        listbox.heading('Orbital Period', text='Orbital Period (Years)', anchor='center')

        for index, row in self.dataPanda.iterrows():
            addSpace = '   ' + row['Dwarf']
            listbox.insert('', 'end', values=(addSpace, row['Distance(AU)'], row['Period(years)']))

        listbox.column('Name', width=60)
        listbox.column('Distance', anchor='center')
        listbox.column('Orbital Period', anchor='center')

        listbox.pack(expand=True, fill='both')

    def createPage3(self):
        page3 = ttk.Frame(self.tabControl)
        self.tabControl.add(page3, text="Page 3")

        label = tk.Label(page3, text="Column and row indices", bg="#dbdad5")
        label.pack()

        listbox = ttk.Treeview(page3, columns=('Index', 'Name', 'Distance', 'Orbital Period'), show='headings')

        listbox.heading('Index', text='Index')
        listbox.heading('Name', text='Name', anchor='w')
        listbox.heading('Distance', text='Distance (AU)', anchor='center')
        listbox.heading('Orbital Period', text='Orbital Period (Years)', anchor='center')

        for index, row in self.dataPanda.iterrows():
            listbox.insert('', 'end', values=(index, row['Dwarf'], row['Distance(AU)'], row['Period(years)']))

        listbox.column('Index', anchor='center', width=50)
        listbox.column('Name', width=100)
        listbox.column('Distance', anchor='center', width=225)
        listbox.column('Orbital Period', anchor='center', width=225)

        listbox.pack()

    def run(self):
        self.root.mainloop()

class createDataPanda:
    def __init__(self, filepath):
        self.filepath = filepath
        self.panda = None

    def parseData(self):
        self.panda = pd.read_csv(self.filepath)

    def printPanda(self):
        print(self.panda)

    def runPanda(self):
        self.parseData()
        # self.printPanda()


if __name__ == "__main__":
    fileName = 'Dwarfs.csv'

    scrap = createDataPanda(fileName)
    scrap.runPanda()

    dataPanda = scrap.panda
    # print(dataPanda)

    gui = dataFramesGui("Dwarf Planets", dataPanda)
    gui.run()
