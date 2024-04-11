import schedule
import time
import subprocess

def run_script():
    subprocess.run(['/usr/bin/python3', 'products.py'])


schedule.every().thursday.at('22:00').do(run_script)

while True:
    schedule.run_pending()
    time.sleep(300)
