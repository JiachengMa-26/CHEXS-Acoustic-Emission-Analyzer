import copy
from ast import While
import itertools
from matplotlib.axis import XAxis
import numpy as np
import h5py as h5
from scipy.signal import find_peaks
import matplotlib.pyplot as plt
import scipy.io as scio
from tkinter import Tk # from tkinter import Tk for Python 3.x
from tkinter.filedialog import askopenfilename
import soundfile as sf
import scipy.io.wavfile
import scipy.signal
import os
#############################(Function Area)################################################################################

def supplementaryCoordinates():
    global supplementaryNumber #HLT / Unit
    global position #Peak, the first highest point
    global time
    global temBag #Bag for all x and y points for the array
    
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
    
    # Determine if the pulse is valid, if so: saveToBag
    if num >= averageMagnitudeUp or num <= averageMagnitudeLow:
        # Here we will find the first pulse, and then we will take his previous points and fill them according to HLT
        if len(temBag) == 0:
            supplementaryCoordinates() #Complementary spots
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
print("All element: \n",x,"\n") #Tell element

################################(Get & Check User input)#############################################################################

#select stream_dump
#0 = stream_dump
#1 = stream_dump_1
#2 = stream_dump_2
askStream_dump = int(input("Select Stream Dump(0 for stream_dump, 1, and 2):"))

stream_dump = 'stream_dump'
stream_dump_1 = 'stream_dump_1'
stream_dump_2 = 'stream_dump_2'

if askStream_dump == 0 and x.__contains__(stream_dump) == True:
    dataSet = np.array(data[stream_dump])[0]
elif askStream_dump == 1 and x.__contains__(stream_dump_1) == True:
    dataSet = np.array(data[stream_dump_1])[0]
elif askStream_dump == 2 and x.__contains__(stream_dump_2) == True:
    dataSet = np.array(data[stream_dump_2])[0]    

sampleRate = float(np.array(data['sample_rate'])[0][0])
streamTot = float(np.array(data['stream_tot'])[0][0])
print("Stream_Dump: ", dataSet)
print("Sample_Rate: ", np.array(data['sample_rate'])[0])
print("Stream_Tot: ", np.array(data['stream_tot'])[0])

################################(graph in 5 seconds)#############################################################################

gX = []
gY = []

timeLength = ((1 / (sampleRate * (10**3))) * len(dataSet)) #Calculate length of the entire data

print("Duration: ", timeLength, "s. Please select the time period to be drawn...")

askNumberRangeStart = (int(input("Please enter the start time: ")) * 1000000) * 2 #This is equal to the start time in the X coordinate
askNumberRangeEnd = (int(input("Please enter the end time: ")) * 1000000) * 2 #This is equal to the end time in the X coordinate

# loop through the list between askNumberRangeStart and askNumberRangeEnd
for i in range((askNumberRangeStart) , len(dataSet)):
    currentNum = float(dataSet[i])
    gX.append(i/2)
    gY.append(currentNum)
    if i >= (askNumberRangeEnd):
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

xItem = [] # x values are in this list

yItem = [] # y values are in this list

dataBag = {} # All recorded pulses will be collected in this dictionary

position = 0 # Record the current position

pulseNumber = 1 

temBag = {} # Dictionary before the end of each HLT

found = False # Check if the HLT time is exceeded

time = 0 # x-axis record, also time record

hltNumber = 0 # HLT time log, which is the total amount of time that has been logged since the HLT was triggered

showDialog = True #The presentation of the dialog box is determined, and if the user chooses to exit, False will be displayed.

unit = ((1 / (sampleRate * (10**3))) * 1000000) #Calculate units from the original .mat file, basically converting from seconds to microseconds

supplementaryNumber = float(HLT / unit) #Based on the HLT of the user input for the complement(Of plot in the begaining), because we want the peak to be in the middle of the image

print("supNUM = ", supplementaryNumber) #Tells you how many points will be added before the peak

for i in range(len(dataSet)): #loop through the dataset to retrieve any points that exceed the user input value
    currentNum = float(dataSet[i])
    position = i
    #print(currentNum)
    time += unit
    saveToBag(currentNum, hltNumber)
    #print(hltNumber)
    
print((dataBag))
print(len(dataBag)," pulses found.")

#############################(User selection)################################################################################           

#############################(CASE 1)################################################################################           

def pulseAnalyze(xAxis, yAxis): 
    
    global averageMagnitudeUp #User entered upperbound
    global averageMagnitudeLow #User entered lowerbound
    
    x = np.array(xAxis)
    y = np.array(yAxis)
    
    ##############################Signal Filtering###############################################
    scipy.io.wavfile.write('ecg.wav', 4800, y)
    # read ECG data from the WAV file
    sampleRate, data = scipy.io.wavfile.read('ecg.wav')
    times = np.arange(len(data))/sampleRate

    # apply a 3-pole lowpass filter at 0.1x Nyquist frequency
    b, a = scipy.signal.butter(3, 0.1)
    filtered = scipy.signal.filtfilt(b, a, data)
    print()
    plt.figure(figsize=(10, 4))

    plt.subplot(121)
    plt.plot(times, data)
    plt.title("ECG Signal with Noise")
    plt.margins(0, .05)

    plt.subplot(122)
    plt.plot(times, filtered)
    plt.title("Filtered ECG Signal")
    plt.margins(0, .05)

    plt.tight_layout()
    plt.show()
    
    plt.plot(data, '.-', alpha=.5, label="data")

    for cutoff in [.03, .05, .1]:
        b, a = scipy.signal.butter(3, cutoff)
        filtered = scipy.signal.filtfilt(b, a, data)
        label = f"{int(cutoff*100):d}%"
        plt.plot(filtered, label=label)

    plt.legend()
    plt.axis([150, 250, None, None])
    plt.title("Effect of Different Cutoff Values")
    plt.show()
    
    segment = data[150:250]

    filtered = scipy.signal.filtfilt(b, a, segment)
    filteredGust = scipy.signal.filtfilt(b, a, segment, method="gust")

    plt.plot(segment, '.-', alpha=.5, label="data")
    plt.plot(filtered, 'k--', label="padded")
    plt.plot(filteredGust, 'k', label="Gustafsson")
    plt.legend()
    plt.title("Padded Data vs. Gustafsson’s Method")
    plt.show()
    
    os.remove('ecg.wav')
    #############################################################################
    
    #Find peaks
    peaks = find_peaks(y, height = 1, threshold = 1, distance = 1)
    height = peaks[1]['peak_heights'] #list of the heights of the peaks
    peak_pos = x[peaks[0]] #list of the peaks positions
    #Finding the minima
    y2 = y*-1
    minima = find_peaks(y2)
    min_pos = x[minima[0]] #list of the minima positions
    min_height = y2[minima[0]] #list of the mirrored minima heights
    
    #################################Find peaks 2 (base on the filtered data)#################################################################
    
    #Find peaks 2 (base on the filtered data)
    #Before you do that!!!
    #The reason for this is that after filtering you will be able to use peak_pos_ListY2 
    # (i.e. Y after noise removal) to determine Fall Time.
    
    #peaks = find_peaks(filtered, height = 1, threshold = 1, distance = 1)
    #height = peaks[1]['peak_heights'] #list of the heights of the peaks
    #peak_pos = x[peaks[0]] #list of the peaks positions
    #Finding the minima
    #y2 = y*-1
    #minima = find_peaks(y2)
    #min_pos = x[minima[0]] #list of the minima positions
    #min_height = y2[minima[0]] #list of the mirrored minima heights
    
    #peak_pos_ListXPos = list(peak_pos)
    #peak_pos_ListXNeg = list(min_pos)
    #peak_pos_ListX2 = []
    
    #peak_pos_ListYPos = list(height)
    #peak_pos_ListYNeg = list(min_height*-1)
    #peak_pos_ListY2 = []
    
    #for mx in range(len(peak_pos_ListXPos)):
    #    if peak_pos_ListXPos[0] < peak_pos_ListXNeg[0]:
    #        peak_pos_ListX2.append(peak_pos_ListXPos[mx])
    #        peak_pos_ListX2.append(peak_pos_ListXNeg[mx])
    #        peak_pos_ListY2.append(peak_pos_ListYPos[mx])
    #        peak_pos_ListY2.append(peak_pos_ListYNeg[mx])
    #    else:
    #        peak_pos_ListX2.append(peak_pos_ListXNeg[mx])
    #        peak_pos_ListX2.append(peak_pos_ListXPos[mx])
    #        peak_pos_ListY2.append(peak_pos_ListYNeg[mx])
    #        peak_pos_ListY2.append(peak_pos_ListYPos[mx])
            
    ####################################################################################################
    #Plotting
    fig = plt.figure()
    ax = fig.subplots()
    ax.plot(x,y)
    ax.scatter(peak_pos, height, color = 'r', s = 15, marker = 'D', label = 'Maxima')
    ax.scatter(min_pos, min_height*-1, color = 'gold', s = 15, marker = 'X', label = 'Minima')
    ax.legend()
    ax.grid()
    plt.show()
    
    peak_pos_ListXPos = list(peak_pos)
    peak_pos_ListXNeg = list(min_pos)
    peak_pos_ListX = []

    peak_pos_ListYPos = list(height)
    peak_pos_ListYNeg = list(min_height*-1)
    peak_pos_ListY = []

    #Save all the peak in order
    for mx in range(len(peak_pos_ListXPos)):
        if peak_pos_ListXPos[0] < peak_pos_ListXNeg[0]:
            peak_pos_ListX.append(peak_pos_ListXPos[mx])
            peak_pos_ListX.append(peak_pos_ListXNeg[mx])
            peak_pos_ListY.append(peak_pos_ListYPos[mx])
            peak_pos_ListY.append(peak_pos_ListYNeg[mx])
        else:
            peak_pos_ListX.append(peak_pos_ListXNeg[mx])
            peak_pos_ListX.append(peak_pos_ListXPos[mx])
            peak_pos_ListY.append(peak_pos_ListYNeg[mx])
            peak_pos_ListY.append(peak_pos_ListYPos[mx])
        
    #print(peak_pos_ListX) 

    fallCount = 0 #Because we determine Fall time by counting how many times the peak is consistently below the pivotPoint, this is the count (for example, if it is less than the pivotPoint 5 times in a row, it will stop at the fifth time)
    pivotPoint = 0.0 #peak point
    energyReleaseRise = 0 
    energyReleaseFall = 0
    energyReleaseTotal = 0
    beginPointLeft = 0
    beginPointRight = 0
    riseTime = 0
    fallTime = 0
    peakX = 0
    peakAmplitude = max((yAxis), key=abs)
    
    peakX += xAxis[yAxis.index(peakAmplitude)]
    
    #Determine Pivot Point
    if peakAmplitude >= 0:
        if peakAmplitude * 0.05 > averageMagnitudeUp:
            pivotPoint += peakAmplitude
        else:
            pivotPoint += averageMagnitudeUp
               
    elif peakAmplitude <= 0:
        if peakAmplitude * 0.05 < averageMagnitudeLow:
            pivotPoint += peakAmplitude
        else:
            pivotPoint += averageMagnitudeLow
            
    for i in range(0, yAxis.index(peakAmplitude)):
        if(yAxis[i] > pivotPoint):
            beginPointLeft += yAxis[i-1]
            break
    
    tempmax = max(peak_pos_ListY, key=abs)

    print(tempmax)
    start = peak_pos_ListY.index(tempmax)
    end = len(peak_pos_ListY)
    print(start, end)
    print(peak_pos_ListX[start])
    
    #If the point is below the pivot point it will enter this judgment
    for j in range(start, end):

        if(peak_pos_ListY[j] > 0):
            if(peak_pos_ListY[j] < pivotPoint):
                fallCount += 1
            if(fallCount == 10):
                #print("got number: ", peak_pos_ListY[j])
                #print(j)
                indexX = peak_pos_ListX[j]
                #print("indexX", indexX)
                beginPointRight += indexX
                break
            
        elif(peak_pos_ListY[j] < 0):
            if(peak_pos_ListY[j] > pivotPoint):
                fallCount += 1
            if(fallCount == 10):
                #print("got number: ", peak_pos_ListY[j])
                #print(j)
                indexX = peak_pos_ListX[j]
                #print("indexX", indexX)
                beginPointRight += indexX
                break   
            
    riseTime += xAxis[yAxis.index(beginPointLeft)]
    fallTime += beginPointRight
    #print(fallTime)
    for itemR in range(xAxis.index(riseTime), xAxis.index(peakX)):
        energyReleaseRise += ((yAxis[xAxis.index(xAxis[itemR])] ** 2) * unit) 
        
    for itemF in range(xAxis.index(peakX), xAxis.index(fallTime)):
         energyReleaseFall += ((yAxis[xAxis.index(xAxis[itemF])] ** 2) * unit) 
  
    for itemT in range(len(yAxis)):
         energyReleaseTotal += ((yAxis[itemT] ** 2) * unit)
             
    print("About this pulse: ")
    print("Peak Amplitude: ", peakAmplitude)
    print("Peak X: ", peakX)
    print("PivotPoint: ", pivotPoint)
    print("RiseTime: ", riseTime)
    print("FallTime: ", fallTime)
    print("EnergyRelease(Rise): ", energyReleaseRise)
    print("EnergyRelease(Fall): ", energyReleaseFall)
    print("EnergyRelease(Total): ", energyReleaseTotal)
    
       
def case1():
    
    # Select pulse for depiction.
    
    showCase1 = True
    global dataBag
    
    while showCase1 == True:
        tempBagSize = len(dataBag)
        pulsesNumberTeller = ("Select a pause / from 1 to " + str(tempBagSize)+ ": ")
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

        analyzeOrNot = input("Analyze this pulse? y(yes), n(no): ").lower()
        
        
        
        if analyzeOrNot == "y":
            pulseAnalyze(xAxis, yAxis)
        elif analyzeOrNot == "n":
            print("Back to previous stage...")
        showOrNot = input("Continue to query? y(yes), n(no): ").lower()
        if showOrNot == "n":
            showCase1 = False
        elif showOrNot == "y":
            showCase1 = True
        else:
            print("Invalid input. Please enter again...")
        
    backToMain()

#############################(CASE 2)################################################################################           

def case2():
    # Depict all pulses on the entire data graph
    
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
    
    showOrNot = input("Back to the main menu? y(yes), n(no): ").lower()
    if showOrNot == "n":
            showDialog = False
    elif showOrNot == "y":
            showDialog = True
    else:
        print("Invalid input. Please enter again...")
        backToMain()

while showDialog == True: 
    firstSelection = int(input("Please select the operation to be performed: \n 1: Query in all pulses intercepted. \n 2: Check the distribution of pulses in the complete image: ")) 
    if firstSelection == 1:
        case1()
    elif firstSelection == 2:
        case2()
    elif firstSelection == 3:
        print("picked 3")
    else:
        print("invalid")




        