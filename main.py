#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from tkinter import *
from tkinter import ttk
import tkinter.filedialog
from pandas import read_csv,DataFrame
import numpy as np
from ray import ray
import matplotlib.pyplot as plt

def trace(initial_ray):
    # calculation efficiency
    dt = 0.01
    if inpi.get()!='':
        Max_Steps = int(inpi.get())
    else :
        Max_Steps = 1000

    rayslist = []
    nthray = 0
    raynum = len(initial_ray)
        
    for r0 in initial_ray:
        s = 'tracing '+str(nthray)+'/'+str(raynum)+' rays ...'
        lbtask.config(text=s)
        lbtask.update()

        oneray = []
        oneray.append(r0)

        for j in range(0,Max_Steps):
            A = dt*getD(oneray[j].r)
            B = dt*getD(oneray[j].r+0.5*dt*getT(oneray[j].r,oneray[j].s)+0.125*dt*A)
            C = dt*getD(oneray[j].r+dt*getT(oneray[j].r,oneray[j].s)+0.5*dt*B)
            nextT = getT(oneray[j].r,oneray[j].s)+1/6*(A+4*B+C)
            nextr = oneray[j].r+dt*(getT(oneray[j].r,oneray[j].s)+1/6*(A+2*B))
            nexts = nextT/getn(nextr)
            nextray = ray()
            nextray.r = nextr
            nextray.s = nexts
            oneray.append(nextray)

        rayslist.append(oneray)
        nthray = nthray + 1
    lbtask.config(text='')
    return rayslist

def getn(r):
    if medtype.get() == 0:
        n0 = float(inp1.get())
        A = float(inp2.get())
        n = n0*np.sqrt(1-A**2 * (r[0]**2+r[1]**2))
    elif medtype.get() == 1:
        n0 = float(inp1.get())
        A = float(inp2.get())
        n = n0*(1-0.5*A**2*(r[0]**2+r[1]**2)+5/24*A**4*(r[0]**2+r[1]**2)**2)
    elif medtype.get() == 2:
        n0 = float(inp1.get())
        A = float(inp2.get())
        n = n0*(1-0.5*A**2*(r[0]**2+r[1]**2)+3/8*A**4*(r[0]**2+r[1]**2)**2)
    
    return n

def getdeln(r,n=getn):
    h = 1e-4
    dx = np.array([h,0,0])
    dy = np.array([0,h,0])
    parx = (n(r+dx)-n(r-dx))/(2*h)
    pary = (n(r+dy)-n(r-dy))/(2*h)
    return np.array([parx,pary,0])


def getT(r,s,n=getn):
    return n(r)*s

def getD(r,n=getn,deln=getdeln):
    return n(r)*deln(r)



# edit media coefficient
def mededitor():
    if medtype.get() == 0:
        lb1.config(text = 'n0')
        lb2.config(text = 'A')
    elif medtype.get() == 1:
        lb1.config(text = 'n0')
        lb2.config(text = 'A')
    elif medtype.get() == 2:
        lb1.config(text = 'n0')
        lb2.config(text = 'A')   

def delTree(tree):
    x = tree.get_children()
    for item in x:
        tree.delete(item)

def rayload():
    filename=tkinter.filedialog.askopenfilename(filetypes=[("逗号分隔值",".csv")])
    if filename != '':
        raydata = read_csv(filename,usecols=["rx","ry","rz","sa","sb","sc"])
        raydata = np.array(raydata)
        ray_num = len(raydata)       
        delTree(tree)
        for j in range(0,ray_num):
            tree.insert("",END,text=str(j),values=(str(raydata[j,0]),str(raydata[j,1]),str(raydata[j,2]),str(raydata[j,3]),str(raydata[j,4]),str(raydata[j,5])))

def run():
    global rayslist
    initial_ray = []
    for item in tree.get_children():    
        item_text = tree.item(item,"values")
        r0 = ray() 
        r0.r = np.array([float(item_text[0]),float(item_text[1]),float(item_text[2])])
        r0.s = np.array([float(item_text[3]),float(item_text[4]),float(item_text[5])])
        initial_ray.append(r0)
    rayslist = trace(initial_ray)

def showtraj():
    # plot trajectory
    global rayslist
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    for ray1 in rayslist:
        x = np.zeros(len(ray1))
        y = np.zeros(len(ray1))
        z = np.zeros(len(ray1))
        for j in range(0,len(ray1)):
            x[j] = ray1[j].r[0]
            y[j] = ray1[j].r[1]
            z[j] = ray1[j].r[2]
        plt.plot(z,x,y)
    plt.title('3D trajectory')
    ax.set_xlabel('z')
    ax.set_ylabel('x')
    ax.set_zlabel('y')
    plt.show()

def showimage():
    # plot spot diagram
    global rayslist
    imgs = inpimg.get()
    imgs = imgs.split()
    for imgz in imgs:
        imgz = float(imgz)
        fig = plt.figure()
        ax = fig.add_subplot(111)
        for ray1 in rayslist:
            x = np.zeros(2)
            y = np.zeros(2)
            z = np.zeros(2)
            x[1] = ray1[0].r[0]
            y[1] = ray1[0].r[1]
            z[1] = ray1[0].r[2]
            indimg = -1
            for j in range(0,len(ray1)):
                x[0] = x[1]
                y[0] = y[1]
                z[0] = z[1]
                x[1] = ray1[j].r[0]
                y[1] = ray1[j].r[1]
                z[1] = ray1[j].r[2]
                if z[1] > imgz:
                    indimg = j-1
                    break
            if indimg >=0:
                plt.scatter(ray1[indimg].r[0],ray1[indimg].r[1])
        
        if inpx.get() != '':
            xspan = float(inpx.get())
        else:
            xspan = 1.0
        if inpy.get() != '':
            yspan = float(inpy.get())
        else:
            yspan = 1.0
        plt.title('z = '+str(imgz))
        ax.set(xlim=(-1*xspan,xspan),ylim=(-1*yspan,yspan))
        ax.set_xlabel('x')
        ax.set_ylabel('y')
    plt.show()

def saverays():
    global rayslist
    file_path = tkinter.filedialog.asksaveasfilename()
    if file_path != '':
        if file_path[-4:] != '.csv':
            file_path = file_path + '.csv'
        reshape_list = []
        rayindex = 0
        for ray in rayslist:
            for r in ray:
                tmp = [rayindex,r.r[0],r.r[1],r.r[2],r.s[0],r.s[1],r.s[2]]
                reshape_list.append(tmp)
            rayindex = rayindex + 1
        columns = ["ray-index","rx","ry","rz","sa","sb","sc"]
        dt = DataFrame(reshape_list,columns=columns)
        dt.to_csv(file_path,index=0)




root = Tk()
root.title('Graded Index Media Ray Tracer')
root.geometry('600x500')

# choose media type
medtype = IntVar()
rd1 = Radiobutton(root,text="n = n0*sqrt(1-A^2 * r^2)",variable=medtype,value=0,command=mededitor)
rd1.place(x=50,y=10,width=200,height=20)
rd2 = Radiobutton(root,text="n = n0*sech(Ar)",variable=medtype,value=1,command=mededitor)
rd2.place(x=50,y=30,width=200,height=20)
rd3 = Radiobutton(root,text="n = n0/sqrt(1+A^2*r^2)",variable=medtype,value=2,command=mededitor)
rd3.place(x=50,y=50,width=200,height=20)
lb1 = Label(root, text='n0')
lb1.place(x=300, y=10, width=20, height=20)
lb2 = Label(root, text='A')
lb2.place(x=450, y=10, width=20, height=20)
inp1 = Entry(root)
inp1.place(x=345, y=10, width=50, height=20)
inp2 = Entry(root)
inp2.place(x=495, y=10, width=50, height=20)


# load rays and display
btn_editray = Button(root, text='Load Rays',command=rayload,relief=RAISED)
btn_editray.place(x=20,y=90)
tree = ttk.Treeview(root)
tree["columns"] = ("0","1","2","3","4","5")
tree.column("#0",width=10,anchor="center")
tree.column("0",width=30,anchor="center")
tree.column("1",width=30,anchor="center")
tree.column("2",width=30,anchor="center")
tree.column("3",width=30,anchor="center")
tree.column("4",width=30,anchor="center")
tree.column("5",width=30,anchor="center")
tree.heading("0",text="rx",anchor="center")
tree.heading("1",text="ry",anchor="center")
tree.heading("2",text="rz",anchor="center")
tree.heading("3",text="sa",anchor="center")
tree.heading("4",text="sb",anchor="center")
tree.heading("5",text="sc",anchor="center")
tree.place(relx=0.05,y=200,relwidth=0.9,relheight = 0.5)

lbi = Label(root, text='iteration')
lbi.place(x=120,y=95,width=50)
inpi = Entry(root)
inpi.place(x=180,y=95,width=60)
inpi.insert(0,'1000')


btn_run = Button(root,text='trace',command=run,relief=RAISED)
btn_run.place(x=300,y=90,width=100)

btn_save = Button(root,text='save',command=saverays,relief=GROOVE)
btn_save.place(x=320,y=130,width=60)

lbtask = Label(root, text='')
lbtask.place(x=425,y=100,width=140)


# show results
btn_traj = Button(root,text='Show Trajectory',command=showtraj,relief=RAISED)
btn_traj.place(x=20,y=130,width=110)
btn_imag = Button(root,text='Show Image',command=showimage,relief=RAISED)
btn_imag.place(x=180,y=130,width=100)

inpimg = Entry(root)
inpimg.place(x=180,y=170,width=150)

lbx = Label(root, text='x span')
lbx.place(x=400,y=135,width=50)
lby = Label(root, text='y span')
lby.place(x=400,y=160,width=50)
inpx = Entry(root)
inpx.place(x=460,y=135,width=60)
inpy = Entry(root)
inpy.place(x=460,y=160,width=60)


root.mainloop()