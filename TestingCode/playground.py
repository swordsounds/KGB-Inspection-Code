import os
import uuid

unique_filename = str(uuid.uuid4()).split('-')[0] #test code TEST THIS
print(os.cpu_count())
print(unique_filename)