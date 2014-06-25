
def isAudioPlaying():
    asoundStatus = open('/proc/asound/card0/pcm0p/sub0/status', 'r').read()
    if 'closed' in asoundStatus:
        return False
    else:
        return True

import RPi.GPIO as GPIO

def powerOn(console):
    GPIO.output(11, GPIO.HIGH)
    if console:
        print("Power ON")

def powerOff(console):
    GPIO.output(11, GPIO.LOW)
    if console:
        print("Power OFF")

import time

def main( console = False, shutdownTime = 200 ):
    shutdownTimer = shutdownTime
    power = 0

    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(11, GPIO.OUT)
    GPIO.output(11, GPIO.LOW)

    loop = True
    while loop:
        audioPlaying = isAudioPlaying()

        if audioPlaying:
            if power == 0:
                powerOn(console)
                power = 1
                shutdownTimer = shutdownTime
            if shutdownTimer != shutdownTime:
                shutdownTimer = shutdownTime
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

    parser.add_option("-s", "--shutdowntime",  action="store", dest="shutdowntime", default=200, type="int", help="set the shutdown time (seconds)")
    parser.add_option("-d", "--daemon", action="store_true", dest="daemon", default=False, help="start as daemon")
    parser.add_option("-c", "--console", action="store_true", dest="console", default=False, help="output on console")

    (optionen, args) = parser.parse_args()

    argShutdownTime = optionen.shutdowntime
    if optionen.daemon:
        with daemon.DaemonContext():
            main(console=False, shutdownTime=argShutdownTime)
    else:
        main(console=optionen.console, shutdownTime=argShutdownTime)

    sys.exit(0)
