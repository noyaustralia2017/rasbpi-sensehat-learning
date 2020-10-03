# source code linking to Anvil was sourced from: https://anvil.works/blog/raspberry-pi-4-web-ide #

import anvil.server #import libraries i.e. the Anvil library. Mianly connects to Anvil server
from anvil.tables import app_tables #links to Anvil table
from sense_hat import SenseHat #sensehat library
from datetime import datetime  #date time library
import time  #time library      
from picamera import PiCamera #pi camera library

camera = PiCamera() #declaring pi camera as camera
sense = SenseHat() #declaring sensehat as sense
red = (255,0,0) #red color for LED
green = (0,255,0) #green color for Led scren
id = 1 #using the ID part to name files etc. was suggested and developed by Ms Maher
camera.rotation = 180 #just flipping the camera for taking pics.
anvil.server.connect("") #unique server code for data to be sent to

def cam(id): #this is the function for the camera
        camera.capture('img'+str(id)+'.jpg')  #takes picture and the file name is image and as each image is taken it will be img plus a number
        print('Captured image') #when image captured it will say 'captured image'
        time.sleep(20) #sleep for 10 sec means take pics every 10 seconds.


def nope(): # this is a function for the LED screen. It will display real time data on the LED screen for users
    nope = sense.get_humidity() #just saying when we refer to nope it means get humidity
    if nope > 30: # this aspect of code is saying if the humidity is greater than 30
        sense.clear(red) # the LED screen will go red
    elif nope < 29 and nope > 10: # this aspect of code is saying if the humidity is greater than 10 and less than 29 
        sense.clear(green) # the LED screen will go green
    time.sleep(0.5) #how long the color will display for
    sense.show_message("Humidity: "+ str(round(nope,1))) # show message on LED

def pres(): # this is a function for the LED screen. It will display real time data on the LED screen for users
    pres = sense.get_pressure() # this is to simpplify things down and say pres means to get the pressure from the sensor. 
    if pres > 800: #if pressure is greater than 800 the screen will be red
        sense.clear(red)  
    elif pres < 799 and pres > 400: #if the pressure is less than 799 and greater than 400 the LED screen will be green
        sense.clear(green)
    time.sleep(0.5)#how long the color will display for
    sense.show_message("{Pressure: "+ str(round(pres,1))) # this will do a roll of the text that shows the real time value of the atmospheric pressure of the room

def temp(): # this is a function for the LED screen. It will display real time data on the LED screen for users
    temp = sense.get_temperature() # this is to simpplify things down and say temp means to get the temperature from the sensor. 
    if temp > 30: #if pressure is greater than 30 the screen will be red
        sense.clear(red)
    elif temp < 29 and temp > 10: # this aspect of code is saying if the humidity is greater than 10 and less than 29 
        sense.clear(green) #the LED will go green
    time.sleep(0.5)#how long the color will display for
    sense.show_message("Temperature: "+ str(round(temp,1)))  # show message on LED

while True: #loop untill program is killed
    app_tables.atmospherics.add_row(  #this is the table that the data will be added to
        when=datetime.now(), #get date and time and log it into the table
        pressure=sense.get_pressure(), #get pressure and log it into the table
        humidity=sense.get_humidity(), #get humidity and log it into the table
        temperature=sense.get_temperature() #get room temp. and log it into the table
    )
    time.sleep(10) #sleep 
    cam(id)#run camera function 
    id = id + 1 #run id part with naming file
    for event in sense.stick.get_events(): # this will be the code for when we want to display the live temperature readings. this utilises the joystick on the SenseHat
        if event.action == "pressed": #if the joystick is pressed
            if event.direction =="up": #  in the up direction, it will run the function - nope() which will display the humidity
                nope()
            elif event.direction == "down": #else if the joystick is pushed down it will run the function - pres() which will show the pressure in realtime
                pres()
            elif event.direction == "left": #else if the joystick is pushed left it will run the function - temp() which will show the temperature currently in realtime
                temp() 
