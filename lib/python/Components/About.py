#Embedded file name: /usr/lib/enigma2/python/Components/About.py
import sys
import os
import time

def getVersionString():
    return getImageVersionString()


def getImageVersionString():
    try:
        if os.path.isfile('/var/lib/opkg/status'):
            st = os.stat('/var/lib/opkg/status')
        else:
            st = os.stat('/usr/lib/ipkg/status')
        tm = time.localtime(st.st_mtime)
        if tm.tm_year >= 2011:
            return time.strftime('%Y-%m-%d %H:%M:%S', tm)
    except:
        pass

    return _('unavailable')


def getEnigmaVersionString():
    import enigma
    enigma_version = enigma.getEnigmaVersionString()
    if '-(no branch)' in enigma_version:
        enigma_version = enigma_version[:-12]
    return enigma_version


def getKernelVersionString():
    try:
        return open('/proc/version', 'r').read().split(' ', 4)[2].split('-', 2)[0]
    except:
        return _('unknown')


def getModelString():
    try:
        file = open('/proc/stb/info/boxtype', 'r')
        model = file.readline().strip()
        file.close()
        return model
    except IOError:
        return 'unknown'


def getChipSetString():
    try:
        f = open('/proc/stb/info/chipset', 'r')
        chipset = f.read()
        f.close()
        return chipset
    except IOError:
        return 'unavailable'


def getCPUString():
    try:
        file = open('/proc/cpuinfo', 'r')
        lines = file.readlines()
        for x in lines:
            splitted = x.split(': ')
            if len(splitted) > 1:
                splitted[1] = splitted[1].replace('\n', '')
                if splitted[0].startswith('system type'):
                    system = splitted[1].split(' ')[0]

        file.close()
        return system
    except IOError:
        return 'unavailable'


def getCpuCoresString():
    try:
        file = open('/proc/cpuinfo', 'r')
        lines = file.readlines()
        for x in lines:
            splitted = x.split(': ')
            if len(splitted) > 1:
                splitted[1] = splitted[1].replace('\n', '')
                if splitted[0].startswith('processor'):
                    if int(splitted[1]) > 0:
                        cores = 2
                    else:
                        cores = 1

        file.close()
        return cores
    except IOError:
        return 'unavailable'


def getHardwareTypeString():
    try:
        if os.path.isfile('/etc/model'):
            return open('/etc/model').read().strip().upper()
        if os.path.isfile('/proc/stb/info/boxtype') and os.path.isfile('/proc/stb/info/board_revision') and os.path.isfile('/proc/stb/info/version'):
            return open('/proc/stb/info/boxtype').read().strip().upper() + ' (' + open('/proc/stb/info/board_revision').read().strip() + '-' + open('/proc/stb/info/version').read().strip() + ')'
        if os.path.isfile('/proc/stb/info/vumodel'):
            return 'VU+' + open('/proc/stb/info/vumodel').read().strip().upper() + '(' + open('/proc/stb/info/version').read().strip().upper() + ')'
        if os.path.isfile('/proc/stb/info/model'):
            return open('/proc/stb/info/model').read().strip().upper()
    except:
        pass

    return _('unavailable')


def getImageTypeString():
    try:
        return open('/etc/issue').readlines()[-2].capitalize().strip()[:-6]
    except:
        pass

    return _('undefined')


about = sys.modules[__name__]
