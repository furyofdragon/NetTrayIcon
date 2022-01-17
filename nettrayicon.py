#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Provides network info with sytray icon
'''

import os
import signal
import subprocess
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GObject

UPDATE_INTERVAL_MS = 5000

currpath = os.path.dirname(os.path.realpath(__file__))
APP_NETWORK_ON = currpath + '/gtk-connect.svg'
APP_NETWORK_OFF = currpath + '/gtk-disconnect.svg'
COLLATE = "utf-8"
STATUS_UP = "up"
STATUS_DOWN = "down"


def get_ifaces():
    i = os.listdir("/sys/class/net/")
    i.remove('lo')
    return i


def update():
    ADDRINFO = []
    n_up = 0
    for IFACE in IFACES:
        status = ''
        with open("/sys/class/net/"+IFACE+"/operstate", "r") as status_file:
            status = status_file.read().strip('\n')
        if status == STATUS_UP:
            addr = subprocess.run(["ip", "-4", "-o", "addr", "sh", IFACE], stdout=subprocess.PIPE).stdout.decode(COLLATE).strip('\n').split()[3]
            ADDRINFO.append(IFACE + "\t: " + addr + "\t: " + status)
            n_up = n_up + 1
        elif status == STATUS_DOWN:
            ADDRINFO.append(IFACE + "\t: " + "No network" + "\t: " + status)
        else:
            ADDRINFO.append(IFACE + "\t: " + "No network" + "\t: " + status)
    if n_up > 0:
        icon.set_from_file(APP_NETWORK_ON)
    else:
        icon.set_from_file(APP_NETWORK_OFF)
    icon.set_tooltip_text('\n'.join(ADDRINFO))
    return True


if __name__ == "__main__":
    icon = Gtk.StatusIcon()
    icon.set_from_file(APP_NETWORK_OFF)
    icon.set_visible(True)
    IFACES = get_ifaces()
    GObject.timeout_add(UPDATE_INTERVAL_MS, update)
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    Gtk.main()
