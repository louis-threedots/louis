from arduino import Arduino
import time
ar = Arduino()
print("sleep")
time.sleep(4)
print("slept")
ar.discover()
