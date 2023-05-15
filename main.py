# Taylor Hokanson
# January 2023
# TODO: send variables back and forth to update on index page

# general
import gc
import time

# server
from phew import logging, template, server, access_point, dns
from phew.template import  render_template
from phew.server import redirect

from neopixel import Neopixel
numpix = 16
strip = Neopixel(numpix, 0, 0, "GRB")
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
white = (255, 255, 255)
off = (0, 0, 0)
strip.brightness(2)
led_speed = .02
disco = 0

#blinking LED
import machine
from machine import Pin
ssr=Pin(15,Pin.OUT)

gc.threshold(50000) # setup garbage collection

DOMAIN = "pico.wireless" # This is the address that is shown on the Captive Portal
led = machine.Pin("LED", machine.Pin.OUT)
led.on()

def color_wipe(color, led_speed):
    for x in range(numpix):
        strip.set_pixel(x, off)
        strip.show()

    for x in range(numpix):
        strip.set_pixel(x, color)
        time.sleep(led_speed)
        strip.show()

    for x in range(numpix):
        strip.set_pixel(x, off)
        time.sleep(led_speed)
        strip.show()

color_wipe(white, led_speed)

@server.route("/", methods=['GET','POST'])
def index(request):
    """ Render the Index page and respond to form requests """
    if request.method == 'GET':
        # logging.debug("Get request")
        # give the webpage access to python variables
        return render_template("index.html")
    if request.method == 'POST':
        text = request.form.get("text", None)
        #logging.debug(f'posted message: {text}')
        if text == "red":
            color_wipe(red, led_speed)
        if text == "green":
            color_wipe(green, led_speed)
        if text == "blue":
            color_wipe(blue, led_speed)
        #global disco = global disco + 1
        #return render_template("index.html", disco = str(disco))
        return render_template("index.html", disco = str(disco))

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
    #return render_template("index.html", disco = str(disco))
    return render_template("index.html")

@server.catchall()
def catch_all(request):
    """ Catch and redirect requests """
    if request.headers.get("host") != DOMAIN:
        return redirect("http://" + DOMAIN + "/wrong-host-redirect")

# Set to Accesspoint mode
ap = access_point("Fine With This")     # NAME YOUR SSID
ip = ap.ifconfig()[0]                   # Grab the IP address and store it
#logging.info(f"starting DNS server on {ip}")
dns.run_catchall(ip)                    # Catch all requests and reroute them
server.run()                            # Run the server
#logging.info("Webserver Started")
print("Webserver Started")
