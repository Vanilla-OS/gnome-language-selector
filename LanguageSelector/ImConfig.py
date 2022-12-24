# ImConfig.py (c) 2012-2020 Canonical
# Author: Gunnar Hjalmarsson <gunnarhj@ubuntu.com>
#
# Released under the GPL
#

import os
import subprocess
import locale

class ImConfig(object):
    
    def __init__(self):
        pass

    def available(self):
        return os.path.exists('/usr/bin/im-config')

    def getAvailableInputMethods(self):
        inputMethods = sorted(subprocess.check_output(['im-config', '-l']).decode().split())
        inputMethods.append('none')
        return inputMethods

    def getCurrentInputMethod(self):
        (systemConfig, userConfig, autoConfig) = \
          subprocess.check_output(['im-config', '-m']).decode().split()[:3]
        if userConfig != 'missing':
            return userConfig

        """
        no saved user configuration
        fall back to the system configuration
        """
        system_conf = ''
        if systemConfig == 'default':
            system_conf = autoConfig
        elif os.path.exists('/etc/X11/xinit/xinputrc'):
            for line in open('/etc/X11/xinit/xinputrc'):
                if line.startswith('run_im'):
                    system_conf = line.split()[1]
                    break
        if not system_conf:
            system_conf = autoConfig
        return system_conf

    def setInputMethod(self, im):
        subprocess.call(['im-config', '-n', im])
    
if __name__ == '__main__':
    im = ImConfig()
    print('available input methods: %s' % im.getAvailableInputMethods())
    print('current method: %s' % im.getCurrentInputMethod())
    print("setting method 'fcitx'")
    im.setInputMethod('fcitx')
    print('current method: %s' % im.getCurrentInputMethod())
    print('removing ~/.xinputrc')
    im.setInputMethod('REMOVE')
