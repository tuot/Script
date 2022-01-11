import time

from tqdm import tqdm

from rich.progress import track

for i in tqdm([ i for i in range(50)]):
    time.sleep(0.1)

for i in track(range(50),disable=False):
    time.sleep(0.1)