import schedule
import time
import subprocess
import os
from app_logger import get_logger
import logging

logger = get_logger(__name__, logging.INFO, True, True)
script = os.path.join(os.path.dirname(__file__), 'care_data_downloader.py')
# Set the UTC+8 timezone

# Define the function to execute the Python script
def run_script():
    subprocess.run(['python', script])

# Schedule the script to run every day at 12:00 PM UTC+8

logger.info(script)
schedule.every().day.at("11:00", 'Asia/Shanghai').do(run_script).tag('care_data_downloader_task')
schedule.every().day.at("08:15", 'Asia/Shanghai').do(run_script).tag('care_data_downloader_task')

logger.info('Running scheduler...')

# Keep the script running to check for scheduled tasks
try:
    while True:
        schedule.run_pending()
        time.sleep(5) # wait for 5 seconds
except KeyboardInterrupt:
    logger.info('Received keyboard interrupt. Stopping...')
    schedule.clear('care_data_downloader_task')
    exit()