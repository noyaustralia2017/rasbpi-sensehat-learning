#https://www.youtube.com/watch?v=7uo99ODgabQ&feature=emb_title - make light flash or turn on code learnt from here and then modified
#code was sourced from https://www.instructables.com/id/Raspberry-Pi-Park-Sensor/ and modified to meet the needs of the task as there were errors found in the source code.
#view the instructions to the actual build here: https://bndhealtheddies201.wixsite.com/piprojects
#find instructions in folder
import RPi.GPIO as GPIO  #import libraries
import time              #import libraries
GPIO.setwarnings(False)  #getting rid of any warnings that may block the code from running.

GPIO.setmode(GPIO.BCM)   #setting the pinmode to GPIo and we tell it we are  using the BCM GPIO numbers.
TRIG = 23                # We are setting the TRIG on the ultrasonic sensor to port 23
ECHO = 24                # We are setting the ECHO on the ultrasonic sensor to port 24
GREEN = 17               # We are setting the Green Light to port 17
YELLOW = 27              # We are setting the orange Light to port 27
RED = 22                 # We are setting the Red Light to port 22
BUZZER = 25              # We are setting the buzzer to port 25
GPIO.setup(TRIG,GPIO.OUT) # We are setting up the TRIG as an output.
GPIO.setup(ECHO,GPIO.IN)  # We are setting up the ECHO as an input.
GPIO.setup(GREEN,GPIO.OUT)  # We are setting up the green LED as an output
GPIO.setup(YELLOW,GPIO.OUT)  # We are setting up the yellow LED as an output
GPIO.setup(RED,GPIO.OUT)    # We are setting up the red LED as an output
GPIO.setup(BUZZER,GPIO.OUT)  # We are setting up the buzzer  as an output
start = 1                    #declaring a global variable
def no_light ():               #This is what the output should be when  the function is called. This is saying that nothing will turn on.
    GPIO.output(GREEN, GPIO.LOW)   # The green light be  off
    GPIO.output(YELLOW, GPIO.LOW)  # The yellow light be  off.
    GPIO.output(RED, GPIO.LOW)     # The red light will be off.
    GPIO.output(BUZZER, GPIO.LOW)  # The buzzer will be off.

def green_light():                  #This is what the output should be when the function green light is to be run.
    GPIO.output(GREEN, GPIO.HIGH)   # The green light will turn on.
    GPIO.output(YELLOW, GPIO.LOW)   # The yellow light be  off.
    GPIO.output(RED, GPIO.LOW)      # The red light will be off.
    GPIO.output(BUZZER, GPIO.LOW)   # The buzzer will be off.

def yellow_light():                #This is what the output should be when the function yellow light is to be run.
    GPIO.output(GREEN, GPIO.LOW)   # The green light be  off
    GPIO.output(YELLOW, GPIO.HIGH)  # The yellow light will turn on.
    GPIO.output(RED, GPIO.LOW)      # The red light will be off.
    GPIO.output(BUZZER, GPIO.LOW)  # The buzzer will be off.

def red_light():
    GPIO.output(GREEN, GPIO.LOW)     # The green light be  off
    GPIO.output(YELLOW, GPIO.LOW)   #The yellow light be  off.
    GPIO.output(RED, GPIO.HIGH)    # The red light will turn on.
    GPIO.output(BUZZER, GPIO.HIGH)  # The buzzer will turn on and make noises.

def get_distance():      #We are defining a function here called get_distance
    GPIO.output(TRIG, True) #Sets gpio output pin to a high or 1
    time.sleep(0.00001)    #sleeps or waits for 1 micro second
    GPIO.output(TRIG, False)  #Sets gpio output pin to a low or 0
    global start              #In Python, global keyword is used to create a global variable and make changes to the variable in a local context.

    while GPIO.input(ECHO) == False: 
        start = time.time()  #this lets the variable start equal time in seconds since epoch, its continuously reset while the echo = false
        
    while GPIO.input(ECHO) == True:
        end = time.time()    #this lets the variable end equal time in seconds since epoch, its continuously reset while the echo = true
        
    signal_time = end-start # basic maths variable end minus variable start equals new variable signal_time
    distance = signal_time / 0.000058  # basic maths variable signal_time divided by 0.000058 equals new variable distance
    return distance #A return statement is used to end the execution of the function call and “returns” the result 
    

while True:  #This will happen if ECHO picks something up
    distance = get_distance()
    time.sleep(0.05)
    print("distance")  #when it detects something it will print "distance"

    if distance >= 60: #if the distance is greater than the declared value then the function no_light will run. This means nothing will turn on.
        no_light()

    elif 90 > distance > 23:  #if the distance is between than the declared value then the function no_light will run. This means that function green_light will run.
        green_light()

    elif 22 > distance > 16: #if the distance is between than the declared value then the function no_light will run. This means that function green_light will run.
        yellow_light()

    elif distance <=15: #if the distance is between than the declared value then the function no_light will run. This means that function green_light will run.
        red_light()

    else:              #if there is an issue with anything like sensor not working etc. it will print "error".
        print ("error")

