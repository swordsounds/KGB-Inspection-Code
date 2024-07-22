from gpiozero import Robot, Motor
import time
import csv
from threading import Thread

ROBOT = Robot(right=Motor(19, 13), left=Motor(18, 12))
info = {
            "dpad_up": 0,
            "dpad_down": 0,
            "dpad_left": 0,
            "dpad_right": 0,
        }
# Open the CSV file in read mode
def go():
    print('ran')
    ROBOT.forward()
    time.sleep(5)

    ROBOT.stop()
with open('data.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
             print(row.keys())
while True:
    with open('data.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)

        for key, value in reader.items():
                info[key] = value     
        if reader['dpad_up'] == 1:
            p = Thread(target=go())
            p.start()

