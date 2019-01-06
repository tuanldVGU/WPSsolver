from tkinter import *
from tkinter import filedialog
from gekko import GEKKO
import csv
import codecs
from pandas import DataFrame
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


def read_CSV(fileName):
    result = []
    print(fileName)
    f=codecs.open(fileName,"rb","utf-16")
    csvread=csv.reader(f,delimiter='\t')
    for row in csvread:
        temp = row[0].split(',')
        tmp = []
        for x in temp:
            tmp.append(int(x))
        result.append(tmp)
        print(result)
    return result

def WPS_solver(esave,ssave,prebreak,midbreak,postbreak):
    print(esave,ssave,prebreak,midbreak,postbreak)
    
    m = GEKKO()
    m.options.SOLVER=1  # APOPT is an MINLP solver

    # optional solver settings with APOPT
    m.solver_options = ['minlp_maximum_iterations 500', \
                        # minlp iterations with integer solution
                        'minlp_max_iter_with_int_sol 10', \
                        # treat minlp as nlp
                        'minlp_as_nlp 0', \
                        # nlp sub-problem max iterations
                        'nlp_maximum_iterations 50', \
                        # 1 = depth first, 2 = breadth first
                        'minlp_branch_method 1', \
                        # maximum deviation from whole number
                        'minlp_integer_tol 0.05', \
                        # covergence tolerance
                        'minlp_gap_tol 0.01']

    #initial variables
    x1,x2,x3,x4,x5,x6,x7,x8,x9,x10,x11,x12,x13,x14,x15,x16,x17,x18,x19,x20,x21,x22,x23,x24 = [m.Var(value = 0, integer=True) for i in range(1,25)]

    #initial value
    #print x5.value

    #rest break hour
    breakHour = 2
    #period of work
    period = 4
    #requirement
    re = read_CSV(esave)
    # re = [[0, 3, 20], [3, 6, 16], [6, 9, 25], [9, 12, 40], [12, 16, 60], [16, 20, 30], [20, 24, 25]]
    def checkRequirement(hour):
        for i in re:
            if hour>= i[0] and hour<i[1]:
                return i[2]
    #Equations
    for i in range(0,24): 
        eq = []
        requirement = checkRequirement(i)
        
        for j in range(0,period):
            if i-j<=0:
                eq.append(i-j+24)
            else:
                eq.append(i-j)
            if i-j-breakHour-period <= 0:
                eq.append(i-j-breakHour-period+24)
            else:
                eq.append(i-j-breakHour-period)
        a = 0
        for k in eq:
            a += vars() ["x"+str(k)]
        m.Equation(a >=requirement)
        m.Equation(vars() ["x"+str(i+1)] >=0)
    #Objectives
    m.Obj(x1+x2+x3+x4+x5+x6+x7+x8+x9+x10+x11+x12+x13+x14+x15+x16+x17+x18+x19+x20+x21+x22+x23+x24)

    #set global options
    m.options.IMODE = 3

    #solve simulation
    m.solve(GEKKO(remote = True))

    #results
    # print('')
    # print('Results: ')
    # print(vars().value)
    # printout(vars().value)
    hour = []
    value = []
    sum = 0
    for i in range (1,25):
        hour.append('x'+str(i))
        value.append(vars() ["x"+str(i)].value[0])
        sum += vars() ["x"+str(i)].value[0]
        # print('x'+str(i), str(vars() ["x"+str(i)].value))
    inp = { 'hour' : hour, '# of employee' : value}
    
    printout(inp,sum)
