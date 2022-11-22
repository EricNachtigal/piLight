import network
import socket
from time import sleep
from picozero import pico_temp_sensor, pico_led
import machine
from machine import Pin

ssid = 'Breakfast'
password = 'NatAndEric'

blue = Pin(20, Pin.OUT)
green = Pin(21, Pin.OUT)
red = Pin(22, Pin.OUT)

def connect():
    #Connect to WLAN
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    pico_led.on()
    while wlan.isconnected() == False:
        print('Waiting for connection...')
        sleep(1)
    ip = wlan.ifconfig()[0]
    print(f'Connected on {ip}')
    pico_led.off()
    return ip

def open_socket(ip):
    # Open a socket
    address = (ip, 80)
    connection = socket.socket()
    connection.bind(address)
    connection.listen(1)
    return connection

def webpage(temperature):
    #Template HTML
    html = f"""
        <!DOCTYPE html>
        <html>
        <p>Red</p>
        <form action="./redlighton">
        <input type="submit" value="Red light on" />
        </form>
        <form action="./redlightoff">
        <input type="submit" value="Red light off" />
        </form>
        <!--END RED-->
        <p>Green</p>
        <form action="./greenlighton">
        <input type="submit" value="Green light on" />
        </form>
        <form action="./greenlightoff">
        <input type="submit" value="Green light off" />
        </form>
        <!--END GREEN-->
        <p>Blue</p>
        <form action="./bluelighton">
        <input type="submit" value="Blue light on" />
        </form>
        <form action="./bluelightoff">
        <input type="submit" value="Blue light off" />
        </form>
        <!--END BLUE-->
        <p>Temperature is {temperature}</p>
        </body>
        </html>
        """
    return str(html)

def serve(connection):
    #Start a web server
    temperature = 0
    while True:
        client = connection.accept()[0]
        request = client.recv(1024)
        request = str(request)
        try:
            request = request.split()[1]
        except IndexError:
            pass
        # RED
        if request =='/redlighton?':
            red.on()
        elif request =='/redlightoff?':
            red.off()
        # END RED
        # GREEN
        elif request =='/greenlighton?':
            green.on()
        elif request =='/greenlightoff?':
            green.off()
        # END GREEN
        # BLUE
        elif request =='/bluelighton?':
            blue.on()
        elif request =='/bluelightoff?':
            blue.off()
        # END BLUE
        temperature = pico_temp_sensor.temp
        html = webpage(temperature)
        client.send(html)
        client.close()
    
try:
    ip = connect()
    connection = open_socket(ip)
    serve(connection)
except KeyboardInterrupt:
    machine.reset()