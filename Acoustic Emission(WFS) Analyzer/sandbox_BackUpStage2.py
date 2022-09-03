import copy
from ast import While
import numpy as np
import h5py as h5
import matplotlib.pyplot as plt
import scipy.io as scio
from tkinter import Tk # from tkinter import Tk for Python 3.x
from tkinter.filedialog import askopenfilename

#############################(Function Area)################################################################################
def supplementaryCoordinates():
    global supplementaryNumber
    global position
    global time
    global temBag
    
    supplementaryNumberInt = int(supplementaryNumber)
    supplementaryPosition = position - supplementaryNumberInt
    tempTime = float(supplementaryPosition * unit)
    if supplementaryPosition >= 0 and tempTime >= 0:
        for j in range(supplementaryNumberInt):
            temBag[tempTime] = dataSet[supplementaryPosition]
            supplementaryPosition += 1
            tempTime += unit
        
    
def saveToBag(num, hltNow):
    global found
    global hltNumber
    global unit
    global pulseNumber
    global temBag
    
    if num >= averageMagnitudeUp or num <= averageMagnitudeLow:
        if len(temBag) == 0:
            supplementaryCoordinates()
        temBag[time] = num
        found = True
        hltNumber -=  hltNumber
    elif hltNow < HLT and found == True :
        temBag[time] = num
        hltNumber += unit
    elif hltNow >= HLT:
        tempb = copy.deepcopy(temBag)
        dataBag[pulseNumber] = tempb
        pulseNumber = pulseNumber + 1
        temBag.clear()
        hltNumber -=  hltNumber
        found = False
###############################(File openner)##############################################################################

Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
filename = askopenfilename() # show an "Open" dialog box and return the path to the selected file

################################(Analyze the file)#############################################################################

data=h5.File(filename,'r')
x = list(data.keys())
print("All element: \n",x,"\n")

################################(Get & Check User input)#############################################################################

dataSet = np.array(data['stream_dump'])[0]
sampleRate = float(np.array(data['sample_rate'])[0][0])
streamTot = float(np.array(data['stream_tot'])[0][0])
print("Stream_Dump", np.array(data['stream_dump'])[0])
print("Sample_Rate", np.array(data['sample_rate'])[0])
print("Stream_Tot", np.array(data['stream_tot'])[0])

################################(graph in 5 seconds)#############################################################################

gX = []
gY = []

for i in range(len(dataSet)):
    currentNum = float(dataSet[i])
    gX.append(i/2)
    gY.append(currentNum)
    if i== 5 * (sampleRate * (10**3)):
        #range(len(dataSet))
        break
plt.plot(gX, gY)
plt.xlabel('x Time (Second)')
# naming the y axis
plt.ylabel('y Magnitude')
plt.show()

################################(get user input)#############################################################################
 
numberChecker = False

while numberChecker == False:
    
    inAverageMagnitudeUp = input("Enter Average Magnitude(Upper bound >0): ")
    averageMagnitudeUp = int(inAverageMagnitudeUp)
    print("Your upper bound is: ",averageMagnitudeUp)
    
    inAverageMagnitudeLow = input("Enter Average Magnitude(Lower bound <0): ")
    averageMagnitudeLow = int(inAverageMagnitudeLow)
    print("Your lower bound is: ",averageMagnitudeLow)
    
    inHLT = input("Enter HLT (Hit lockout time): ")
    HLT = int(inHLT)
    print("Your HLT (Hit lockout time) is: ",HLT)
    
    if averageMagnitudeUp > 0 and averageMagnitudeLow < 0:
        numberChecker = True
    else:
        print("Error: Please reenter your input")
print("Everything is ready, the program is operating")   

#############################(Handling data)################################################################################

xItem = []
yItem = []
dataBag = {}
position = 0
pulseNumber = 1
temBag = {}
found = False
time = 0
#= streamTot
hltNumber = 0
#s to Microsecond
showDialog = True

unit = ((1 / (sampleRate * (10**3))) * 1000000) 
supplementaryNumber = float(HLT / unit)
print("supNUM = ", supplementaryNumber)

for i in range(len(dataSet)):
    currentNum = float(dataSet[i])
    position = i
    #print(currentNum)
    time += unit
    saveToBag(currentNum, hltNumber)
    #print(hltNumber)
    
print((dataBag))
print(len(dataBag)," pulses found.")

#############################(User selection)################################################################################           

def case1():
    showCase1 = True
    global dataBag
    while showCase1 == True:
        tempBagSize = len(dataBag)
        pulsesNumberTeller = ("Select a pause / from 1 to " + str(tempBagSize))
        selectedPulse = int(input(pulsesNumberTeller))

        xAxis = []
        yAxis = []
        selectedDict = dataBag[selectedPulse]
        for xKey in selectedDict:
            xAxis.append(xKey)
            yAxis.append(selectedDict[xKey])
        
        plt.plot(xAxis, yAxis)
        plt.xlabel('x Time (Microsecond)')
        # naming the y axis
        plt.ylabel('y Magnitude')
        plt.show()
    
    
        showOrNot = input("Continue to query? y(yes), n(no)").lower()
        if showOrNot == "n":
            showCase1 = False
        elif showOrNot == "y":
            showCase1 = True
        else:
            print("Invalid input. Please enter again...")
    backToMain()

def case2():
    gX = []
    gY = []
    xAxis = []
    yAxis = []
    
    for i in range(len(dataSet)):
        currentNum = float(dataSet[i])
        gX.append(i * unit)
        gY.append(currentNum)
        
    for j in range(len(dataBag)):   
        selectedDict = dataBag[j+1]
        for xKey in selectedDict:
            xAxis.append(xKey)
            yAxis.append(selectedDict[xKey])
            
    plt.plot(gX, gY,"b.")
    plt.plot(xAxis, yAxis,"g.")
    plt.xlabel('x Time (Second)')
    # naming the y axis
    plt.ylabel('y Magnitude')
    plt.show()
    backToMain()

def backToMain():
    global showDialog
    
    showOrNot = input("Back to the main menu? y(yes), n(no)").lower()
    if showOrNot == "n":
            showDialog = False
    elif showOrNot == "y":
            showDialog = True
    else:
        print("Invalid input. Please enter again...")
        backToMain()

while showDialog == True: 
    firstSelection = int(input("Please select the operation to be performed: \n 1: Query in all pulses intercepted. \n 2: Check the distribution of pulses in the complete image")) 
    if firstSelection == 1:
        case1()
    elif firstSelection == 2:
        case2()
    elif firstSelection == 3:
        print("picked 3")
    else:
        print("invalid")




        