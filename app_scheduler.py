import schedule
import time
import subprocess
import os
from app_logger import get_logger
import logging

logger = get_logger(__name__, logging.INFO, True, True)

logging.basicConfig()
schedule_logger = logging.getLogger("schedule")
schedule_logger.setLevel(level=logging.DEBUG)

script = os.path.join(os.path.dirname(__file__), "care_bot.py")


# Define the function to execute the Python script
def run_script():
    subprocess.run(["python", script])
    all_jobs = schedule.get_jobs()
    logger.info(f"{all_jobs = }")


# Schedule the script to run every day at 12:00 PM UTC+8

logger.info(script)
schedule.every().day.at("08:15", "HongKong").do(run_script).tag("care_bot_task")

if os.environ.get("DEBUG", False):
    logger.info("Running script for DEBUG purposes")
    run_script()

logger.info("Running scheduler...")
subprocess.run(["python", script])
all_jobs = schedule.get_jobs()
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
