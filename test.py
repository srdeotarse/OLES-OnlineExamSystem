import time
from datetime import datetime,date
print("Hello world")
timeduration = "0:1:0"
one = 1

while True: 
    onesecondstr = "0:0:"+str(one)
    onesecond = datetime.strptime(onesecondstr, '%H:%M:%S').time() 
    testimated = datetime.strptime(timeduration, '%H:%M:%S').time()            
    lefttime = datetime.combine(date.min, testimated)-datetime.combine(date.min, onesecond)  # in minutes
    secs=lefttime.seconds #timedelta has everything below the day level stored in seconds
    minutes = secs/60
    hours = secs/3600
    print(str(int(hours+minutes+secs))+" mins")
    time.sleep(1)
    one += 1
