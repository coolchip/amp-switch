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

import time

def do_main_program( console ):
    loop = True
    while loop:
        status = readStatus()
        if console:
		    print(status)
        else:
            fp = open('status.log','a')
            fp.write(status+"\n")
            fp.close()
        time.sleep(5)

import os
from optparse import OptionParser 
import daemon

if __name__ == "__main__":
    parser = OptionParser( os.path.relpath(__file__) + " [-c] | [-d]" )
	
    parser.add_option("-d", "--daemon", action="store_true", dest="daemon", default=False, help="start as daemon")
    parser.add_option("-c", "--console", action="store_true", dest="console", default=False, help="output on console")

    (optionen, args) = parser.parse_args()

    if optionen.daemon: 
        with daemon.DaemonContext():
            do_main_program(False)
    else:
        do_main_program(optionen.console)

    sys.exit(0)
