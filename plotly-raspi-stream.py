import plotly.plotly as py
from plotly.graph_objs import Scatter, Layout, Figure
import time
from time import strftime
import serial
import sys

port = '/dev/ttyAMA0'
baud = 9600
ser = serial.Serial(port=port, baudrate=baud)

username = 'jamborta'
api_key = '8cc12mt0jm'
stream_token1 = '4uknclomb5'
stream_token2 = 'katvhtjay0'

py.sign_in(username, api_key)

trace1 = Scatter(
    x=[],
    y=[],
    stream=dict(
        token=stream_token1
    )
)

trace2 = Scatter(
    x=[],
    y=[],
    stream=dict(
        token=stream_token2
    )
)

layout = Layout(
    title='Raspberry Pi Streaming Sensor Data'
)

fig = Figure(data=[trace1,trace2], layout=layout)

print py.plot(fig, filename='Temperature monitor')

stream1 = py.Stream(stream_token1)
stream1.open()

stream2 = py.Stream(stream_token2)
stream2.open()

try:
	#the main sensor reading loop
	while True:
	
		ser.write("aAATEMP-----")
        	temp1 = float(ser.read(12)[7:])
		ser.write("aABTEMP-----")
        	temp2 = float(ser.read(12)[7:])
		i = strftime("%Y-%m-%d %H:%M:%S")
        	stream1.write({'x': i, 'y': temp1})
        	stream2.write({'x': i, 'y': temp2})
        	# delay between stream posts
        	time.sleep(5)
except KeyboardInterrupt:
	print "Shuting down"
	stream1.close()
	stream2.close()
	sys.exit()
