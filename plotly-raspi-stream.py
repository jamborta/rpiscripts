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
stream_token3 = '4uknclomb5'
stream_token4 = 'w8mbk9nv86'

py.sign_in(username, api_key)

trace0 = Scatter(
    x=[],
    y=[],
    name="bedroom",
    stream=dict(token=stream_token1,maxpoints=576)
)

trace1 = Scatter(
    x=[],
    y=[],
    name="living room",
    stream=dict(token=stream_token2,maxpoints=576)
)

trace2 = Scatter(
    x=[],
    y=[],
    name="guest room",
    stream=dict(token=stream_token3,maxpoints=576)
)

trace3 = Scatter(
    x=[],
    y=[],
    name="outside",
    stream=dict(token=stream_token4,maxpoints=576)
)

layout = Layout(
    title='Raspberry Pi Streaming Sensor Data'
)

fig = Figure(data=[trace0,trace1,trace2,trace3], layout=layout)

print py.plot(fig, filename='Temperature monitor', fileopt='extend')

stream1 = py.Stream(stream_token1)
stream1.open()

stream2 = py.Stream(stream_token2)
stream2.open()

stream3 = py.Stream(stream_token3)
stream3.open()

stream4 = py.Stream(stream_token4)
stream4.open()

prev_temp1 = 0
prev_temp2 = 0
prev_temp3 = 0
prev_temp4 = 0


def readSensor(code, sleep="015M"):
    if ser.inWaiting() > 12:
        logging.info(ser.read(ser.inWaiting()))
    ser.write("a%sTEMP-----" % code)
    time.sleep(1)
    r = ser.read(ser.inWaiting())
    ser.write("a%sSLEEP%s" % (code,sleep))
    time.sleep(1)
    logging.info("SLEEP command: " + ser.read(ser.inWaiting()))
    if len(r) == 12 and r[3:7] == "TEMP":
        temp = float(r[7:])
        logging.info("Temp read successful (%s) (%s)" % (code, str(temp)))
        return float(r[7:])
    elif len(r) == 0:
        logging.info("No message from %s" % code)
    else:
        logging.info("Extra messages waiting (%s): %s" % (code, r))
        return None

def check_temp_difference(prev_temp, temp, stream):
    if prev_temp is not None and temp is not None and abs(prev_temp - temp) < 50:
        try:
            stream.write({'x': i, 'y': temp})
        except Exception as e:
            logging.info("Error write: " + e.message)
            if e.message.startswith("Stream has not been opened yet"):
                logging.info("Opening stream")
                stream.open()
        return (temp, temp)
    elif temp is None:
        return (prev_temp, None)
    else:
        return (None, None)

def send_heartbeat(stream):
    try:
        stream.heartbeat()
    except Exception as e:
        logging.info("Error heartbeat: " + e.message)


try:
    #the main sensor reading loop
    while True:
        logging.info("reading sensor")
        #wait just a bit here so all sensors wake up
        time.sleep(0.5)
        temp1 = readSensor("AA")
        temp2 = readSensor("AB")
        temp3 = readSensor("AC")
        temp4 = readSensor("AD")
        i = strftime("%Y-%m-%d %H:%M:%S")
        logging.info("sending stream")
        (prev_temp1, temp1) = check_temp_difference(prev_temp1, temp1, stream1)
        (prev_temp2, temp2) = check_temp_difference(prev_temp2, temp2, stream2)
        (prev_temp3, temp3) = check_temp_difference(prev_temp3, temp3, stream3)
        (prev_temp4, temp4) = check_temp_difference(prev_temp4, temp4, stream4)
        logging.info("writing to db")
        f = open('sensor_reading.csv','a')
        f.write(i+","+str(temp1)+","+str(temp2)+","+str(temp3)+","+str(temp4)+"\n")
        f.flush()
        f.close()
        # delay between stream posts
        time.sleep(30)
        #sent heartbeat
        for i in range(0,29):
            send_heartbeat(stream1)
            send_heartbeat(stream2)
            send_heartbeat(stream3)
            send_heartbeat(stream4)
            time.sleep(30)
except KeyboardInterrupt:
    print "Shuting down"
    stream1.close()
    stream2.close()
    stream3.close()
    stream4.close()
    f.close()
    sys.exit()
