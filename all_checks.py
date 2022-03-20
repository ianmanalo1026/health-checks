import re
import shutil
import sys
import os
import socket

def check_reboot():
    """Returns True if the computer has a pending reboot"""
    return os.path.exists("/run/reboot-required")

def check_disk_full(disk, min_gb, min_percent):
    """Returns True if there isn't enough disk spae, False otherwise"""
    du = shutil.disk_usage(disk)
    #calculate the percentage of free space
    percent_free = 100 * du.free/ du.total
    #calculate how many free gigabytes
    gigabytes_free = du.free/2**30
    if percent_free < min_percent or gigabytes_free < min_gb:
        return True
    return False

def check_root_full():
    """Returns True if the root partition is full, False Otherwise."""
    return check_disk_full(disk="/", min_gb=2, min_percent=10)

def check_no_network():
    """Returns True if it failes to resolve Google's URL, False otherwise"""
    try:
        socket.gethostbyname("www.google.com")
        return False
    except:
        return True

def main():
    checks=[
        (check_reboot, "Pending Reboot"),
        (check_root_full, "Root Partition full"),
        (check_no_network, "No working Network")
    ]
    everything_ok=True
    for check,msg in checks:
        if check():
            print(msg)
            everything_ok=False
            
    if not everything_ok:
        sys.exit(1)
    print("Everythin ok.")
    sys.exit(0)
    
main()