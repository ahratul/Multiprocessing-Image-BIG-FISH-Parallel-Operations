#!/usr/bin/env python
# coding: utf-8

# In[12]:


import multiprocessing
import time
import pandas as pd
import os
import csv
import os
import numpy as np
import bigfish
import bigfish.stack as stack
import bigfish.detection as detection
import bigfish.multistack as multistack
import bigfish.plot as plot
from time import sleep
from concurrent.futures import ThreadPoolExecutor
import psutil
from multiprocessing import Process


folder='path'
output_folder='path'




def image_process():
    tiff_files = [f for f in os.listdir(folder) if f.endswith('.tiff')]
    for file in tiff_files:
        filepath = os.path.join(folder, file)

        # Load the TIFF file using BigFish
        image = stack.read_image(filepath)

        # Process the image stack using some function from BigFish
        spots, threshold = detection.detect_spots(
            images=image,
            return_threshold=True,
            voxel_size=(300, 103, 103),
            spot_radius=(350, 150, 150))


        # Convert the processed stack to a Pandas DataFrame
        df = pd.DataFrame(spots, columns=["z", "y", "x"])

        # Save the DataFrame to a CSV file
        csv_file = file.replace('.tiff', '.csv')
        df.to_csv(output_folder+csv_file, index=False)




from multiprocessing import Process
if __name__ == '__main__':
    start_time = time.perf_counter()
    p1 = Process(target=image_process())
    p1.start()
    p1.join()
    end_time = time.perf_counter()
    elapsed_time = end_time - start_time
    print(f'Elapsed time: {elapsed_time:.2f} seconds')
    cpu_percent = psutil.cpu_percent()
    print(f'CPU usage: {cpu_percent}%')

    # Get information about memory usage
    memory_info = psutil.virtual_memory()
    memory_percent = memory_info.percent
    print(f'Memory usage: {memory_percent}%')

    # Get information about disk usage
    disk_info = psutil.disk_usage('/')
    disk_percent = disk_info.percent
    print(f'Disk usage: {disk_percent}%')






