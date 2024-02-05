import schedule
import time
import subprocess
import os
from app_logger import get_logger
import logging

logger = get_logger(__name__, logging.DEBUG, True, True)


script = os.path.join(os.path.dirname(__file__), "care_bot.py")


# Define the function to execute the Python script
def run_script():
    subprocess.run(["python", script])
    all_jobs = schedule.get_jobs()
    logger.info(f"{all_jobs = }")


# Schedule the script to run every day at 12:00 PM UTC+8
schedule.every().day.at("08:15", "Asia/Hong_Kong").do(run_script).tag("care_bot_task")

schedule.run_all()

all_jobs = schedule.get_jobs()
logger.info(f"{all_jobs = }")
# Keep the script running to check for scheduled tasks
try:
    while True:
        schedule.run_pending()
        time.sleep(60)  # wait for 60 seconds
except KeyboardInterrupt:
    logger.info("Received keyboard interrupt. Stopping...")
    schedule.clear("care_bot_task")
    exit()
except Exception as e:
    logger.error("Unexpected exception occurred: %s", str(e))
