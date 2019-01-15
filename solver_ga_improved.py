import random
import csv
import codecs
from pandas import DataFrame
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import *
from tkinter import filedialog

class Agent:

    # Agent initiation

    def __init__(self,reqs):
        self.employee = []
        for req in reqs:
            self.employee.append(random.randint(0,req))
        self.fitness = -1.0
    
    # Calculate Sum of Employee
    def getSum(self):
        sum = 0
        for x in self.employee:
            sum += x
        return sum

    # search Gene
    def containsGene(self,target):
        for gene in self.employee:
            if gene == target:
                return True
        return False

    # Calculate clashes of the agents
    def calcClash(self,reqs,pre,mid,post):
        clashes = 0
        for i in range(0,23):
            req_test= 0

            for j in range(i,i+pre):
                req_test += self.employee[j%24]
            
            for j in range(i+pre+mid,i+pre+mid+post):
                req_test += self.employee[j%24]

            if req_test < reqs[i]:
                clashes += 1
                break
        return clashes

class Population:

    # Population initiation
    def __init__(self,size,reqs):
        self.agents = [Agent(reqs) for _ in range(size)]
        self.totalFitness = -1.0

    # Select offset element after sorted
    def bestAgent(self,offset):
        self.agents = sorted(self.agents, key=lambda agent: agent.fitness, reverse=True)
        return self.agents[offset]
 
    # Shuffle population
    def shuffle(self):
        for i in reversed(range(len(self.agents))):
            j = random.randint(0,i)
            tmp = self.agents[i]
            self.agents[i] = self.agents[j]
            self.agents[j] = tmp

class GeneticAlgorithm:

    # Initiate GA
    def __init__(self,mutationRate,crossoverRate,tournament):
        self.mutationRate = mutationRate
        self.crossoverRate = crossoverRate
        self.tournament = int(tournament/3)
    
    # Check terminate condition
    def isTerminationConditionMet(self,population):
        return population.bestAgent(0).fitness == 1.0

    # Calclate fitness of the agents
    def calcFitness(self,agent,reqs,pre,mid,post):
        clashes = agent.calcClash(reqs,pre,mid,post)
        
        fit = 1 / (clashes + 1)
        fitness = 0
        
        if fit == 1.0:
            fitness = 1 / (agent.getSum() * 1.0)

        return fitness

    # Evaluate the population
    def evalPopulation(self,population,reqs,pre,mid,post):

        populationFitness = 0
        
        for i,agent in enumerate(population.agents):
            population.agents[i].fitness = self.calcFitness(agent,reqs,pre,mid,post)
            populationFitness += population.agents[i].fitness

        population.totalFitness = populationFitness / len(population.agents)

        return population

    # Select parent
    def selectParent(self,population):
        tournament = Population(len(population.agents),[0]*24)
        tournament.agents = [] 

        population.shuffle()

        for i in range(self.tournament):
            tournament.agents.append(population.agents[i])

        return tournament.bestAgent(0)

    # Crossover
    def crossover(self,population):
        
        newPopulation = Population(len(population.agents),[0]*24)

        # Loop over population by fitness
        for i in range(len(population.agents)):

            # get parent1
            parent1 = population.bestAgent(i)

            # Apply crossover ?
            if (self.crossoverRate > random.uniform(0.0,1.0)) and (i>=2):
                
                # Get parent2 by perform tournament
                parent2 = self.selectParent(population)
                
                # Create offspring
                offspring = Agent([0]*24)
                offspring.employee = [-1]*24

                # Get subset of parent
                substrPos1 = random.randint(0,len(parent1.employee))
                substrPos2 = random.randint(0,len(parent1.employee))

                # start and end position
                strPos = min(substrPos1,substrPos2)
                endPos = max(substrPos1,substrPos2)

                # loop through parent1
                for j in range(strPos,endPos):
                    offspring.employee[j] = parent1.employee[j]

                # loop through parent2
                for j in range(len(parent2.employee)):
                    parent2Gene = (j+ endPos) % len(parent2.employee)
                    # if offspring doesnt contain parent 2 gene, add it
                    if (offspring.containsGene(parent2.employee[parent2Gene])==False):
                        # find spare position
                        for k in range(len(offspring.employee)):
                            if offspring.employee[k] == -1:
                                offspring.employee[k] = parent2.employee[k]
                                break
                
                # loop through offspring to find empty point
                for k in range(len(offspring.employee)):
                    if offspring.employee[k] == -1:
                        # offspring.employee[k] = random.randint(0,parent2.employee[k])
                        offspring.employee[k] = 0

                newPopulation.agents[i] = offspring
            else:
                newPopulation.agents[i] = parent1
        return newPopulation

    # Mutation
    def mutate(self,population,reqs):
        population.agents = sorted(population.agents, key=lambda agent: agent.fitness, reverse=True)
        for i,agent in enumerate(population.agents):
            if i >= 2:
                for idx in range(24):
                    if random.uniform(0.0,1.0) <= self.mutationRate:
                        tmp = random.randint(0,reqs[idx])
                        # tmp = 0
                        population.agents[i].employee[idx] = tmp
        return population

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

def acqire_req(inp,size):
    reqs = [0]*size
    for shift in inp:
        for i in range(shift[0],shift[1]):
            reqs[i] = shift[2]
    return reqs

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
    
    resultLabel = Label(res,text="Total number of employee "+str(maxE)+" and total cost is: "+str(maxE*500)+" USD").grid(row=1,sticky=N+S+E+W)

def WPS_solver_ga(esave,salary,preb,midb,postb,populationSize,generations,crossover,mutate):

    # Acquire the requirement 
    reqs = acqire_req(read_CSV(esave),24)

    # Initiate Population
    population = Population(populationSize,reqs)

    # Initiate Genetic Algorithm
    mutationRate = float(mutate)
    crossoverRate = float(crossover)
    tournament = populationSize
    ga = GeneticAlgorithm(mutationRate,crossoverRate,tournament)

    # Evaluate Population
    population = ga.evalPopulation(population,reqs,preb,midb,postb)

    # Start evolution loop
    for generation in range(1,generations):
        
        # Check terminate condition
        if ga.isTerminationConditionMet(population):
            break
        
        agent007 = population.bestAgent(0)
        print("Minimum staff : " + str(agent007.getSum()))
        # tmp = []
        # for agent in population.agents:
        #     tmp.append(agent.fitness)
        # print(tmp)

        # Crossover
        population = ga.crossover(population)

        # Mutation
        population = ga.mutate(population,reqs)

        # Evaluation
        population = ga.evalPopulation(population, reqs,preb,midb,postb)

    hour = []
    for i in range (1,25):
        hour.append('x'+str(i))
    inp = { 'hour' : hour, '# of employee' : population.bestAgent(0).employee}
    
    printout(inp,population.bestAgent(0).getSum(),500)
    

        

    