"""
Try the linux command `tail`
"""

import time
import os

while True:
    os.system('touch.log && echo `date` >> test.log')
    time.sleep(5)
