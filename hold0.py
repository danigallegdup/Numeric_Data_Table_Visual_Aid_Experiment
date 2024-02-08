import time
from tkinter import *
from PIL import Image, ImageTk
import csv
import tkinter.ttk as ttk
import os

import csv
from time import time,sleep

import pyautogui
import threading
from datetime import date
from threading import Timer


TASK_NAME = 0
TABLE_PIC = 1
TABLE = 2
TASK_ID = 3
TYPE = 4
REP = 5
CONDITION=6
ORDER = 7
C_ANSWER = 8
p_id = 9
c_row = 10
c_col=11
is_end = 12
show_text = 13
av= 14
count = 1
image_number = 0
list_number = 0
tuple_number = 0
mn = 15
is_image = False
paused = True
answer_list =[]
header = False
header_m = False
start_mouse = 1000



is_error = False

file_path = input("Enter participants number: ")
#os.chdir(file_path)
def resize(ev = None):
    
    label.config(text='') #改变字体大小

def show(panel,img):
    global image_number
    global count
    global list_number
    global tree
    global head_list
    global TableMargin
    global i
    global is_image
    global paused
    global oldtime
    global start_time
    global end_time
    global start_time_e
    global end_time_e
    global mouse_checker
    global start_mouse 
    i=0
    start_mouse = 3813 #60 secs: 3813
    pyautogui.moveTo(33, 24)
    ##if image_number == len(a_path):
     ##   image_number = 0
    
    photo = ImageTk.PhotoImage(Image.open(img[list_number][TABLE_PIC]).resize((top.winfo_width(), top.winfo_height())))
    
    label.config(text='')
    label.configure(image=photo)
    label.image =photo

    
    print(img[list_number][TABLE])
    
    if (image_number !=0):
            for widgets in frame.winfo_children():
              widgets.destroy()

    button2 = Button(frame,text ='save',width = 10,height = 5, command=lambda: save_file(img[list_number-1]))
    button2.pack(side= 'left')
    head_list = read_table(img)
    start_time = display2.cget('text')
    
    #TableMargin = Frame(root, width=500)
    #TableMargin.pack(side=TOP)
    #print(TableMargin)
    print(len(head_list))
    scrollbarx = Scrollbar(frame, orient=HORIZONTAL)
    scrollbary = Scrollbar(frame, orient=VERTICAL)
    tree = ttk.Treeview(frame, columns=(head_list[0] ,head_list[1],head_list[2],head_list[3] ,head_list[4],head_list[5],
        head_list[6] ,head_list[7],head_list[8],head_list[9] ,head_list[10],head_list[11]), height=400, selectmode="extended", yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set)
    scrollbary.config(command=tree.yview)
    scrollbary.pack(side=RIGHT, fill=Y)
    scrollbarx.config(command=tree.xview)
    scrollbarx.pack(side=BOTTOM, fill=X)
    tree.heading(head_list[0], text=head_list[0], anchor=W)
    tree.heading(head_list[1], text=head_list[1], anchor=W)
    tree.heading(head_list[2], text=head_list[2], anchor=W)
    tree.heading(head_list[3], text=head_list[3], anchor=W)
    tree.heading(head_list[4], text=head_list[4], anchor=W)
    tree.heading(head_list[5], text=head_list[5], anchor=W)
    tree.heading(head_list[6], text=head_list[6], anchor=W)
    tree.heading(head_list[7], text=head_list[7], anchor=W)
    tree.heading(head_list[8], text=head_list[8], anchor=W)
    tree.heading(head_list[9], text=head_list[9], anchor=W)
    tree.heading(head_list[10], text=head_list[10], anchor=W)
    tree.heading(head_list[11], text=head_list[11], anchor=W)
    
    tree.bind('<ButtonRelease-1>', selectItem)
    tree.column('#0', stretch=NO, minwidth=0, width=0)

    tree.pack()
    print(tree)
    start_time_e = (time())*1000
    i= 0
    mouse_checker = True

    with open(img[list_number][TABLE]) as f:
        reader = csv.DictReader(f, delimiter=',')
        for row in reader:
            colum1 = row[head_list[0]]
            colum2 = row[head_list[1]]
            colum3 = row[head_list[2]]
            colum4 = row[head_list[3]]
            colum5 = row[head_list[4]]
            colum6 = row[head_list[5]]
            colum7 = row[head_list[6]]
            colum8 = row[head_list[7]]
            colum9 = row[head_list[8]]
            colum10 = row[head_list[9]]
            colum11 = row[head_list[10]]
            colum12 = row[head_list[11]]


            tree.insert("", i, iid=i+1, values=(colum1,colum2,colum3,colum4,colum5,colum6,colum7,colum8,colum9,colum10,colum11,colum12))
            i = i+1
        print(count)
    print(head_list)
    count = count+1
    list_number= list_number + 1
    image_number += 1
    i=i+1
    is_image = True

    paused = False
    oldtime = time()
    run_timer()
    save_mouse()
    print(start_time)
    temp = 10

    

   

   # r and c tell us where to grid the labels


        
    
    
    
def save_file(file):
    global header
    global is_error
    print(str(True))
    file_handle = open(file_path + "/result.csv", 'a')
    if(header == False):
        file_handle.write('participant ID'+','+'P_answer'+','+'start time'+','+'end time'+','+'start time_e'+','+'end time_e'+','+'start time_t'+','+'time spent'+','+'Task ID'+','+'trial'+','+'Repetition'+','+'Condition'+','+'Order of table'+','+'Correct Answer'+','+'col'+','+'row'+','+'Answer row'+','+'Answer column'+','+'error'+','+'isPerfect'+','+'ans_value'+'\n')

    
    for p in answer_list:
        file_handle.write(str(file[p_id])+','+str(p[0]) + ',' + str(start_time)+','+str(end_time)+','+str(start_time_e)+','+str(end_time_e)+','+str(start_time_t)+','+ str((end_time_e-start_time_e)/1000) + ','+ str(file[TASK_ID])+',' +str(file[mn]) +',' 
        + str(file[REP]) +','+ str(file[CONDITION]) +','+ str(file[ORDER]) +','+str(file[C_ANSWER])+','+str(col)+','+str(ro)+','+str(file[c_row])+','+str(file[c_col])+','+str(is_error)+','+str(str(p[0])==str(file[C_ANSWER]))+','+str(file[av])+'\n')
    
    file_handle.close()
    is_error = False
    header = True
def white(p):
    global is_image
    global paused
    global end_time
    global end_time_e
    global mouse_checker

   
    mouse_checker = False
    if p[list_number-1][is_end]:
        label.config(image='')
        label.config(fg="blue",text=str(p[list_number-1][show_text]),font='Helvetica -35')
    else:
        label.config(image='')    
        label.config(fg="red",text="Please don't click or press on anything and wait for experimenter's response.",font='Helvetica -55')
        
        

    is_image = False
    paused = True
    oldtime = time()
    end_time = display2.cget('text')
    end_time_e = (time())*1000
def save_mouse():

    global header_m
    
    global start_mouse 
    if mouse_checker == False:
        header_m = True
        ##start_mouse = (time())*1000
        return 

    else:
        global t

        if test_l[list_number-1][TYPE] == "Describing" and start_mouse <0:
            pyautogui.press("space")
            
            
            
        start_mouse -=1
        file_handle = open(file_path+'/'+'mouse/'+test_l[list_number-1][mn]+'-'+str(date.today())+'-'+str(start_time_e)+'.csv','a')
        if header_m == False:
            file_handle.write('trial'+','+'timestamp'+','+'x'+','+'y'+'\n')
        file_handle.write(str(test_l[list_number-1][mn])+','+str((time())*1000)+','+str(pyautogui.position().x)+','+str(pyautogui.position().y)+'\n')
        ##print(str(pyautogui.position()))
    
        t= threading.Timer(0.001, save_mouse)
        t.start()
        header_m = True
        
            
    
def wai_t():
    print("waiting")
def change_task(task):
    global test_l
    global count
    global list_number
    global tuple_number
    global oldtime2
    global start_time_t
    global t
    global header_m

    header_m = False
    #print(type(task[list_number][TASK_NAME]))
    start_time_t = (time())*1000
    display.config(text='00:00')
    label.config(image='')
    label.config(fg="black",text='\n'*10+str(task[list_number][TASK_NAME])+'\n'*20+test_l[list_number][TASK_ID],font='Helvetica -35')
    print(task[list_number][TASK_NAME])
    
    count = count +1
    print('aa')
def close(): #关闭两个窗口

    top.destroy()

    root.destroy()
def read_csv(filename):
    task_list =[]
    my_list = []
    with open(filename, newline='\n') as f:
        #file_handle = open(filename, 'r')
        next(f)
        csv_reader = csv.reader(f)
        for row in csv_reader:
            
            print (str(row[TASK_NAME]))
            #line = line.rstrip()
            #list_of_words = line.split(',')
            TN = row[TASK_NAME]
            TP = row[TABLE_PIC]
            T = row[TABLE]
            ID = row[TASK_ID]
            TYP = row[TYPE]
            REPE = row[REP]
            CON = row[CONDITION]
            ORD = row[ORDER]
            CANS = row[C_ANSWER]
            pid = row[p_id]
            crow = row[c_row]
            ccol = row[c_col]
            end = row[is_end]
            st = row[show_text]
            ans_value = row[av]
            mouse_name = row[mn]

            task_list.append((TN,TP,T,ID,TYP,REPE,CON,ORD,CANS,pid,crow,ccol,end,st,ans_value,mouse_name))

        #file_handle.close()

        print(my_list)
        
        return task_list
        

#FM

test_l = read_csv(file_path+'/'+file_path + 'input.csv')
top = Tk()
print(test_l)
top.attributes("-fullscreen", True)




def go_back():
    global list_number
    global image_number
    global is_error
    list_number = list_number -1
    image_number = image_number -1
    is_error = True
    
top.geometry('2000x2000')

label=Label(top,fg="red",text="Thank you for your participation, please be patient and wait for experimenter's response.",wraplength=1000, font='Helvetica -55',justify=LEFT)
label.pack()

label.pack(fill=X, expand=1)
panel = Label(top)
panel.pack(side = "bottom", fill = "both", expand = "yes")







def run_timer():
        global oldtime
        if paused:
            return
        delta = int(time() - oldtime)
        #print('1')
        timestr = '{:02}:{:02}'.format(*divmod(delta, 60))
        display.config(text=timestr)
        display.after(1000, run_timer)

def run_timer2():
        
        delta = int(time() - oldtime2)
        #print('1')
        timestr = '{:02}:{:02}'.format(*divmod(delta, 60))
        display2.config(text=timestr)
        display2.after(1000, run_timer2)
def selectItem(event):
        count = 0
        global col
        global ro
        curItem = tree.item(tree.focus())
        col = tree.identify_column(event.x)
        ro = tree.identify_row(event.y)
        print ('curItem = ', curItem)
        print ('col = ', col)
        print ('row = ', ro)
        global answer_list
        

        if col == '#0':
            cell_value = curItem['text']
        elif col == '#1':
            cell_value = curItem['values'][0]
            
        elif col == '#2':
            cell_value = curItem['values'][1]
            count = 1
        elif col == '#3':
            cell_value = curItem['values'][2]
        elif col == '#4':
            cell_value = curItem['values'][3]
        elif col == '#5':
            cell_value = curItem['values'][4]
        elif col == '#6':
            cell_value = curItem['values'][5]
        elif col == '#7':
            cell_value = curItem['values'][6]
        elif col == '#8':
            cell_value = curItem['values'][7]
        elif col == '#9':
            cell_value = curItem['values'][8]
        elif col == '#10':
            cell_value = curItem['values'][9]
        elif col == '#11':
            cell_value = curItem['values'][10]
        elif col == '#12':
            cell_value = curItem['values'][11]
        

        print('row:', curItem['values'])
        print ('cell_value = ', cell_value)
        
        answer_list = [(cell_value,display.cget('text'))]
        

def read_table(tablel):
    
    file_handle = open(tablel[list_number][TABLE],'r')
    for line in file_handle:
        line = line.rstrip()
        list_of_words = line.split(',')
        print(list_of_words)
        break
    
   

    return list_of_words



    
root = Tk()

root.title("Python - Import CSV File To Tkinter Table")
width = 100
height = 100
frame = Frame(root)
frame.pack(side="top", expand=True, fill="both")
frame2 = Frame(root)
frame2.pack(side="bottom", expand=True, fill="both")
display = Label(frame2, text='00:00', width=100)
display2 = Label(frame2, text='00:00', width=100)
display3 = Label(frame2, text='', width=100)
#display.pack(side="bottom")
f_save = Label(frame2, text='', width = 100)
f_save.pack(side="left")
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width/2) - (width/2)
y = (screen_height/2) - (height/2)
oldtime2 = time()
run_timer2()





root.geometry('2000x2000')

##button = Button(top,text ='click',width = 10,height = 5, command = lambda:white() if(is_image) else (show(panel,test_l) if(count%2==0) else change_task(test_l)))

##button.pack( side= 'left')
second=StringVar()
top.bind("<space>", lambda x:white(test_l) if(is_image) else (show(panel,test_l) if(count%2==0) else change_task(test_l)))
top.bind("<Tab>", lambda x :go_back())

top.protocol("WM_DELETE_WINDOW", close)#只要其中一个窗口关闭,就同时关闭两个窗口

root.protocol("WM_DELETE_WINDOW", close)#只要其中一个窗口关闭,就同时关闭两个窗口

mainloop()



