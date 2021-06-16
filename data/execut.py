# -*- coding: utf-8 -*-
import sys, locale, subprocess, platform,time

def ping(host):
    ping_str = "-n 1" if platform.system().lower() == "windows" else "-c 1"
    args = "ping " + " " + ping_str + " " + host
    con_out = subprocess.check_output(args, shell=True).decode('cp866')
    return con_out
def monitor(host):
    ping_out = ping(host)
    string = str(ping_out)
    output = string.split('\n')[-3:]
    return output
