from random import randint
from pyamaze import maze,agent
import matplotlib.pyplot as plt

global popSize,mazeSizeInX,mazeSizeInY,a,maxWays
maxWays=100    #to select loop percent in maze module           
a=[]
popSize=100
mazeSizeInX=15 #no of columns in a maze
mazeSizeInY=15 #no of rows in a maze

#*************Functions for Genetic Algorithm****************

def population():
    population=[]
    for i in range(popSize):
        population.append([])      #example    population=[[]]
        for j in range(mazeSizeInX):
            a=randint(1,mazeSizeInY)
            population[i].append(a) 
        population[i][0]=1
        population[i][-1]=mazeSizeInY
    return population

def findingCoordinates(chrom):
    coord,b=[],0                        
    var2=1           #var2 will be use in every condition
    for j in range(len(chrom)-1):

        #first condition 
        if chrom[j]<chrom[j+1]: 
            b=chrom[j]       
            while (b!=chrom[j+1]+1):
                coord.append((b,var2))
                b+=1   
            var2+=1 
        #second condition
        if chrom[j]>chrom[j+1]:
            b=chrom[j]              
            while (b!=chrom[j+1]-1):
                coord.append((b,var2))
                b-=1
            var2+=1 
        # Third condition
        if chrom[j]==chrom[j+1]:
            coord.append((chrom[j],var2))
            var2+=1
    coord.append((mazeSizeInY,mazeSizeInX)) 
    return coord

def FindingDirections(chrom): 
    directions={}
    for i in range(len(chrom)-1):
        if chrom[i][0]>chrom[i+1][0]:
            directions[chrom[i]]='N'
        elif chrom[i][0]<chrom[i+1][0]:
            directions[chrom[i]]='S'
        else:
            if chrom[i][1]>chrom[i+1][1]:
                directions[chrom[i]]='W'
            elif chrom[i][1]<chrom[i+1][1]:
                directions[chrom[i]]='E'
    return directions

def infeasibleSteps(chrom,maze_map):
    b=findingCoordinates(chrom)
    x=FindingDirections(b)
    infesibleSteps = 0
    for coordinate, direction in x.items():
        if maze_map[coordinate][direction] == 0:
            infesibleSteps += 1
    return infesibleSteps

def stepcount(chrom):
    stepcounter,b=0,0                        
    var2=1           #var2 will be use in every condition
    for j in range(len(chrom)-1):

        #first condition 
        if chrom[j]<chrom[j+1]: 
            b=chrom[j]        
            while (b!=chrom[j+1]+1):
                stepcounter+=1
                b+=1 
            var2+=1 
         #second condition
        if chrom[j]>chrom[j+1]:
            b=chrom[j]              
            while (b!=chrom[j+1]-1):
                stepcounter+=1
                b-=1
            var2+=1 
        # Third condition
        if chrom[j]==chrom[j+1]:
            stepcounter+=1
            var2+=1
    return stepcounter+1

def sortTheChrom(population,mazMap):
    sorted_list = sorted(population, key = lambda i: infeasibleSteps(i,mazMap))
    return sorted_list

def crossOverFunction(sortedList):
    cutpoint=int(mazeSizeInX/2)
    sort=int(len(sortedList)/2)
    for i in range(sort):
        for j in range(cutpoint):
            sortedList[i+sort][j]=sortedList[i][j]
        for j in range(cutpoint,mazeSizeInX):
            sortedList[i+sort][j]=sortedList[i][j]
    return sortedList

def mutationFunction(fullPop):
    for i in range(len(fullPop)-1):
        if infeasibleSteps(fullPop[i],solution)>6:
            i+=1
        elif infeasibleSteps(fullPop[i],solution)>4:
            i+=2
        else:
            i+=3
        if i>len(fullPop)-1:
            return fullPop
        a=randint(1,mazeSizeInX-2)
        fullPop[i][a]=randint(1,mazeSizeInX)
    return fullPop

#****************Main of program***********************

m=maze(mazeSizeInY,mazeSizeInX)
m.CreateMaze(mazeSizeInY,mazeSizeInX,loopPercent=maxWays)
solution=m.maze_map 

length,itrations,solvepath=[],[],0
for i in range(100000):
    a=population()
    for j in range(1000000):
        sortedPop=sortTheChrom(a,solution)
        zeroInfStep=infeasibleSteps(sortedPop[0],solution)
        print(zeroInfStep)
        if zeroInfStep==0:
            solvepath+=1
            length.append(stepcount(sortedPop[0]))
            itrations.append(j+1)            
            if solvepath==1:
                print(sortedPop[0])
                b=agent(m,footprints=True,filled=True,shape='arrow')
                b.position=(1,1)
                path=findingCoordinates(sortedPop[0])
                m.tracePath({b:path},delay=300)
                m.run()
                #itrations.sort()
                #print(itrations)
                #print(length)
                '''plt.plot(itrations,length)
                plt.xlabel('No Of Itrations')
                plt.ylabel('Lengths of Possible Paths')
                plt.title('Graph B/W length and Itrations')
                plt.show()'''
                exit()
            break
        b=crossOverFunction(sortedPop)
        a=mutationFunction(b)