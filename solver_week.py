# Import required packages
import pandas as pd
import numpy as np
#import gurobipy as gp
from gurobipy import *
import csv
import codecs
from pandas import DataFrame
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def printout(inp,maxE):
    res= Tk()    
    res.title("WPS solver | Solution")
    df = DataFrame(inp,columns=['hour', '# of employee'])
    figure1 = plt.Figure(figsize=(6,5), dpi=100)
    ax1 = figure1.add_subplot(111)
    bar1 = FigureCanvasTkAgg(figure1, res)
    bar1.get_tk_widget().grid(row=0,sticky=N+S+E+W)
    df.plot(kind='bar', legend=True, ax=ax1)
    ax1.set_title('Staff scheduling in one day')
    resultLabel = Label(res,text="Total number of employee"+str(maxE)).grid(row=1,sticky=N+S+E+W)

def printoutWeek(shiftDetail, shiftList, totalCost):
    res= Tk()    
    res.title("WPS solver | Solution")
    tree = ttk.Treeview(res)
    tree["columns"]= shiftList
    i = 0
    for s in shiftList:
        tree.insert("" , i,    text=s, values=shiftDetail[i])
        i += 1
    tree.insert("", i, text='Total cost', values=totalCost )
    tree.pack(fill='both')
    
def read_CSV(fileName):
    result = []
    f=codecs.open(fileName,"rb","utf-16")
    csvread=csv.reader(f,delimiter='\t')
    for row in csvread:
        temp = row[0].split(',')
        tmp = []
        tmp.append(temp[0])
        try:
            tmp.append(int(temp[1]))
        except:
            tmp.append(temp[1])
        # for x in temp:
        #     tmp.append(int(x))
        result.append(tmp)
        # print(result)
    return result
    
def WPS_solver_week(wsave,ssave,asave,msave,otSalary):
    shiftList = []
    shiftReq = []
    tmp = read_CSV(wsave)
    for row in tmp:
        shiftList.append(row[0])
        shiftReq.append(row[1])

    workerList = []
    regCost = []
    tmp = read_CSV(ssave)
    for row in tmp:
        workerList.append(row[0])
        regCost.append(row[1])

    mgmtList = []
    tmp = read_CSV(ssave)
    for row in tmp:
        mgmtList.append(row[0])

    # shiftList = ['Monday1','Monday2','Tuesday1','Tuesday2','Wednesday1','Wednesday2'
    #          ,'Thursday1','Thursday2','Friday1','Friday2','Saturday1','Saturday2','Sunday1','Sunday2']
    # workerList = ['EE01','EE02','EE03','EE04','EE05','EE06','EE07','EE08','EE09','EE10', 'EE11']

    # shiftReq = [3,2,4,4,5,4,5,4,2,4,5,4,3,5]
    shiftRequirements  = { s : shiftReq[i] for i,s in enumerate(shiftList) }

    # Assume everyone is available
    availability = pd.DataFrame(np.ones((len(workerList), len(shiftList))), index=workerList, columns=shiftList)

    # For illustration, assume following people are unavailable: EE02 on Tuesday1, EE05 on Saturday2, EE08 on Thursday1
    tmp = read_CSV(asave)
    for i,row in enumerate(tmp):
        availability.at[row[0],row[1]] = 0
    # availability.at['EE02','Tuesday1'] = 0
    # availability.at['EE05','Saturday2'] = 0
    # availability.at['EE08','Thursday1'] = 0

    # Create availability dictionary to be used in decision variable bounding
    avail = {(w,s) : availability.loc[w,s] for w in workerList for s in shiftList}

    # mgmtList = ['EE01','EE03','EE05','EE07']
    nonmgmtList = [x for x in workerList if x not in mgmtList]

    # Cost of a regular shift
    # regCost = [200,100,225,110,190,105,210,120,95,100, 200]

    # Cost of overtime shift
    OTCost = [otSalary*x for x in regCost]

    regularCost  = { w : regCost[i] for i,w in enumerate(workerList) }
    overtimeCost  = { w : OTCost[i] for i,w in enumerate(workerList) }

    # Range of shifts that every workers is required to stay between
    minShifts = 3
    maxShifts = 7

    # Number of shifts to trigger overtime
    OTTrigger = 5

    model = Model("Workers Scheduling")

    # ub ensures that workers are only staffed when they are available
    x = model.addVars(workerList, shiftList, ub=avail, vtype=GRB.BINARY, name='x')

    regHours = model.addVars(workerList, name='regHrs')
    overtimeHours = model.addVars(workerList, name='overtimeHrs')
    overtimeTrigger = model.addVars(workerList, name = "OT_Trigger", vtype = GRB.BINARY)

    # Ensure proper number of workers are scheduled

    shiftReq = model.addConstrs((
        (x.sum('*',s) == shiftRequirements[s] for s in shiftList)
    ), name='shiftRequirement')

    # Differentiate between regular time and overtime

    ## Decompose total shifts for each worker into regular shifts and OT shifts
    regOT1 = model.addConstrs((regHours[w] + overtimeHours[w] == x.sum(w,'*') for w in workerList))
    ## Ensure that regular shifts are accounted for first for each nurse before counting OT shifts
    regOT2 = model.addConstrs((regHours[w] <= OTTrigger for w in workerList))
    ## Only allow the OT trigger to come on when regular shift count is greater than regular shift limit
    regOT3 = model.addConstrs((regHours[w] / OTTrigger >= overtimeTrigger[w] for w in workerList))

    # Ensure each worker stays within min and max shift bounds

    minShiftsConstr = model.addConstrs(((
        x.sum(w,'*') >= minShifts for w in workerList)
    ), name='minShifts')

    maxShiftsConstr = model.addConstrs(((
        x.sum(w,'*') <= maxShifts for w in workerList)
    ), name='maxShifts')

    # Ensure every shift has at least one manager

    for s in shiftList:
        model.addConstr((quicksum(x.sum(m,s) for m in mgmtList) >= 1), name='mgmtStaffing'+str(s))

        # Minimize total cost, accounting for pay difference between regular time and overtime

    model.ModelSense = GRB.MINIMIZE

    Cost = 0
    Cost += (quicksum(regularCost[w]*regHours[w] + overtimeCost[w]*overtimeHours[w] for w in workerList))

    model.setObjective(Cost)

    model.write("Optimized_Scheduling.lp")
    file = open("Optimized_Scheduling.lp", 'r')
    print(file.read())
    file.close()

    model.optimize()

    print('Total cost = $' + str(model.ObjVal))

    sol = pd.DataFrame(data={'Solution':model.X}, index=model.VarName)
    sol = sol.iloc[0:len(x)]

    dashboard = pd.DataFrame(index = workerList, columns = shiftList)
    for w in workerList:
        for s in shiftList:
            dashboard.at[w,s] = sol.loc['x['+w+','+s+']',][0]
            
    dashboard
    a =[]
    shiftAssignments = {}
    for s in shiftList:
        shiftAssignments.update({s: list(dashboard[dashboard[s] == 1].loc[:,].index)})
        a.append(list(dashboard[dashboard[s] == 1].loc[:,].index))
        
    #print('result')
    #print(shiftAssignments)
    printoutWeek(a, shiftList, str(model.ObjVal))
    return "yes"