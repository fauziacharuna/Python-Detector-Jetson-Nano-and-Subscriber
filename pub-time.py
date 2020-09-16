from datetime import datetime
from threading import Timer

x=datetime.today()
y=x.replace( second=10, microsecond=0)
delta_t=y-x

secs=delta_t.seconds+1

def hello_world():
    print "hello world"
    #...

t = Timer(secs, hello_world)
t.start()