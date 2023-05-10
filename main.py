# Based on CyberDog by Kevin McAleer
# Taylor Hokanson
# January 2023

# general
import gc
import time

# server
from phew import logging, template, server, access_point, dns
from phew.template import  render_template
from phew.server import redirect

import time
from neopixel import Neopixel
numpix = 16
strip = Neopixel(numpix, 0, 0, "GRB")
red = (255, 0, 0)
off = (0, 0, 0)
strip.brightness(2)

#blinking LED
import machine
from machine import Pin
ssr=Pin(15,Pin.OUT)

gc.threshold(50000) # setup garbage collection

DOMAIN = "pico.wireless" # This is the address that is shown on the Captive Portal
led = machine.Pin("LED", machine.Pin.OUT)
led.on()

my_var = "Hello World!"
my_var2 = ""
solenoid_status = False

for x in range(numpix):
    strip.set_pixel(x, off)
    strip.show()    

for x in range(numpix):
    strip.set_pixel(x, red)
    time.sleep(0.02)
    strip.show()
    
for x in range(numpix):
    strip.set_pixel(x, off)
    time.sleep(0.02)
    strip.show()    

@server.route("/", methods=['GET','POST'])
def index(request):
    """ Render the Index page and respond to form requests """
    if request.method == 'GET':
        #logging.debug("Get request")
        # give the webpage access to python variables
        return render_template("index.html", my_var, my_var2)
    if request.method == 'POST':
        #text = request.form.get("text", None)
        #logging.debug(f'posted message: {text}')
        #return render_template("index.html", text=text)
        text = "clicked"
        logging.debug(f'posted message: {text}')
        solenoid_status = True;
        if solenoid_status == True:
            print("firing!")
            #led.on()
            ssr.value(1)
            time.sleep(1)
            ssr.value(0)
            #led.off()
            print("done.")
            solenoid_status = False;
        return render_template("index.html")

@server.route("/wrong-host-redirect", methods=["GET"])
def wrong_host_redirect(request):
  # if the client requested a resource at the wrong host then present 
  # a meta redirect so that the captive portal browser can be sent to the correct location
  body = "<!DOCTYPE html><head><meta http-equiv=\"refresh\" content=\"0;URL='http://" + DOMAIN + "'/ /></head>"
  logging.debug("body:",body)
  return body

@server.route("/hotspot-detect.html", methods=["GET"])
def hotspot(request):
    """ Redirect to the Index Page """
    return render_template("index.html")

@server.catchall()
def catch_all(request):
    """ Catch and redirect requests """
    if request.headers.get("host") != DOMAIN:
        return redirect("http://" + DOMAIN + "/wrong-host-redirect")

# Set to Accesspoint mode
ap = access_point("FWT")  # Change this to whatever Wifi SSID you wish
ip = ap.ifconfig()[0]                   # Grab the IP address and store it
logging.info(f"starting DNS server on {ip}")
dns.run_catchall(ip)                    # Catch all requests and reroute them
server.run()                            # Run the server
logging.info("Webserver Started")