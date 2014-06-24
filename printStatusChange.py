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

def do_main_program():
    loop = True
    while loop:
        status = readStatus()
        fp = open('status.log','a')
        fp.write(status+"\n")
        fp.close()
        print(status)
        time.sleep(5)

import daemon

if __name__ == "__main__":
    with daemon.DaemonContext():
        do_main_program()

    sys.exit(0)

