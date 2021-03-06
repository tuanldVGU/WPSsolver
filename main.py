from tkinter import *
from tkinter import filedialog
from solver import WPS_solver
from solver_ga_improved import WPS_solver_ga
from solver_week import WPS_solver_week

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
    if text=="w":
        global weekFile
        weekFile.set(fileName)
    else:
        global salaryFile
        salaryFile.set(fileName)
    return

root= Tk()
# root.geometry("650x350")
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
salaryLabel = Label(root,text="Enter the salary (USD):").grid(row=1,sticky="W")
salaryEntry = Entry(root, textvariable= salaryFile).grid(row=1,column=1)
sbtn = Button(root, text="Choose file", command= lambda: import_CSV("s")).grid(row=1, column=2)

# pre-break time
preVal = 4
preLabel = Label(root, text="Pre-break time").grid(row=0,column=3)
preSlider = Scale(root, from_=2, to=6, command=syncPre)
preSlider.set(4)
preSlider.grid(row=1, column=3)

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

# Solve the problem
solBtn = Button(root, text="Solve", command= lambda: WPS_solver(peopleFile.get(),salaryFile.get(),preVal,btVal,postVal)).grid(row=4, column=0, columnspan=6,sticky=N+S+E+W)

# GA population
populationGA = StringVar()
populationGA.set("20")
pGALabel = Label(root,text="GA population:").grid(row=5,sticky="W")
pGAEntry = Entry(root, textvariable= populationGA).grid(row=5,column=1)

# GA generation
generationGA = StringVar()
generationGA.set("1000")
gGALabel = Label(root,text="GA generations:").grid(row=6,sticky="W")
gGAEntry = Entry(root, textvariable= generationGA).grid(row=6,column=1)

# GA crossover rate
crossoverGA = StringVar()
crossoverGA.set("0.9")
cGALabel = Label(root,text="GA crossover rate:").grid(row=7,sticky="W")
cGAEntry = Entry(root, textvariable= crossoverGA).grid(row=7,column=1)

# GA mutation rate
mutationGA = StringVar()
mutationGA.set("0.1")
mGALabel = Label(root,text="GA mutation rate:").grid(row=8,sticky="W")
mGAEntry = Entry(root, textvariable= mutationGA).grid(row=8,column=1)

# Solve the problem GA
solBtn1 = Button(root, text="Solve GA", command= lambda: WPS_solver_ga(peopleFile.get(),salaryFile.get(),preVal,btVal,postVal,int(populationGA.get()),int(generationGA.get()),crossoverGA.get(),mutationGA.get())).grid(row=9, column=0, columnspan=6,sticky=N+S+E+W)

# Week requirement file insert
weekFile = StringVar()
weekFile.set("week_req.csv")
weekLabel = Label(root,text="Enter your week requirement:").grid(row=10,sticky="W")
weekEntry = Entry(root, textvariable= weekFile).grid(row=10,column=1)
wbtn = Button(root, text="Choose file", command= lambda: import_CSV("w")).grid(row=10, column=2)

# Over-time salary
otFile = StringVar()
otFile.set("2")
otLabel = Label(root,text="Enter your overtime salary/ normal salary:").grid(row=11,sticky="W")
otEntry = Entry(root, textvariable= otFile).grid(row=11,column=1)

# Availability
avFile = StringVar()
avFile.set("available.csv")
avLabel = Label(root,text="Employee missing date:").grid(row=12,sticky="W")
avEntry = Entry(root, textvariable= avFile).grid(row=12,column=1)

# Manager
mFile = StringVar()
mFile.set("manager.csv")
mLabel = Label(root,text="Managers :").grid(row=13,sticky="W")
mEntry = Entry(root, textvariable= mFile).grid(row=13,column=1)

# Solve the problem week
solBtn2 = Button(root, text="Solve Week Problem", command= lambda: WPS_solver_week(weekFile.get(),salaryFile.get(),avFile.get(),mFile.get(),int(otFile.get()))).grid(row=14, column=0, columnspan=6,sticky=N+S+E+W)



root.mainloop()