import plotly.plotly as py
from plotly.graph_objs import Scatter, Layout, Figure
import time
from time import strftime
import serial
import sys
import logging

FORMAT = "%(asctime)-15s %(message)s"
logging.basicConfig(format=FORMAT,level=logging.INFO,datefmt='%Y-%m-%d %H:%M:%S')

port = '/dev/ttyAMA0'
baud = 9600
ser = serial.Serial(port=port, baudrate=baud)

username = 'jamborta'
api_key = '8cc12mt0jm'
stream_token1 = 'tlkyiiy8ai'
stream_token2 = 'katvhtjay0'

py.sign_in(username, api_key)

trace0 = Scatter(
    x=[],
    y=[],
    stream=dict(
        token=stream_token1,
	maxpoints=172800
    )
)

trace1 = Scatter(
    x=[],
    y=[],
    stream=dict(
        token=stream_token2,
	maxpoints=172800
    )
)

layout = Layout(
    title='Raspberry Pi Streaming Sensor Data'
)

fig = Figure(data=[trace0,trace1], layout=layout)

print py.plot(fig, filename='Temperature monitor', fileopt='extend')

stream1 = py.Stream(stream_token1)
stream1.open()

stream2 = py.Stream(stream_token2)
stream2.open()

f = open('sensor_reading.csv','a')

prev_temp1 = 0
prev_temp2 = 0


def readSensor(code):
    if ser.inWaiting() > 12:
        logging.info(ser.read(ser.inWaiting()))
    ser.write("a%sTEMP-----" % code)
    if ser.inWaiting() == 12:
        return float(ser.read(12)[7:])
    else:
        logging.info(ser.read(ser.inWaiting()))
        return None


try:
	#the main sensor reading loop
	while True:
		logging.info("reading sensor")	
        temp1 = readSensor("AA")
        temp2 = readSensor("AB")
        if temp1 is None or temp2 is None:
            time.sleep(30)
        i = strftime("%Y-%m-%d %H:%M:%S")
        logging.info("sending stream")
        if abs(prev_temp1 - temp1) < 50:
            stream1.write({'x': i, 'y': temp1})
            prev_temp1 = temp1
        else:
            temp1 = None
        if abs(prev_temp2 - temp2) < 50:
            stream2.write({'x': i, 'y': temp2})
            prev_temp2 = temp2
        else:
            temp2 = None
        logging.info("writing to db")
        f.write(i+","+str(temp1)+","+str(temp2)+"\n")
		# delay between stream posts
        time.sleep(30)
		#sent heartbeat
        stream1.heartbeat()
        stream2.heartbeat()
        time.sleep(30)
except KeyboardInterrupt:
    print "Shuting down"
    stream1.close()
    stream2.close()
    f.close()
    sys.exit()
