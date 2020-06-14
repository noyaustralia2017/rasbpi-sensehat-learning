# Aspects of the data logger were sourced from: https://projects.raspberrypi.org/en/projects/sense-hat-data-logger #
# The code for the data logger was done by using the tutorial from here: https://github.com/raspberrypilearning/sense-hat-data-logger/blob/master/worksheet.md #
# The code for taking pictures from the camera was sourced from doing the Pi Camera tutoiral found here: https://projects.raspberrypi.org/en/projects/getting-started-with-picamera/5 #
#Special thanks to Ms Maher who assisted in getting the data logger and the camera code to run together #
# import libraries that will be used to run the program #
from sense_hat import SenseHat
from datetime import datetime
from time import sleep
from picamera import PiCamera


# this is where we set up logging settings alognside other important items like the color red for the LED screen etc. #
FILENAME = "" #this is setting up the filename for our output of data
WRITE_FREQUENCY = 100 # this code is determining how often the program will write data out to the file. In this case it will collect 100 lines of data and then add these to the file in one go.
red = (255,0,0) #red color for LED
green = (0,255,0) #green color for LED
sense = SenseHat()
batch_data= [] #this will add the sense_data lines untill it reaches the write frequency.
camera = PiCamera()
camera.rotation = 180 #just flipping the camera for taking pics.

id = 1

# In this section we define functions etc. #
def file_setup(filename): #in this function we make a function that sets up a CSV file everyime we run the code and it will contain the parameers as set below
    header  =["temp_h","temp_p","humidity","pressure", "temp", "timestamp"] #these will be our headers for our CSV file which records our data.

    with open(filename,"w") as f:
        f.write(",".join(str(value) for value in header)+ "\n")


    
def get_sense_data(): #this function is pretty much saying to get the readings from the various sensors built into the SenseHat
    sense_data=[] #sets up list structure to gather the data
    sense_data.append(sense.get_temperature_from_humidity()) #get temperature from humidity
    sense_data.append(sense.get_temperature_from_pressure()) #get temperature from humidity
    sense_data.append(sense.get_humidity()) #get humidity readings from sensors
    sense_data.append(sense.get_pressure()) #get pressure readings from sensor
    sense_data.append(sense.get_temperature()) #get the temperature by itself
    sense_data.append(datetime.now()) #get the data and time for when the reading was taken

    return sense_data #this will return that data


def log_data():
    output_string = ",".join(str(value) for value in sense_data)
    batch_data.append(output_string)
    print('Captured sensor data') #once sensor reading is taken it will print 'captured sensor data' so that we know that the data from sesnors has been captured. It's like a safety measure we take just so we know this aspect of the code works.


def cam(id): #this is the function for the camera
        camera.capture('img'+str(id)+'.jpg') #this will pretty much capture the image
        print('Captured image') #once image is taken it will print 'captured image' so that we know that the image has been captured. It's like a safety measure we take just so we know the program works.


def nope(): # this is a function for the LED screen. It will display real time data on the LED screen for users
    nope = sense.get_humidity() 
    if nope > 30: # this aspect of code is saying if the humidity is greater than 30
        sense.clear(red) # the LED screen will go red
    elif nope < 29 and nope > 10: # this aspect of code is saying if the humidity is greater than 10 and less than 29 
        sense.clear(green) # the LED screen will go green
    sleep(0.1) #how long the color will display for
    sense.show_message(str(round(nope,1))) # this will do a roll of the text that shows the real time value of the humidity of the room

def pres(): # this is a function for the LED screen. It will display real time data on the LED screen for users
    pres = sense.get_pressure() # this is to simpplify things down and say pres means to get the pressure from the sensor. 
    if pres > 800: #if pressure is greater than 800 the screen will be read
        sense.clear(red)
    elif pres < 799 and pres > 400: #if the pressure is less than 799 and greater than 400 the LED screen will be green
        sense.clear(green)
    sleep(0.1)#how long the color will display for
    sense.show_message(str(round(pres,1))) # this will do a roll of the text that shows the real time value of the atmospheric pressure of the room

def temp(): # this is a function for the LED screen. It will display real time data on the LED screen for users
    temp = sense.get_temperature() # this is to simpplify things down and say temp means to get the temperature from the sensor. 
    if temp > 30: #if pressure is greater than 30 the screen will be red
        sense.clear(red)
    elif temp < 29 and temp > 10: # this aspect of code is saying if the humidity is greater than 10 and less than 29 
        sense.clear(green) #the LED will go green
    sleep(0.1)#how long the color will display for
    sense.show_message(str(round(temp,1))) # this will do a roll of the text that shows the real time value of the temperature of the room



# this is the part where the main action happens #

if FILENAME == "":
    filename = "SenseLog-"+str(datetime.now())+".csv" #this pretty much helps with the naming of the file of the CSV. It will pretty much save the name of the CSV as the data and time this program was run. 
else:
    filename = FILENAME+"-"+str(datetime.now())+".csv" #if a filename hasn't been set this code will make it set to that of the date and time.

file_setup(filename) #this pretty much calls the function of file)set up to work and do what is said in the above code

while True: #this is pretty much starting up a loop of the programs below for as long as the program is run below. It will execute the code below until told to stop.
    sense_data = get_sense_data()
    log_data()
    cam(id)
    id = id + 1
    with open(filename,"a") as f: # this code here opens the file in append mode which adds the data at the end point of the file rather than overwriting.
            for line in batch_data:
                f.write(line + "\n")
            batch_data = []
            print("Writing to file..") # this will show whenever data is being written. it's not needed but it is there as a safety net so that we know that data is being written and the program works.
    sleep(5)
    for event in sense.stick.get_events(): # this will be the code for when we want to display the live temperature readings. this utilises the joystick on the SenseHat
        if event.action == "pressed": #if the joystick is pressed
            if event.direction =="up": #  in the up direction, it will run the function - nope() which will display the humidity
                nope()
            elif event.direction == "down": #else if the joystick is pushed down it will run the function - pres() which will show the pressure in realtime
                pres()
            elif event.direction == "left": #else if the joystick is pushed left it will run the function - temp() which will show the temperature currently in realtime
                temp()
        

