import re

def readStatus():
    status = ''
    f = open('/proc/asound/card0/pcm0p/sub0/status', 'r')
    for line in f:
        matchObj = re.match(r'state.*', line)
        if matchObj:
            status = matchObj.group()
            break
        matchObj = re.match(r'closed', line)
        if matchObj:
            status = matchObj.group()
            break
    return status


SHUTDOWN_TIME = 10
shutdownTimer = SHUTDOWN_TIME
power = 0

def switchOn():
    print("Power ON")
    power = 1
    shutdownTimer = SHUTDOWN_TIME
    
def switchOff():
    print("Power OFF")
    power = 0

import time

def do_main_program( console ):
    loop = True
    shutdownTimer = SHUTDOWN_TIME
    power = 0
    while loop:
        status = readStatus()

        if status == "closed":
            if power == 1:
                if shutdownTimer == 0:
                    switchOff()
                else:
                    shutdownTimer = shutdownTimer-1
                    print("count down... " + str(shutdownTimer))
        else:
            if power == 0:
                switchOn()

            if shutdownTimer != SHUTDOWN_TIME:
                shutdownTimer = SHUTDOWN_TIME
                print("Stopping count down (Power is still ON)")

        time.sleep(1)


import os
from optparse import OptionParser
import daemon

if __name__ == "__main__":
    parser = OptionParser( os.path.relpath(__file__) + " [-s xxx] [-c]|[-d]" )

    parser.add_option("-s", "--shutdowntime", dest="shutdowntime", default=10, help="set the shutdown time (seconds)")
    parser.add_option("-d", "--daemon", action="store_true", dest="daemon", default=False, help="start as daemon")
    parser.add_option("-c", "--console", action="store_true", dest="console", default=False, help="output on console")

    (optionen, args) = parser.parse_args()

    if optionen.shutdowntime:
        SHUTDOWN_TIME = SHUTDOWN_TIME
    
    if optionen.daemon:
        with daemon.DaemonContext():
            do_main_program(False)
    else:
        do_main_program(optionen.console)

    sys.exit(0)
