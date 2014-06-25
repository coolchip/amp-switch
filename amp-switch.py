
def isAudioPlaying():
    asoundStatus = open('/proc/asound/card0/pcm0p/sub0/status', 'r').read()
    if 'closed' in asoundStatus:
        return False
    else:
        return True

import RPi.GPIO as GPIO

def initHardware():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(11, GPIO.OUT)
    GPIO.output(11, GPIO.LOW)

def powerOn(console):
    GPIO.output(11, GPIO.HIGH)
    if console:
        print("Power ON")

def powerOff(console):
    GPIO.output(11, GPIO.LOW)
    if console:
        print("Power OFF")

import time

def main( console, powerOffDelay ):
    shutdownTimer = powerOffDelay
    power = 0
    initHardware()

    loop = True
    while loop:
        audioPlaying = isAudioPlaying()

        if audioPlaying:
            if power == 0:
                powerOn(console)
                power = 1
                shutdownTimer = powerOffDelay
            if shutdownTimer != powerOffDelay:
                shutdownTimer = powerOffDelay
                if console:
                    print('Stopping count down (Power is still ON)')
        else:
            if power == 1:
                if shutdownTimer == 0:
                    powerOff(console)
                    power = 0
                else:
                    shutdownTimer = shutdownTimer-1
                    print("count down... " + str(shutdownTimer))
        time.sleep(0.1)

import os
from optparse import OptionParser
import daemon

if __name__ == "__main__":
    parser = OptionParser( os.path.relpath(__file__) + " [-s xxx] [-c]|[-d]" )
    parser.add_option("-doff", "--poweroffdelay",  action="store", dest="poweroffdelay", default=200, type="int", help="set the power off delay time (seconds)")
    parser.add_option("-d", "--daemon", action="store_true", dest="daemon", default=False, help="run as daemon")
    parser.add_option("-c", "--console", action="store_true", dest="console", default=False, help="output on console")
    (optionen, args) = parser.parse_args()

    if optionen.daemon:
        with daemon.DaemonContext():
            main(console=False, powerOffDelay=optionen.poweroffdelay)
    else:
        main(console=optionen.console, powerOffDelay=optionen.poweroffdelay)

    sys.exit(0)
