import numpy as np
from pyDOE import lhs
import matplotlib.pyplot as plt


dimensions = 2
sampleVolume  = 1
solutionsConcentrations = []
numSamples= 60
numSubdivisions = 3 #Subdivisions per dimension

##For testing
for i in range (0,dimensions):
    solutionsConcentrations.append(30)

scalingFactor =  min(solutionsConcentrations)
lengthSubDiv = scalingFactor/numSubdivisions


#LHS for a specific number of dimensions and samples
def lhSampling(numberSamples):
    sample  = lhs(int(dimensions), samples=(numberSamples))
    return sample


#Function for initial scaling
def lhsScaling(samples, scaling):
    scaledSamples  = samples * scaling
    return scaledSamples

#Creates the dimensional Tuples to access nDarray
def creatingTupleLIst():

    tList = []
    permutationList = []
    for i in range(0,numSubdivisions):
        permutationList.append(i)
    
    if dimensions == 1:
        for i in permutationList:
            tList.append((i))
    elif dimensions == 2:
        for i in permutationList:
            for j in permutationList:
                tList.append((i,j))
    elif dimensions == 3:
        for i in permutationList:
            for j in permutationList:
                for d in permutationList:
                    tList.append((i,j,d))
    elif dimensions == 4:
        for a in permutationList:
            for b in permutationList:
                for c in permutationList:
                    for d in permutationList:
                        tList.append((a,b,c,d))       
    elif dimensions == 5:
        for a in permutationList:
            for b in permutationList:
                for c in permutationList:
                    for d in permutationList:
                        for e in permutationList:
                            tList.append((a,b,c,d,e))      

    return tList


#Scaling and Offset for subDivisions
#This function get a range of samples and the corrosponding subdivision from which they are from. With this info 
#the function scales the samples accordingly

def lhsSubDicScalin(samples, dimensionTouple):

    scaledSamples = lhsScaling(samples, lengthSubDiv)
    correctedSamples = []

    #Loops through samples
    for i in range (0,len(samples)):       
        newSample = []

        for d in range (0,dimensions):
            offset = dimensionTouple[d]
            offsetSamples = scaledSamples[i, d] + offset * lengthSubDiv
            newSample.append(offsetSamples)

        correctedSamples.append(newSample)

    return correctedSamples


#N dimensional sorting
def sorting(samples,lengthSubDiv,dimensions):

    for i in range(0,len(samples)):
        samplesPos = []

        for d in range(0,dimensions):
            
            pos = int(samples[i,d] // lengthSubDiv)
            samplesPos.append([pos])
              
        samplesPos = tuple(samplesPos)

        samplesPerSubDiv[samplesPos] = samplesPerSubDiv[samplesPos] + 1

    return samplesPerSubDiv


#Checks if one of the Subsections has no sample in it. If that is the case and it is possible that ther could be a sample process starts from the beginning
def checkForZero(array):
    checkZero=[]

    for i in tupleList:
        number = int(numPerSubDiv[i])
        checkZero.append(number)

    if all(i>0 for i in checkZero):
        return True
    else:
        return False


#Calculates the amount of samples per subsection as input for the LHS | should work in N dimensions
def subsampleCalc(number,dimTuple):
    countList = []
    for d in range (0,dimensions):
        factor = dimTuple[d] +1
        count = number * solutionsConcentrations[d] /((lengthSubDiv/2)*factor*sampleVolume)
        countList.append(count)
        
    return int(min(countList))

#Calculates how much sample was used works in N-Dimensions
def  stockUsedCalculator(samples):
    stockUsed  = []
    for d in range(0,dimensions):
        usedForD = []

        for i in range(0,len(samples)):
            tempTuple = tuple(samples[i])
            temp= (tempTuple[d]/solutionsConcentrations[d])*sampleVolume
            usedForD.append(temp)

        
        stockUsed.append(sum(usedForD))
    
    return  stockUsed
































#Reading the number of samples Per subsection, creating the dimensional touple and getting the mL for subsection 
#most optimization logic
def makingSenseOfDimensions(array):
    finalSampleList = []

    zeroSamples = []
    for i in range(0,dimensions):
        zeroSamples.append(0)



    # Damit item accessen
    for i in tupleList:
        #Number is the amount of mL one has per subsection
        number = int(numPerSubDiv[i])
        sampleCount = subsampleCalc(number, i)

        if sampleCount > 0:
            #Creating Samples for Subdivision
            newSamples = lhSampling(sampleCount)
            #Scaling Samples for Subdivision
            scaledSamplesLH = lhsSubDicScalin(newSamples,i)
            #Getting stock used for each dimension
            stockUsed = stockUsedCalculator(scaledSamplesLH)

            #Das muss ich mal in Konzentration umrechnen, aktuell Volumen stocksolution
            for d in range(0,dimensions):
                tempV = stockUsed[d]
                temp = tempV * solutionsConcentrations[d]

                #Wayyyy to low, viel zu aggressiv
                while temp >= (number * sampleVolume* solutionsConcentrations[d]):
                    if (temp-number * sampleVolume* solutionsConcentrations[d]) > lengthSubDiv * i[d]:
                        scaledSamplesPerDimensionSorting = [f[d] for f in scaledSamplesLH] 
                        drueber = (temp - number * sampleVolume)
                        index = min(range(len(scaledSamplesPerDimensionSorting)),key= lambda i:abs(scaledSamplesPerDimensionSorting[i]-drueber))

                        del scaledSamplesLH[index]
                        stockUsed = stockUsedCalculator(scaledSamplesLH)
                        temp = stockUsed[d]
                    else:
                        break


            finalSampleList = finalSampleList + scaledSamplesLH
   
            

        else:
            finalSampleList.append(zeroSamples)


    return finalSampleList

        

































tupleList = creatingTupleLIst()

noOverflow = False
while noOverflow == False:
    
    ##Das ganze dient dazu ein nDarray zu erstellen, das wenn möglich nur Elemente ungleich Null enthält.
    tester = False
    while tester == False:
        
        if numSamples >= numSubdivisions **dimensions:
            if dimensions == 2:
                samplesPerSubDiv = np.zeros((numSubdivisions,numSubdivisions))

            elif dimensions == 1:
                samplesPerSubDiv = np.zeros(numSubdivisions)

            else:
                samplesPerSubDiv = np.zeros((numSubdivisions,)*dimensions)
            
            #Erstellen der initialen samples
            samples = lhSampling(numSamples)
            scaledSamples = lhsScaling(samples,scalingFactor) 
            numPerSubDiv = sorting(scaledSamples,lengthSubDiv,dimensions)
            tester = checkForZero(numPerSubDiv)


        else:
            if dimensions == 2:
                samplesPerSubDiv = np.zeros((numSubdivisions,numSubdivisions))

            elif dimensions == 1:
                samplesPerSubDiv = np.zeros(numSubdivisions)

            else:
                samplesPerSubDiv = np.zeros((numSubdivisions,)*dimensions)

            #Erstellen der initialen samples
            samples = lhSampling(numSamples)
            scaledSamples = lhsScaling(samples,scalingFactor)   
            numPerSubDiv = sorting(scaledSamples,lengthSubDiv,dimensions)
            tester = True

    ##ENDE WHILE

    subSectionTest  = False
    finalSamples = makingSenseOfDimensions(numPerSubDiv)
    iteration =  0
    while subSectionTest == False:
        print(iteration)

        volumeUsed = stockUsedCalculator(finalSamples)
        print(volumeUsed)
        if all(i < numSamples for i in volumeUsed) & all(i > (0.99*numSamples) for i in volumeUsed):
            print("Success")
            subSectionTest = True
            noOverflow  = True
        else:
            finalSamples = makingSenseOfDimensions(numPerSubDiv)
        
        iteration +=1
        if iteration >  5000:
            break

print(finalSamples)
print(len(finalSamples))











x,y = zip(*finalSamples)

print("Final samples: ", len(finalSamples))

print(stockUsedCalculator(finalSamples))

lhsNormSample = lhs(int(dimensions), samples=(len(finalSamples)))

lhsNormSamples = lhsNormSample * scalingFactor

print("greed Stock used:" ,stockUsedCalculator(lhsNormSamples))

fig, ax = plt.subplots()
ax.scatter(scaledSamples[:, 0], scaledSamples[:, 1])
ax.scatter(x,y)
ax.scatter(lhsNormSamples[:,0],lhsNormSamples[:,1])
ax.set_xlabel('Variable 1')
ax.set_ylabel('Variable 2')
ax.set_title('Latin Hypercube Sampling (Scaled)')

for i in range(1, int(numSubdivisions)):
    ax.axvline(i * scalingFactor / numSubdivisions, color='gray', linestyle='dashed')
    ax.axhline(i * scalingFactor / numSubdivisions, color='gray', linestyle='dashed')

plt.show()
