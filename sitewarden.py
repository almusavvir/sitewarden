#!/usr/bin/env python3

## URL watcher re-write as site warden
# Sun Mar 19 9:07pm IST, 26.8C

try:
 import requests, time, subprocess, sys, socket, summary, log_handler, os
 from requests.exceptions import SSLError, ConnectionError
 from colorama import Fore, Style, Back, init

except ModuleNotFoundError:
    print(" \n[!] One or more dependencies required to run this program are missing")
    print('[*] Install required dependencies using "pip install -r requirements.txt" first\n')
    exit()

def color_reset():
    print(Fore.RESET + Back.RESET + Style.RESET_ALL, end='')

def clear():
    command = 'clear' if os.name == 'posix' else 'cls'
    subprocess.call(command, shell=True)

def continue_without_encryption(url):
    print(' [*] Continuing without encryption...')
    main_monitor_loop(url.replace('https://', 'http://'))

def main_monitor_loop(url):
    try:
        while True:
            time.sleep(intensity)
            my_request = requests.get(url)
            if my_request.status_code == 200:
                init()
                color_reset()
                print_status(url, my_request.status_code, 'Site is up', Fore.GREEN)
            else:
                print('Response failure')
                # winsound.Beep(1300,3000)
    except KeyboardInterrupt:
        print('\n [-] Program halted by keyboard interruption\n [-] Exiting...')

def print_status(url, status_code, message, color):
    seconds = time.time()
    print(f' [+] At {time.ctime(seconds)} | {Fore.YELLOW}Host - {url} | Status - {Fore.CYAN}{status_code}{Fore.WHITE} | {color}{message}')
    color_reset()

def get_user_input():
    clear()
    print(Fore.WHITE + Back.BLUE + '                              SITE WARDEN  0.2          © Al Musavvir ')
    color_reset()
    url = input('Target URI or IP        -> ')
    url = 'https://' + url
    intensity = int(input('Frequency (in seconds)  -> '))
    return url, intensity

def validate_url(url):
    try:
        return requests.get(url)
    except SSLError:
        handle_ssl_error(url)
    except ConnectionError:
        handle_connection_error()

def handle_ssl_error(url):
    print(Fore.RED + '\n [-] ERROR - SSL verification failed')
    color_reset()
    if input(' [-] Do you want to continue (y/n) ').lower() == 'y':
        continue_without_encryption(url)
    else:
        print(' [-] Exiting...')
        exit()

def handle_connection_error():
    print(Fore.RED + '\n [-] ERROR - Something went wrong - Please check connection/URL')
    color_reset()
    print(' [-] Exiting...')
    exit()

def get_host_info(url):
    try:
        ip_addr = socket.gethostbyname(url.replace('https://', ''))
        print(f'Host IP - {ip_addr}\n')
        return ip_addr
    except socket.gaierror as err:
        print(f' [-] Cannot resolve hostname - {err}')
        exit()

def monitor(url, intensity):
    prev_ip_addr = get_host_info(url)
    ping_count, success_count, ip_addr_change_count = 0, 0, 0
    log_handler.write_csvheader()

    try:
        while True:
            time.sleep(intensity)
            my_request = requests.get(url)
            ip_addr = socket.gethostbyname(url.replace('https://', ''))
            ping_count += 1

            if prev_ip_addr != ip_addr:
                print(f' [*] At {time.ctime(time.time())} | Change in target IP Address detected, new target IP > {ip_addr}')
                prev_ip_addr = ip_addr
                log_handler.write_ipchange(time.ctime(time.time()), ip_addr)
                ip_addr_change_count += 1

            handle_response(my_request, url, ip_addr, ping_count, success_count)
    except KeyboardInterrupt:
        color_reset()
        print('\nUser interrupt\n')
        summary.run_summary(success_count, ping_count, ip_addr_change_count)
        log_handler.log_file_summary(time.ctime(time.time()), success_count, ping_count, ip_addr_change_count)
        exit()

def handle_response(my_request, url, ip_addr, ping_count, success_count):
    if my_request.status_code == 200:
        init()
        success_count += 1
        print_status(url, my_request.status_code, '[OK]', Fore.GREEN)
        log_handler.write_log(ping_count, time.ctime(time.time()), ip_addr, my_request.status_code, url)
        log_handler.write_csvlog(time.ctime(time.time()), ip_addr, my_request.status_code)

    elif my_request.status_code == 404:
        print_status(url, my_request.status_code, 'Not found', Fore.WHITE + Back.RED)

    elif my_request.status_code == 403:
        print_status(url, my_request.status_code, 'Forbidden', Fore.WHITE + Back.RED)
        log_handler.write_log(ping_count, time.ctime(time.time()), ip_addr, my_request.status_code, url)
        log_handler.write_csvlog(time.ctime(time.time()), ip_addr, my_request.status_code)

    elif my_request.status_code == 503:
        print_status(url, my_request.status_code, 'Service unavailable', Fore.RED)
        log_handler.write_log(ping_count, time.ctime(time.time()), ip_addr, my_request.status_code, url)
        log_handler.write_csvlog(time.ctime(time.time()), ip_addr, my_request.status_code)

    elif my_request.status_code == 500:
        print_status(url, my_request.status_code, 'Internal server error', Fore.RED)
        log_handler.write_log(ping_count, time.ctime(time.time()), ip_addr, my_request.status_code, url)
        log_handler.write_csvlog(time.ctime(time.time()), ip_addr, my_request.status_code)  

    elif my_request.status_code == 301:
        print_status(url, my_request.status_code, 'Moved permanently', Fore.YELLOW)
        log_handler.write_log(ping_count, time.ctime(time.time()), ip_addr, my_request.status_code, url)
        log_handler.write_csvlog(time.ctime(time.time()), ip_addr, my_request.status_code)

    elif my_request.status_code == 302:
        print_status(url, my_request.status_code, 'Found (redirect)', Fore.YELLOW)  
        log_handler.write_log(ping_count, time.ctime(time.time()), ip_addr, my_request.status_code, url)
        log_handler.write_csvlog(time.ctime(time.time()), ip_addr, my_request.status_code)
    else:
        print(Fore.RED + 'Response failure')
        print(my_request.status_code)

if __name__ == "__main__":
    try:
        url, intensity = get_user_input()
        my_request = validate_url(url)
        print('\nStarting monitoring process...')
        monitor(url, intensity)
    except KeyboardInterrupt:
        print('\n [-] - Exiting...')
        clear()
        exit()
    except ValueError:
        print(' \n[!] One or more values provided as inputs are either invalid or missing\n')
        exit()
    except IndexError:
        print('\n [!] IndexError - please check for inputs provided')
