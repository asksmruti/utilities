## Sample supervisord program

Sample supervisord program to monitor the application and restart the application under following condition

It should take as parameters:

• Seconds to wait between attempts to restart service
• Number of attempts before giving up
• Name of the process to supervise
• Check interval in seconds
• Generate logs in case of events.

* Install the python modules 
`pip3 install -r requirements.txt`

* Run the program


`
 python3 supervisor.py --wait-seconds 5 --number-attempts 2 --process-name 'bash -c "sleep 1 && exit 0"' --interval 15
`

* Help
```
supervisor.py --help
usage: supervisor.py [-h] --wait-seconds WAIT_SECONDS --number-attempts
                     NUMBER_ATTEMPTS --process-name PROCESS_NAME --interval
                     INTERVAL

Daemon supervisor

optional arguments:
  -h, --help            show this help message and exit
  --wait-seconds WAIT_SECONDS
                        Seconds to wait between attempts to restart service
  --number-attempts NUMBER_ATTEMPTS
                        Number of attempts before giving up
  --process-name PROCESS_NAME
                        Name of the process to supervise
  --interval INTERVAL   Check interval in seconds
```
