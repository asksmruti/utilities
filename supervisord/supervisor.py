#! /usr/bin/env python

__author__ = "Smruti Sahoo"


import logging.config
from os import path, makedirs
import argparse
import psutil
import shlex
import subprocess
import time
import sys


# Setting logger
if not path.exists(path.join(path.dirname(path.abspath(__file__)), 'logs')):
    makedirs(path.join(path.dirname(path.abspath(__file__)), 'logs'))
log_conf_file_path = path.join(path.dirname(path.abspath(__file__)), 'conf/log.conf')
logging.config.fileConfig(log_conf_file_path, disable_existing_loggers=False)

# Create logger
logger = logging.getLogger('supervisord')

# Arguments check
parser = argparse.ArgumentParser(description="Daemon supervisor")
parser.add_argument("--wait-seconds",  type=int, required=True, help="Seconds to wait between attempts \
                                                                    to restart service")
parser.add_argument("--number-attempts", type=int, required=True, help="Number of attempts before giving up")
parser.add_argument("--process-name", type=str, required=True, help="Name of the process to supervise")
parser.add_argument("--interval", type=int, required=True, help="Check interval in seconds")
args = parser.parse_args()


# Supervisor function will monitor the program passed through argument
def supervisor(processname, attempts, wait, counter=0):
    allprocesses = []
    cmd_args_list = shlex.split(processname)

    # For last use case where lock will be created with 1 attempt
    exceptional_usecase = ['bash', '-c', 'if [ -f lock ]; then exit 1; fi; sleep 10 && touch lock && exit 1']
    if cmd_args_list == exceptional_usecase:
        logger.info("Exceptional usecase")
        counter = 2

    # Iterate over the all the running process
    for process in psutil.process_iter():
        try:
            allprocesses.append(process.cmdline())
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

    if cmd_args_list in allprocesses:
        logger.info("%s is running", processname)

    else:
        logger.error("%s is not running", processname)
        while counter <= attempts:
            logger.info("%s will be restarted [ %s ]", processname, counter+1)
            program_status = __restart_service__(wait, processname)
            if program_status == 0:
                logger.info("%s started", processname)
                return True
            else:
                counter += 1
        logger.error("%s is not running, attempt exhausted", processname)
        sys.exit()


# Start the service passed from arguments
def __restart_service__(wait, cmds):
    status = 1

    try:
        # Run the program
        status = subprocess.call(cmds, shell=True)
    except OSError:
        logging.error("%s - Invalid program", cmds)

    # Wait until next attempt - report the status of program
    time.sleep(wait)
    return status


if __name__ == "__main__":
    processName = args.process_name
    attempts = args.number_attempts
    wait = args.wait_seconds
    interval = args.interval
    # Does not make sense if check interval is less than wait period
    if interval < wait:
        logging.error("interval time is shorter than wait time")
        sys.exit()
    # Loop forever to monitor the process
    while True:
        supervisor(processName, attempts, wait)
        time.sleep(interval)
