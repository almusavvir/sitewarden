#!/usr/bin/env python3

## Summarization before program exit...
## first write Thu Mar 23 11:16am

#©Al Musavvir - almusavvir.siddiqui@gmail.com

#-----------------------------------------------------------------------------------------------------

# Imports

try:
    import requests, time, subprocess, sys, socket
    from requests.exceptions import SSLError, ConnectionError
    from colorama import Fore, Style, Back, init

except ImportError:
    print(" [-] One or more packages required to run this program are missing on this computer...")
    print(' [-] Exiting...')
    exit()

def color_reset():
    print(Fore.RESET + Back.RESET + Style.RESET_ALL, end = '')

def clear():
    subprocess.call('clear', shell = True)

#----------------------------------------------------------------------------

def run_summary(success_count, ping_count, ip_addr_change_count):
    run_count = ping_count - 1
    # print('Summary bla bla bla bla bla bla bla')
    print('Total ' + str(run_count) + ' checks performed, ' + str(success_count) + ' success, ' + str(ip_addr_change_count) + ' Host IP changes')
    # print('Exiting...\n')
