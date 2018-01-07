from firebase import firebase
import serial
import time
import requests
import sys
#import simplejson as sjson

#set up the link to firebase
firebase_url = 'https://test-c6de8.firebaseio.com/'
fb = firebase.FirebaseApplication(firebase_url, None)



# /*==== === === === === === === === === === === === === === === === === == 
# make an array to store the value of each circumference reading. 
# - circumference[0] stores the value of reading 10cm away from the wrist
# - circumference[1] stores the value of reading 20cm away from the wrist
# - circumference[2] stores the value of reading 30cm away from the wrist
# - circumference[3] stores the value of reading 40cm away from the wrist
# ==== === === === === === === === === === === === === === === === === == */
circumference = []




#get patient's name
patientName = input("Please enter patient name: ")
patientID = input("Please enter patient ID: ")

#Ask user which arm is being measured
whichArm = input("Which arm are you measuring?\n-- type[a] for affected\n-- type[u] for unaffected\n")
while whichArm not in ('u','a'):
    whichArm = input("Please type either 'u' or 'a'\n")

#assign a proper name to the variable
if(whichArm == 'a'):
    whichArm = "affected"
elif(whichArm == 'u'):
    whichArm = "unaffected"
	
#ask user which day it is when they are measuring the affected arm
if(whichArm == "affected"):
	whichDay = input("Which day are you measuring: ")
    


#keep track of how many times the loop has been executed
loopNumber = 0

while loopNumber < 5:

    try:
        #make another array to store the result of every circumference at the end of each loop
        forLoopCircumferenceReading = []

        #get the current limb location which is being measured
        limbLocation = loopNumber * 10
        questionForUser = "Please measure circumference at " + str(limbLocation) +  "cm point (y/n)\n"


        #ask the patient to measure his/her circumference
        userResponse = input(questionForUser)

        #======================================================
        #if yes, then get the circumference data 
        #if no, then exit the program right away
        #if it's something else, then ask the user for another input
        #====================================================== 

        #initialise circumferenceReading variable 

        if(userResponse == 'y'):

            #Connect the python script to the arduino via serial port communication
            arduinoOutput = serial.Serial('/dev/cu.usbmodem1411', 115200, timeout=0)
            
            for percentage in range(101):

                time.sleep(0.01)

                circumferenceReading = str((arduinoOutput.readline().decode())).strip()
                while not circumferenceReading:
                    circumferenceReading = str((arduinoOutput.readline().decode())).strip()



                #add circumferenceReading to forLoopCircumferenceReading
                forLoopCircumferenceReading.append(circumferenceReading)



                #===== ANIMATION ======
                sys.stdout.write("\r") 

                sys.stdout.write("Measuring arm at %dcm point... [" % limbLocation)

                #print symbols for loading animation
                numberOfDashes = percentage//5
                numberOfSpaces = 20 - numberOfDashes
                for dash in range(numberOfDashes):
                    sys.stdout.write("=")

                #print blank spaces to fill up the leftover space
                for space in range(numberOfSpaces):
                    sys.stdout.write(" ")

                sys.stdout.write("]")

                sys.stdout.write(" %d%%" % percentage)
                sys.stdout.write(" " + circumferenceReading)
                sys.stdout.flush()
                #===== ANIMATION ======



            print("")

            #Average all values inside forLoopCircumferenceReading
            total = 0.00
            for value in range(len(forLoopCircumferenceReading)):
                total += float(forLoopCircumferenceReading[value])
                # print(float(forLoopCircumferenceReading[value]))

                # print (total)

            # print(total)
            averageCircumferenceReading = total/len(forLoopCircumferenceReading)


            #Prints out the averageCircumferenceReading value 
            sys.stdout.write("the average circumference reading is [%f]\n\n"  %  averageCircumferenceReading)

            circumference.append(averageCircumferenceReading)

            #increment loop number
            loopNumber += 1

        elif(userResponse == 'n'):

            #go to next measurement right away if user types 'n'
            loopNumber += 1
            circumference.append("N/A")

        else:
            print("\n\n************************************************")
            print("Previous input not recognized, please try again")
            print("************************************************\n\n")
    except IOError:
        print('Error! Something went wrong.')


#SUM ALL OF THE CIRCUMFERENCES TOGETHER
#USE KEYBOARD INTERRUPT TO STOP THE SLEEP FUNCTION (fix the percentage)
    


#PUSHING DATA TO FIREBASE
if(whichArm=="affected"):
	result = fb.patch('/' + patientName + '/' + whichArm + '/' + whichDay, {'wrist':circumference[0],
                                                       'tencm_reading':circumference[1],
                                                       'twentycm_reading':circumference[2],
                                                       'thirtycm_reading':circumference[3],
                                                       'fortycm_reading':circumference[4]})
elif(whichArm=="unaffected"):
	result = fb.patch('/' + patientName + '/' + whichArm,{'wrist:':circumference[0],
                                                       'tencm_reading':circumference[1],
                                                       'twentycm_reading':circumference[2],
                                                       'thirtycm_reading':circumference[3],
                                                       'fortycm_reading':circumference[4]})


