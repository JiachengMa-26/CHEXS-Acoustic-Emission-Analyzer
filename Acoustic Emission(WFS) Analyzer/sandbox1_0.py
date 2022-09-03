from ast import While
import numpy as np
import h5py as h5
import matplotlib.pyplot as plt
import scipy.io as scio
from tkinter import Tk # from tkinter import Tk for Python 3.x
from tkinter.filedialog import askopenfilename

#############################(Function Area)################################################################################
def checkHLM(tempHltNumber):
    global hltNumber
    if tempHltNumber >= HLT:
        print("HLT!!!")
        print("save x", xItem)
        print("save y", yItem)
        
        #Deep copy of the previous files
        tempX = xItem.copy()
        tempY = yItem.copy()
        
        dataBag.append(tempX)
        dataBag.append(tempY)
        print("Now dataBag: ", dataBag)
        del xItem[:]
        print("clear x", xItem)
        del yItem[:]
        hltNumber -= hltNumber
        print("clear y", yItem)
    
def checkMagnitude(time, bound):
  global hltNumber
  if(bound > 0):
      if(bound > averageMagnitudeUp):
          checkHLM(hltNumber)
          xItem.append(time)
          yItem.append(bound)
      else:
        hltNumber += sampleRate
        print("Now add HLT", hltNumber)
        
  elif(bound < 0):
      if(bound < averageMagnitudeLow):
          checkHLM(hltNumber)
          xItem.append(time)
          yItem.append(bound)
      else:
        hltNumber += sampleRate
        print("Now add HLT", hltNumber)
    
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

################################(graph in 2 seconds)#############################################################################
gX = []
gY = []

for i in range(len(dataSet)):
    currentNum = float(dataSet[i])
    gX.append(i)
    gY.append(currentNum)
    if i== 5 * (2*(10**6)):
        break
plt.plot(gX, gY)
plt.xlabel('x seconds * (5 * (10**(-7)))')
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
dataBag = []

time = streamTot
hltNumber = 0

for i in range(len(dataSet)):
    currentNum = float(dataSet[i])
    #print(currentNum)
    time += sampleRate
    
    checkMagnitude(time, currentNum)
    print(hltNumber)
    if i==10:
    #if i == len(dataSet):
        checkHLM(hltNumber)
        break
    
print(len(dataSet))    
print(xItem)   
print(yItem)
print(dataBag)




           
