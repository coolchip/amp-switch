#!/usr/bin/env python
# The MIT License (MIT)
# 
# Copyright (c) 2014 coolchip
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import sys
import time
from threading import Timer
from optparse import OptionParser
import daemon
from gpioout import GpioOut
from consoleout import ConsoleOut
from transmitterout import TransmitterOut
from udpout import UdpOut

def isAudioPlaying():
    asoundStatus = open('/proc/asound/card0/pcm0p/sub0/status', 'r').readline()
    if 'closed' in asoundStatus:
        return False
    else:
        return True

def main( contolOut, powerOffDelay ):
    audioPlaying = False
    timer = None
    try:
        while True:
            if audioPlaying != isAudioPlaying():
                audioPlaying = isAudioPlaying()
                if audioPlaying:
                    if timer:
                        timer.cancel()
                    contolOut.powerOn()
                else:
                    timer = Timer(powerOffDelay, contolOut.powerOff, ())
                    timer.start()
            time.sleep(0.25)
    except (KeyboardInterrupt, SystemExit):
        pass
    else:
        pass

if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("-t", "--poweroffdelay",  action="store", dest="poweroffdelay", default=200, type="int", help="set the power off delay time (seconds)")
    parser.add_option("-d", "--daemon", action="store_true", dest="daemon", default=False, help="run as daemon")
    parser.add_option("-c", "--console", action="store_true", dest="console", default=False, help="output on console")
    parser.add_option("-m", "--transmitter", action="store_true", dest="transmitter", default=False, help="output on radio transmitter")
    parser.add_option("-u", "--udp", action="store_true", dest="udp", default=False, help="output on udp (powerPi)")
    (optionen, args) = parser.parse_args()

    if optionen.daemon:
        with daemon.DaemonContext():
            main( GpioOut(), powerOffDelay=optionen.poweroffdelay )
    else:
        if optionen.console:
            main( ConsoleOut(), powerOffDelay=optionen.poweroffdelay )
        elif optionen.transmitter:
            main( TransmitterOut(), powerOffDelay=optionen.poweroffdelay )
        elif optionen.udp:
            main( UdpOut(), powerOffDelay=optionen.poweroffdelay )
        else:
            main( GpioOut(), powerOffDelay=optionen.poweroffdelay )
    sys.exit(0)
