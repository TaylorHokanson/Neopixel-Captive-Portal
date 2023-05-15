### Raspberry Pi Pico W captive portal
A demonstration of the Pico W as captive portal for mobile-based project control without internet connectivity.

#### Equipment
- Raspberry Pi Pico W
- Neopixel ring (16 RGB leds)
- Windows PC

#### Wiring Diagram
- GP0 >> Neopixel SIG
- GND >> Neopixel GND
- TBA >> Neopixel PWR
- 500–1000 µF/6.3V Cap between PWR >> GND (prevents glitching)

#### Setup
1.  Install Thonny on Windows PC
1.  Plug in Pico W (may need to hold down BOOTSEL button)
1.  Install Micropython via Thonny
1.  Use Thonny package manager to install Micropython-Phew
1. Drop neopixel.py and main.py in the root folder

#### Case
The [3D models](3D_models) in this repo can be used as an enclosure for our simple circuit. They are designed to be lightly hot-glued together.

#### Thanks

- [blaz-r](https://github.com/blaz-r/pi_pico_neopixel)
- [kevinmcaleer](https://github.com/kevinmcaleer/cyberdog/blob/main/cyberdog.py)
