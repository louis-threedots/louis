from arduino import Arduino
import time
ar = Arduino(main_cell="arduino")
print("sleep")
time.sleep(4)
print("slept")
ar.discover()
