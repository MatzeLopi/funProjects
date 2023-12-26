import numpy as np
from pyDOE import lhs
import matplotlib.pyplot as plt




def calculateLengthSubdiv(dimensions,scalingFactor,numSubdivisions):
    lengthSubDiv = []
    for d in range(0,dimensions):
        lengthSubDiv.append(scalingFactor[d]/numSubdivisions)
    return lengthSubDiv


def createNDarray(numSubdivisions,dimensions):
    if dimensions == 2:
        samplesPerSubDiv = np.zeros((numSubdivisions,numSubdivisions))

    elif dimensions == 1:
        samplesPerSubDiv = np.zeros(numSubdivisions)

    else:
        samplesPerSubDiv = np.zeros((numSubdivisions,)*dimensions)

    return samplesPerSubDiv


#LHS for a specific number of dimensions and samples
def lhSampling(numberSamples,dimensions):
    sample  = lhs(int(dimensions), samples=(numberSamples))
    return sample


#Function for initial scaling
def lhsScaling(samples, scaling,dimensions):
    scaledSamples = []
    for i in range(0,len(samples)):
        tempSample = []
        for d in range(0,dimensions):
            temp = samples[i,d] * scaling[d]
            tempSample.append(temp)
        scaledSamples.append(tempSample)
    return scaledSamples


#Creates the dimensional Tuples to access nDarray
def creatingTupleLIst(numSubdivisions,dimensions):

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

def lhsSubDicScalin(samples, dimensionTouple,dimensions,lengthSubDiv):

    scaledSamples = lhsScaling(samples, lengthSubDiv,dimensions)
    correctedSamples = []

    #Loops through samples
    for i in range (0,len(samples)):       
        newSample = []

        for d in range (0,dimensions):
            offset = dimensionTouple[d]
            offsetSamples = scaledSamples[i][d] + offset * lengthSubDiv[d]
            newSample.append(offsetSamples)

        correctedSamples.append(newSample)

    return correctedSamples


#N dimensional sorting
def sorting(samples,lengthSubDiv,dimensions,ndarray):

    for i in range(0,len(samples)):
        samplesPos = []

        for d in range(0,dimensions):
            number = samples[i][d]
            pos = int(number// lengthSubDiv[d])
            samplesPos.append([pos])
              
        samplesPos = tuple(samplesPos)

        ndarray[samplesPos] = ndarray[samplesPos] + 1

    return ndarray


#Checks if one of the Subsections has no sample in it. If that is the case and it is possible that ther could be a sample process starts from the beginning
def checkForZero(numPerSubDiv,tupleList):
    checkZero=[]
    if numPerSubDiv.size < len(tupleList):
        return False

    for i in tupleList:
        number = int(numPerSubDiv[i])
        checkZero.append(number)

    if all(i>0 for i in checkZero):
        return True
    else:
        return False


#Calculates the amount of samples per subsection as input for the LHS 
def subsampleCalc(number_Samples_per_Dimension,dimTuple,dimensions,solutionsConcentrations,sampleVolume,lengthSubDiv):
    countList = []
    for d in range (0,dimensions):
        factor = dimTuple[d] +1
        count = number_Samples_per_Dimension * solutionsConcentrations[d] /((lengthSubDiv[d]/2)*factor*sampleVolume)
        countList.append(count)
    return int(min(countList))


#Calculates how much sample was used works in N-Dimensions
def stockUsedCalculator(samples,dimensions,solutionsConcentrations,sampleVolume):
    stockUsed  = []
    for d in range(0,dimensions):
        usedForD = []
        for i in range(0,len(samples)):
            tempTuple = tuple(samples[i])
            temp= (tempTuple[d]/solutionsConcentrations[d]*sampleVolume)
            usedForD.append(temp)     
        stockUsed.append(sum(usedForD))
    return  stockUsed




#calculates the volume a sample will have
def actualSampleVolume(samples):
    pass


#Calculates how many initial samples can be made from solution
def calculateNumberSamples(sampleVolume, stockVolume, stockConcentration,maxConcentration,dimensions):
    numberOfSamples_List = []
    for d in range(0,dimensions):
        numberOfSamples_List.append((stockConcentration[d]*stockVolume[d])/(sampleVolume*maxConcentration[d]))
    
    numberOfSamples = min(numberOfSamples_List)
    return int(numberOfSamples)

#Function which creates and scales the samples for one subdivision
def getSamplesPerSubDiv(dimensions,dTuple,samples_per_Subdivision):
    allowedSamplesPerSub = int(samples_per_Subdivision[dTuple])
    return allowedSamplesPerSub

def subDivSampling(dTuple,dimensions,lengthSubDiv,sampleVolume,solutionsConcentrations,samplecount_subdivision):
    zeroSamples = []
    for i in range(0,dimensions):
        zeroSamples.append(0)

    if samplecount_subdivision > 0:
        subdivision_Samples = lhSampling(samplecount_subdivision,dimensions)
        scaled_Samples = lhsSubDicScalin(subdivision_Samples,dTuple,dimensions,lengthSubDiv)
        return scaled_Samples
    else:
        return zeroSamples


#Reading the number of samples Per subsection, creating the dimensional touple and getting the mL for subsection 
#most optimization logic
def subdivision_opt(samples, dimensions,sampleVolume,dTupel,solutionsConcentrations,allowedSamplesPerSub,stockUsed):

    while any(i > allowedSamplesPerSub*sampleVolume for i in stockUsed):    
        for d in range(0,dimensions):
            stock_used_per_D = stockUsed[d]


            scaledSamplesPerDimensionSorting = [f[d] for f in samples] 
            druebermL = (stock_used_per_D - allowedSamplesPerSub * sampleVolume) #drueber in mL -> brauche es aber in Konzentration
            drueber = druebermL * solutionsConcentrations[d]
            index = min(range(len(scaledSamplesPerDimensionSorting)),key= lambda i:abs(scaledSamplesPerDimensionSorting[i]-drueber))

            del samples[index]
            stockUsed = stockUsedCalculator(samples,dimensions,solutionsConcentrations,sampleVolume)
            print("Drüber",dTupel,druebermL)    

    stockUsed = stockUsedCalculator(samples,dimensions,solutionsConcentrations,sampleVolume)

    
    return samples,stockUsed

def checkStockUsage(stockUsed,dimensions):
    stockUsed_sum = []
    for d in range(0,dimensions):
        stockUsed_D = sum(stockUsed[d])
        stockUsed_sum.append(stockUsed_D)

    return stockUsed_sum


def first_opt(sampleVolume,stockVolume,stockConcentration,maxConcentration,scalingFactor,dimensions,number_of_Subdivisions):



    #Creating tuple List 
    tupleList = creatingTupleLIst(number_of_Subdivisions, dimensions)

    #CreateNDArray
    nDarray = createNDarray(number_of_Subdivisions,dimensions)

    #Calculate length Subdivisions
    lengthSubdivision = calculateLengthSubdiv(dimensions,scalingFactor,number_of_Subdivisions)

    #Calculate amount of initial samples
    numberOfSamples = calculateNumberSamples(sampleVolume,stockVolume,stockConcentration,maxConcentration,dimensions)
    
    samplesPerSubdivision  = nDarray

    while checkForZero(samplesPerSubdivision,tupleList) == False:
        #create Initial Samples    
        initial_Samples = lhSampling(numberOfSamples,dimensions)
        #scales initial Samples
        initial_samples_scaled = lhsScaling(initial_Samples,scalingFactor,dimensions)
        #Sorts samples in subdivisions
        samplesPerSubdivision  = sorting(initial_samples_scaled,lengthSubdivision,dimensions,nDarray)


    subdivision_Samples_List = []
    stockUsed_List = []

    for tuple in tupleList:
        allowed_samples_subdiv = getSamplesPerSubDiv(dimensions,tuple,samplesPerSubdivision)
        samplecount_subdivision = subsampleCalc(allowed_samples_subdiv,tuple,dimensions,stockConcentration,sampleVolume,lengthSubdivision)

        subdivision_Samples = subDivSampling(tuple,dimensions,lengthSubdivision,sampleVolume,stockConcentration,samplecount_subdivision)

        subdivision_stockUsed = stockUsedCalculator(subdivision_Samples,dimensions,stockConcentration,sampleVolume)

        opt_Samples, stockUsed_perDivision = subdivision_opt(subdivision_Samples,dimensions,sampleVolume,tuple,stockConcentration,allowed_samples_subdiv,subdivision_stockUsed)

        subdivision_Samples_List = subdivision_Samples_List + opt_Samples

        stockUsed_List.append(stockUsed_perDivision)


    stockUsed = checkStockUsage(stockUsed_List,dimensions)
    
    return subdivision_Samples_List,stockUsed



def second_opt(sampleVolume,stockVolume,stockConcentration,maxConcentration,scalingFactor,dimensions,number_of_Subdivisions):
    samples, volumeUsed = first_opt(sampleVolume,stockVolume,stockConcentration,maxConcentration,scalingFactor,dimensions,number_of_Subdivisions)
    
    progress = 0

    stockLeft= []
    for d in range(0,dimensions):
        stockLeft.append(stockVolume[d] - volumeUsed[d])

    while all(i > 0 for i in stockLeft) & all(i < (0.01*max(stockVolume)) for i in stockLeft):
        samples,volumeUsed = first_opt(sampleVolume,stockVolume,stockConcentration,maxConcentration,scalingFactor,dimensions,number_of_Subdivisions)
        print("Iteration: ", progress)
        progress += 1

    return samples,volumeUsed

        


sampleVolume = 1 #in mL
stockVolume = [30,30]
stockConcentration = [30,30]
maxConcentration = [30,30]
scalingFactor =  [30,30]
dimensions = 2
number_of_Subdivisions = 3 #Per Dimension


finalSamples, stockUsedFinal = second_opt(sampleVolume,stockVolume,stockConcentration,maxConcentration,scalingFactor,dimensions,number_of_Subdivisions)
print(len(finalSamples))



x,y = zip(*finalSamples)
print(stockUsedFinal)
print("StockUsed X", sum(x)/30)
print("StockUsed Y", sum(y)/30)


fig, ax = plt.subplots()
ax.scatter(x,y)
ax.set_xlabel('Variable 1')
ax.set_ylabel('Variable 2')
ax.set_title('Latin Hypercube Sampling (Scaled)')

plt.show()














































'''#Zweite Version Code
lhsNormSample = lhs(int(dimensions), samples=(len(finalSamples)))
lhsNormSamples = lhsNormSample * scalingFactor
usedNormSolution = max(stockUsedCalculator(lhsNormSamples))
lhsNormScaling = numSamples/usedNormSolution
finallhsNormSamples = lhsNormSamples * lhsNormScaling
print("Zweite Variante, max Konzentration, genutztes Volumen:")
print(scalingFactor[0]*lhsNormScaling)
print(stockUsedCalculator(finallhsNormSamples))
print("green Stock used:" ,stockUsedCalculator(lhsNormSamples))




'''