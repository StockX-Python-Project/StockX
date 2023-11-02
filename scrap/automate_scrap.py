import subprocess
import os
import schedule
import time

ROOT_PATH = os.path.dirname(os.path.abspath(__file__))


def automate_scrap():
    scraping = [
        "python",
        ROOT_PATH + "scrap.py",
    ]
    subprocess.run(scraping, check=True)


schedule.every().day().at("08:00").do(automate_scrap)

while True:
    schedule.run_pending()
    time.sleep(1)
    print("Success")
