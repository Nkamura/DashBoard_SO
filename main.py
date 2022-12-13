import subprocess
import tkinter as tk
from tkinter import ttk
import math
iterator = 1
#Func. para atualizar os valores
def updateTop():
    msgTop = subprocess.run(['top', '-b', '-n1'], stdout = subprocess.PIPE)
    #Filtrar para mostrar somente processos executando (Bom verificar se está realmente mostrando igual do terminal)
    #msgTop = subprocess.run(['top', '-bi', '-n1'], stdout = subprocess.PIPE)
    TopList.delete(0, TopList.size())
    strTop = msgTop.stdout.splitlines()
    i = 1
    for lines in strTop:
        TopList.insert(i, lines)
        i = i+ 1
    root.after(2000, updateTop)

def updateMem():
    msgMem = subprocess.run(['free'], stdout = subprocess.PIPE)
    stringMem = msgMem.stdout.split()
    total = int(stringMem[7].decode("utf-8"))
    pieV[0] = (int(stringMem[8].decode("utf-8")) / total) * 100
    pieV[1] = (int(stringMem[9].decode("utf-8")) / total) * 100
    pieV[2] = (int(stringMem[11].decode("utf-8")) / total) * 100
    labelMem["text"]=msgMem.stdout
    root.after(2000, updateMem)
def openTerminal():
    subprocess.Popen("gnome-terminal")

def angle(n):
    return 360*n/1000

def createPieChar():
    angle1 = angle(pieV[0]*10)
    angle2 = angle(pieV[1]*10)
    angle3 = angle(pieV[2]*10)

    canvas.create_arc((200, 10, 600, 400), fill="red", outline="red", start=angle(0), extent=angle1)
    canvas.create_arc((200, 10, 600, 400), fill="green", outline="green", start=angle1, extent=angle2)
    canvas.create_arc((200, 10, 600, 400), fill="blue", outline="blue", start=angle1+angle2, extent=angle3)
    root.after(2000, createPieChar)


root = tk.Tk()
root.geometry('800x600')
root.title('Linux Dashboard')
# add widgets here


mainframe = ttk.Frame(root, width=800, height=600)
mainframe.pack()
notebook = ttk.Notebook(mainframe)
notebook.pack()

#Criação dos frames do DashBoard
frame1 = ttk.Frame(notebook, width=800, height=600)
#Duas janelas dentro da janela 1
sNotebook = ttk.Notebook(frame1, width=800, height=600)
sFrame1 = ttk.Frame(sNotebook, width=800, height=600)
sFrame2 = ttk.Frame(sNotebook, width=800, height=600)
frame2 = ttk.Frame(notebook, width=800, height=600)
frame3 = ttk.Frame(notebook, width=800, height=600)
frame4 = ttk.Frame(notebook, width=800, height=600)
frame5 = ttk.Frame(notebook, width=800, height=600)
TopList = tk.Listbox(notebook, width=800, height=600)
scrollbar = tk.Scrollbar(TopList)
scrollbar.pack(side="right", fill="both")

TopList.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=TopList.yview)

terminalButton = ttk.Button(frame5, text='Terminal', command=openTerminal)
terminalButton.pack()

canvas = tk.Canvas(frame3, width=800, height=400)

#Comandos que serão utilizados
#shell=True para rodar o comando da linha inteira sem ter que quebrar
msghrdwr = subprocess.run("lscpu | grep -v 'Vulnerability\|Flags' | sed 's/  */ /g'", shell=True, stdout=subprocess.PIPE)
#Mudei o lugar que esta puxando as info. no proc vem mais "completo"
#msgSO = subprocess.run(["uname", '-a'], stdout = subprocess.PIPE)
msgSO = subprocess.run(['cat', '/proc/version'], stdout = subprocess.PIPE)
msgMem = subprocess.run(['free'], stdout = subprocess.PIPE)
stringMem = msgMem.stdout.split()
pieV = {}
total = int(stringMem[7].decode("utf-8"))
pieV[0] = (int(stringMem[8].decode("utf-8")) / total) * 100
pieV[1] = (int(stringMem[9].decode("utf-8")) / total) * 100
pieV[2] = (int(stringMem[11].decode("utf-8")) / total) * 100
createPieChar()
msgPrts = subprocess.run(['df', '-Th'], stdout = subprocess.PIPE)
#Tá para ficar pegando só os processos que estão "sendo usados"
#msgTop = subprocess.run(['top', '-bi', '-n1'], stdout = subprocess.PIPE)
msgTop = subprocess.run(['top', '-b', '-n1'], stdout = subprocess.PIPE)
stringTop = msgTop.stdout.splitlines()
for lines in stringTop:
    TopList.insert(iterator, lines)
    iterator = iterator + 1

labelRam = ttk.Label(frame3, text="Uso de Memória RAM")
labelHrdwr = ttk.Label(sFrame1, text=msghrdwr.stdout)
labelSO = ttk.Label(sFrame2, text=msgSO.stdout, wraplength=800)
labelMem = ttk.Label(frame3, text=msgMem.stdout)
labelPrts = ttk.Label(frame4, text=msgPrts.stdout)
#labelTop = ttk.Label(frame2, text=msgTop.stdout)
labelUsed = ttk.Label(frame3, text="Used", foreground="Red")
labelFree = ttk.Label(frame3, text="Free", foreground="Green")
labelCache = ttk.Label(frame3, text="Buffer/Cache", foreground="Blue")

sNotebook.pack()
labelHrdwr.pack()
labelSO.pack()
#labelTop.pack()
labelRam.pack()
canvas.pack()
labelUsed.pack()
labelFree.pack()
labelCache.pack()
labelMem.pack()
labelPrts.pack()

#Nomeando os Frames
notebook.add(frame1, text='Sistema (hardware e SO)')
sNotebook.add(sFrame2, text='SO')
sNotebook.add(sFrame1, text='Hardware')
notebook.add(TopList, text='Processos/Threads')
notebook.add(frame3, text='Memória')
notebook.add(frame4, text='Sistema de arquivo')
notebook.add(frame5, text='Terminal')

root.after(2000, updateTop)
root.after(2000, updateMem)
root.after(2000, createPieChar())

root.mainloop()



#Janela de Terminal (clicar e abrir o terminal em outra janela)
#Scroll do processos/threads
#Para memória usar o du df também caso possível
#Parte de entrada e saida IO
