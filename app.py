from rocketry import Rocketry
from rocketry.conds import time_of_day, monthly, weekly, retry
from db import get_data
from loguru import logger

app = Rocketry()

@app.task(weekly.on("Sunday") & time_of_day.between("06:00", "12:00") | retry(3))
def do_weekly():
    """Runs a task weekly on Sunday between 6 and noon. Max retries if failed: 3"""
    try:
      data = get_data('SELECT * FROM table_name')
      if not data:
         raise Exception("No data found")
      logger.info(data)
      # Do something with data
    except Exception as e:
      logger.info(e)
    

@app.task(monthly.at("15th") & time_of_day.between("06:00", "08:00") | retry(3))
def do_monthly():
    """Runs a task monthly on the 15th between 6
    and 8. Max retries if failed: 3"""
    try:
      data = get_data('SELECT * FROM table_name')
      if not data:
         raise Exception("No data found")
      logger.info(data)
      # Do something with data
    except Exception as e:
      logger.info(e)
  
  

if __name__ == "__main__":
    app.run()

