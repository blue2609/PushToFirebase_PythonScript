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
patientID = input("Please enter the patient ID:")
patientName = input("Please enter patient name: ")

#Ask user which arm is being measured
whichArm = input("Which arm are you measuring?\n-- type[a] for affected\n-- type[u] for unaffected\n")
while whichArm not in ('u','a'):
    whichArm = input("Please type either 'u' or 'a'\n")


#assign a proper name to the variable
if(whichArm == 'a'):
    whichArm = "affected"
elif(whichArm == 'u'):
    whichArm = "unaffected"
	
#ask user which day it is when they are measuring 
whichDay = input("Which day are you measuring: ")
whichDate = input("Which date are you measuring: ")
    


#keep track of how many times the loop has been executed
loopNumber = 0

while loopNumber < 5:

    try:
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
            arduinoOutput = serial.Serial('/dev/cu.usbmodem1421', 115200, timeout=0)
            
            for percentage in range(101):

                time.sleep(0.1)

                circumferenceReading = str((arduinoOutput.readline().decode())).strip()
                while not circumferenceReading:
                    circumferenceReading = str((arduinoOutput.readline().decode())).strip()



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



            #prints out the circumference reading at this current point
            sys.stdout.write("\nthe circumference reading is [" + circumferenceReading + "]\n\n")


            #create an empty character variable which will contain either y/n
            repeatReading = "" 

            #ask if user is happy with the current reading
            while(repeatReading != 'y') or (repeatReading != 'n'):

                repeatReading = input("Would you like to repeat the " + str(limbLocation) + "cm reading (y/n)?\n") 

                #if user wants to repeat reading, exit the if statement and repeat the measurement
                #process for this arm measurement point
                if(repeatReading == 'y'):
                    break

                #if user is satisfied with the reading, go to the next measurement point
                #and insert the current reading to the array 
                elif(repeatReading == 'n'):

                    #increment loop number
                    loopNumber += 1

                    limbLocation = loopNumber * 10

                    circumference.append(circumferenceReading)
                    break

                #otherwise, print an error messsage
                else:
                    print("\n\n************************************************")
                    print("Previous input not recognized, please try again")
                    print("************************************************\n\n")


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
    


result = fb.patch('/' + patientID, {'First_Name':patientName, 
									'PatientID': patientID})
#PUSHING DATA TO FIREBASE

result = fb.patch('/' + patientID + '/' + whichArm + '/' + whichDay, 
                                                      {'date':whichDate,
												       'wrist':circumference[0],
                                                       'tencm_reading':circumference[1],
                                                       'twentycm_reading':circumference[2],
                                                       'thirtycm_reading':circumference[3],
                                                       'fortycm_reading':circumference[4]})




