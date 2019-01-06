from tkinter import *
from tkinter import filedialog
from solver import WPS_solver

def syncPre(val):
    tmp = 8-int(val)
    postSlider.set(tmp)
    return

def syncPost(val):
    tmp = 8-int(val)
    preSlider.set(tmp)
    return

def import_CSV(text):
    fileName = filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("csv files","*.csv"),("all files","*.*")))
    print(fileName)
    if text=="p":
        global peopleFile
        peopleFile.set(fileName)
    else:
        global salaryFile
        salaryFile.set(fileName)
    return

root= Tk()
root.geometry("650x350")
root.title("WPS solver")

# topFrame = Frame(root)
# topFrame.pack(fill=X)
# botFrame = Frame(root)
# botFrame.pack(fill=X, side=BOTTOM)

# People File insert
peopleFile = StringVar()
peopleFile.set("emp_req.csv")
peopleLabel = Label(root,text="Enter your employee requirement CSV:").grid(row=0,sticky="W")
peopleEntry = Entry(root, textvariable= peopleFile).grid(row=0,column=1)
pbtn = Button(root, text="Choose file", command= lambda: import_CSV("p")).grid(row=0, column=2)

# Salary File insert
salaryFile = StringVar()
salaryFile.set("salary_req.csv")
salaryLabel = Label(root,text="Enter your salary requirement CSV:").grid(row=1,sticky="W")
salaryEntry = Entry(root, textvariable= salaryFile).grid(row=1,column=1)
sbtn = Button(root, text="Choose file", command= lambda: import_CSV("s")).grid(row=1, column=2)

# pre-break time
prtVal = 4
prtLabel = Label(root, text="Pre-break time").grid(row=0,column=3)
prtSlider = Scale(root, from_=2, to=6, command=syncPre)
prtSlider.set(4)
prtSlider.grid(row=1, column=3)

# break time
btVal = 2
btLabel = Label(root, text="Break time").grid(row=0,column=4)
btSlider = Scale(root, from_=1, to=2)
btSlider.set(2)
btSlider.grid(row=1,column=4)

# post-break time
postVal = 4
postLabel = Label(root, text="Post-break time").grid(row=0,column=5)
postSlider = Scale(root, from_=2, to=6, command=syncPost)
postSlider.set(4)
postSlider.grid(row=1, column=5)

# Maximum workday in a week
wdVal = StringVar()
wdLabel = Label(root,text="Maximum workday in a week:").grid(row=2,sticky="W")
wdEntry = Entry(root, textvariable= wdVal)
wdVal.set("5")
wdEntry.grid(row=2,column=1)

# Solve the problem
solBtn = Button(root, text="Solve", command= lambda: WPS_solver(peopleFile.get(),salaryFile.get(),prtVal,btVal,postVal)).grid(row=4, column=0, columnspan=6,sticky=N+S+E+W)

root.mainloop()