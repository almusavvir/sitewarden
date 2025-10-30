#!/usr/bin/env python3

## Log handling for both down and uptimes...
## first write Thu Mar 23 9:21am

#©Al Musavvir - almusavvir.siddiqui@gmail.com

#-----------------------------------------------------------------------------------------------------

# Imports

try:
    import requests, time, subprocess, sys, socket, csv, os
    from requests.exceptions import SSLError, ConnectionError
    from colorama import Fore, Style, Back, init

except {ImportError, ModuleNotFoundError} :
    print(" [-] One or more packages required to run this program are missing on this computer...")
    print(' [-] Exiting...')
    exit()

# Colorama color reset and terminal 'clear' defs

def color_reset():
    print(Fore.RESET + Back.RESET + Style.RESET_ALL, end = '')


def clear():
    if os.name == 'posix':
        subprocess.call('clear', shell = True)
    else:
        subprocess.call('cls', shell = True)


#   WRITE PING TO LOG FILE

def write_log(ping_count, pingtime, ip_addr, status_code, url):
    
    file_path = "./logs/logs.txt"
    expanded_path = os.path.expanduser(file_path)

    with open(str(expanded_path), 'a') as log:
        # log.write("\nOne check performed")
        if status_code == 200:
            log.write('\n Check ' + str(ping_count) + ' At ' + str(pingtime) + ' Status of ' +  str(ip_addr) + ' Host - ' + str(url) + ' >> ' + str(status_code) + ' OK')
        elif status_code == 403:
            log.write('\n At ' + str(pingtime) + ' Status of ' + str(ip_addr) + ' >> ' + str(status_code) + ' Forbidden')
        elif status_code == 301:
            log.write('\n Check ' + str(ping_count) + ' At ' + str(pingtime) + ' Status of ' + str(ip_addr) + ' Host - ' + str(url) + ' >> ' + str(status_code) + ' Moved Permanently')
        elif status_code == 302:
            log.write('\n Check ' + str(ping_count) + ' At ' + str(pingtime) + ' Status of ' + str(ip_addr) + ' Host - ' + str(url) +  ' >> ' + str(status_code) + ' Found (Redirect)')
        elif status_code == 400:
            log.write('\n Check ' + str(ping_count) + ' At ' + str(pingtime) + ' Status of ' + str(ip_addr) + ' Host - ' + str(url) +  ' >> ' + str(status_code) + ' Bad Request')
        elif status_code == 401:
            log.write('\n Check ' + str(ping_count) + ' At ' + str(pingtime) + ' Status of ' + str(ip_addr) + ' Host - ' + str(url) +  ' >> ' + str(status_code) + ' Unauthorized')
        elif status_code == 404:
            log.write('\n Check ' + str(ping_count) + ' At ' + str(pingtime) + ' Status of ' + str(ip_addr) + ' Host - ' + str(url) +  ' >> ' + str(status_code) + ' Not Found')
        elif status_code == 408:
            log.write('\n Check ' + str(ping_count) + ' At ' + str(pingtime) + ' Status of ' + str(ip_addr) + ' Host - ' + str(url) +  ' >> ' + str(status_code) + ' Request Timeout')
        elif status_code == 429:
            log.write('\n Check ' + str(ping_count) + ' At ' + str(pingtime) + ' Status of ' + str(ip_addr) + ' Host - ' + str(url) +  ' >> ' + str(status_code) + ' Too Many Requests')
        elif status_code == 500:
            log.write('\n Check ' + str(ping_count) + ' At ' + str(pingtime) + ' Status of ' + str(ip_addr) + ' Host - ' + str(url) +  ' >> ' + str(status_code) + ' Internal Server Error')
        elif status_code == 502:
            log.write('\n Check ' + str(ping_count) + ' At ' + str(pingtime) + ' Status of ' + str(ip_addr) + ' Host - ' + str(url) +  ' >> ' + str(status_code) + ' Bad Gateway')
        elif status_code == 503:
            log.write('\n Check ' + str(ping_count) + ' At ' + str(pingtime) + ' Status of ' + str(ip_addr) + ' Host - ' + str(url) +  ' >> ' + str(status_code) + ' Service Unavailable')
        elif status_code == 504:
            log.write('\n Check ' + str(ping_count) + ' At ' + str(pingtime) + ' Status of ' + str(ip_addr) + ' Host - ' + str(url) +  ' >> ' + str(status_code) + ' Gateway Timeout')
        else:
            log.write('\n Check ' + str(ping_count) + ' At ' + str(pingtime) + ' Status of ' + str(ip_addr) + ' Host - ' + str(url) +  ' >> ' + str(status_code) + ' Response')


#  Write IP Change to log file

def write_ipchange(pingtime, ip_addr):
    with open ('logs.txt', 'a') as log:
        log.write('\n\n At ' + str(pingtime) + ' Target IP changed to ' + str(ip_addr) + '\n\n')


def log_file_summary(pingtime, success_count, ping_count, ip_addr_change_count):
    with open('logs.txt', 'a') as log:
        log.write('\n\n At ' + str(pingtime) + ' program stopped manually ----------------\n\n')
        log.write('Total ' + str(ping_count) + ' checks performed, ' + str(success_count) + ' success, ' + str(ip_addr_change_count) + ' target IP changes')
        print('Complete log can be found at ./logs/logs.txt and ./logs/logs.csv\n')

# CSV logging starts here

def write_csvheader():

    file_path = "./logs/logs.csv"
    expanded_path = os.path.expanduser(file_path)

    fields = ['Time', 'Target IP', 'Status']

    with open(str(expanded_path), 'a') as csvlog:
        csvwriter = csv.writer(csvlog)
        csvwriter.writerow(fields)


def write_csvlog(pingtime, ip_addr, status_code):

    file_path = "./logs/logs.csv"
    expanded_path = os.path.expanduser(file_path)

    rows = [pingtime, ip_addr, status_code]

    with open(str(expanded_path), 'a') as csvlog:
        csvwriter = csv.writer(csvlog);
        csvwriter.writerow(rows)
