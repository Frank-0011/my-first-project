import os
import pandas as pd
import psutil
import logging
import time
from datetime import datetime
import threading  

try:
    os.remove("tasklist.txt")
except: None



# تنظیمات اولیه لاگینگ
logging.basicConfig(
    filename="system_monitor.log",
    filemode="w",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def run_cmd(cmd, fileN="result.txt"):
    fileN += ".txt"
    os.system(f"{cmd} > {fileN}")
    with open(f"{fileN}") as M:
        content = M.read()[3:]

#تسک های فعال
def run_cmd(cmd , fileN = "result.txt"):
    fileN += ".txt"

    os.system(f"{cmd} > {fileN}")
    with open(f"{fileN}") as M:
        content = M.read()[3:]

run_cmd("tasklist" , "tasklist")

with open("tasklist.txt", "r") as f:
    content = [i.strip() for i in f.readlines()[3:]]
    content = [[j for j in i.split("  ") if j!=""] for i in content]
    
pd = pd.DataFrame(content , columns = ["name" , "PID session name" , "session#" , "ram usage"])


# تابع لاگ‌برداری از دیسک
def log_disk_info():
    try:
        partitions = psutil.disk_partitions()
        logging.info("Starting disk information logging...")
        
        for partition in partitions:
            logging.info(f"Device: {partition.device}")
            logging.info(f"Mount Point: {partition.mountpoint}")
            logging.info(f"File System: {partition.fstype}")
            
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                logging.info(f"  Total Size: {usage.total / (1024**3):.2f} GB")
                logging.info(f"  Used: {usage.used / (1024**3):.2f} GB")
                logging.info(f"  Free: {usage.free / (1024**3):.2f} GB")
                logging.info(f"  Percentage Used: {usage.percent}%")
            except PermissionError:
                logging.warning(f"  Permission Denied for {partition.device}")
        
        logging.info("Disk information logging completed.")
    except Exception as e:
        logging.error(f"An error occurred while logging disk information: {e}")

# تابع لاگ‌برداری از شبکه
def log_network_info():
    logging.info("---------------------------------------------------------------------------------------------------------------------------------------------")
    logging.info("---------------------------------------------------------------------------------------------------------------------------------------------")
    logging.info("---------------------------------------------------------------------------------------------------------------------------------------------")
    logging.info("---------------------------------------------------------------------------------------------------------------------------------------------")   
    logging.info("---------------------------------------------------------------------------------------------------------------------------------------------")
    try:
        net_io = psutil.net_io_counters(pernic=True)
        logging.info("Starting network status logging...")
        
        for interface, stats in net_io.items():
            logging.info(f"Interface: {interface}")
            logging.info(f"  Bytes Sent: {stats.bytes_sent / (1024**2):.2f} MB")
            logging.info(f"  Bytes Received: {stats.bytes_recv / (1024**2):.2f} MB")
            logging.info(f"  Packets Sent: {stats.packets_sent}")
            logging.info(f"  Packets Received: {stats.packets_recv}")
        
        logging.info("Network status logging completed.")
    except Exception as e:
        logging.error(f"An error occurred while logging network status: {e}")

#تابع نمایش وضعیت cpu و ram
def monitor_cpu_ram():
    while True:
        cpu_percent = psutil.cpu_percent(interval=1)
        ram_percent = psutil.virtual_memory().percent
        bars = 40
        cpu_bars = "▮" * int((cpu_percent / 100) * bars) + "▯" * (bars - int((cpu_percent / 100) * bars))
        ram_bars = "▮" * int((ram_percent / 100) * bars) + "▯" * (bars - int((ram_percent / 100) * bars))
        print(f"\rCPU Usage: |{cpu_bars}| {cpu_percent:.2f}%   RAM Usage: |{ram_bars}| {ram_percent:.2f}%", end="")

# تابع برای اجرای لاگ‌برداری دوره‌ای
def periodic_logging():
    while True:
        log_disk_info()
        log_network_info()
        time.sleep(15)   

# اجرای هم‌زمان وظایف
if __name__ == "__main__":
    threading.Thread(target=monitor_cpu_ram, daemon=True).start()
    
    periodic_logging()
