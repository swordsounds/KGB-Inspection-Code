import os
import uuid

unique_filename = str(uuid.uuid4()).split('-')[0] #test code TEST THIS
print(os.cpu_count())
print(unique_filename)

mydict = {
    'dpad_up': 0,
    'dpad_down': 0,
    'dpad_left': 0, 
    'dpad_right': 0
    }

for key, value in mydict.items():
    mydict[key] = 2
print(mydict)