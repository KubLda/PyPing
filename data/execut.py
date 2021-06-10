import sys, locale, subprocess, platform,time

# with open('data/config.ini', 'r') as file:
#     lst = file.readlines()
# del lst[0]
# lst = [[str(n) for n in x.split()] for x in lst]

# host = lst[1][1]

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
