import random
import csv
import codecs
from pandas import DataFrame
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import *
from tkinter import filedialog

class Agent:
    
    def __init__(self):

        self.employee = []
        for req in reqs:
            self.employee.append(random.randint(0,req))
        self.fitness = -1

    def __str__(self):

        return "Employee: " + str(self.employee) + "; Fitness: " + str(self.fitness)

shift = None
population = 20
generations = 1000
reqs = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
ans = 10000
ans_agent = []
prebreak = 4
midbreak = 2
postbreak = 4

def printout(inp,maxE,s):
    res= Tk()    
    res.title("WPS solver | Solution")

    df = DataFrame(inp,columns=['hour', '# of employee'])
    figure1 = plt.Figure(figsize=(6,5), dpi=100)
    ax1 = figure1.add_subplot(111)
    bar1 = FigureCanvasTkAgg(figure1, res)
    bar1.get_tk_widget().grid(row=0,sticky=N+S+E+W)
    df.plot(kind='bar', legend=True, ax=ax1)
    ax1.set_title('Staff scheduling in one day')
    resultLabel = Label(res,text="Total number of employee "+str(maxE)+" and total cost is: "+str(maxE*s)+" USD").grid(row=1,sticky=N+S+E+W)

def read_CSV(fileName):
    result = []
    f=codecs.open(fileName,"rb","utf-16")
    csvread=csv.reader(f,delimiter='\t')
    for row in csvread:
        temp = row[0].split(',')
        tmp = []
        for x in temp:
            tmp.append(int(x))
        result.append(tmp)
        # print(result)
    return result

def WPS_solver_ga(esave,salary,preb,midb,postb,p,g):
    global prebreak,midbreak,postbreak,population,generations 
    prebreak = preb
    midbreak = midb
    postbreak = postb

    population = p
    generations = g

    req = acqire_req(read_CSV(esave))
    agents = init_agents(population)

    for generation in range(generations):

        agents = fitness(agents)
        agents = selection(agents)
        agents = crossover(agents)
        agents = mutation(agents)

        if any(agent.fitness >=generations for agent in agents):

            print("Threshold met!")
            break
    hour = []
    for i in range (1,25):
        hour.append('x'+str(i))
    inp = { 'hour' : hour, '# of employee' : ans_agent}
    
    printout(inp,ans,salary)

def acqire_req(inp):
    
    for shift in inp:
        for i in range(shift[0],shift[1]):
            reqs[i] = shift[2]

def init_agents(population):

    return [Agent() for _ in range(population)]

def fitness(agents):

    global ans,ans_agent

    for agent in agents:
        tmp = True
        sum =0
        for i in range(0,23):
            sum += agent.employee[i]
            req_test= 0

            for j in range(i,i+prebreak):
                req_test += agent.employee[j%24]
            
            for j in range(i+prebreak+midbreak,i+prebreak+midbreak+postbreak):
                req_test += agent.employee[j%24]

            if req_test < reqs[i]:
                agent.fitness = -1
                tmp = False
                break
        if tmp == True:
            if sum < ans:
                ans = sum
                ans_agent = agent.employee
                agent.fitness += 2
            else:
                agent.fitness += 1

    return agents

def selection(agents):

    agents = sorted(agents, key=lambda agent: agent.fitness, reverse=True)
    agents = agents[:int(0.2 * len(agents))]
    return agents

def crossover(agents):

    offspring = []

    for _ in  range(int((population - len(agents))/2)):

        parent1 = random.choice(agents)
        parent2 = random.choice(agents)

        child1 = Agent()
        child2 = Agent()

        split = random.randint(0,23)

        child1.employee = []
        child1.employee.extend(parent1.employee[0:split+1]) 
        child1.employee.extend(parent2.employee[split:23])
        
        child2.employee = []
        child2.employee.extend(parent2.employee[0:split+1]) 
        child2.employee.extend(parent1.employee[split:23])

        offspring.append(child1)
        offspring.append(child2)

    agents.extend(offspring)
    return agents

def mutation(agents):
    
    for agent in agents:
        for idx in range(24):
            if random.uniform(0.0,1.0) <=0.1:
                
                tmp = random.randint(0,reqs[idx])
                agent.employee[idx] = tmp

        
    return agents