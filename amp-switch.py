# This file is part of Amp Switch
#
# Copyright (C) 2014 Sebastian Balling <coolchip@gmx.de>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import time
from threading import Timer
from optparse import OptionParser
import daemon
from gpioout import GpioOut
from consoleout import ConsoleOut

def isAudioPlaying():
    asoundStatus = open('/proc/asound/card0/pcm0p/sub0/status', 'r').readline()
    if 'closed' in asoundStatus:
        return False
    else:
        return True

def main( contolOut, powerOffDelay ):
    audioPlaying = False
    timer = None
    while True:
        if audioPlaying != isAudioPlaying():
            audioPlaying = isAudioPlaying()
            if audioPlaying:
                if timer:
                    timer.cancel()
                    #print("Delayed Power off canceled...")
                contolOut.powerOn()
            else:
                timer = Timer(powerOffDelay, contolOut.powerOff, ())
                timer.start()
        time.sleep(0.25)

if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("-t", "--poweroffdelay",  action="store", dest="poweroffdelay", default=200, type="int", help="set the power off delay time (seconds)")
    parser.add_option("-d", "--daemon", action="store_true", dest="daemon", default=False, help="run as daemon")
    parser.add_option("-c", "--console", action="store_true", dest="console", default=False, help="output on console")
    (optionen, args) = parser.parse_args()

    if optionen.daemon:
        with daemon.DaemonContext():
            main( GpioOut(), powerOffDelay=optionen.poweroffdelay )
    else:
        if optionen.console:
            main( ConsoleOut(), powerOffDelay=optionen.poweroffdelay)
        else:
            main( GpioOut(), powerOffDelay=optionen.poweroffdelay )
    sys.exit(0)
