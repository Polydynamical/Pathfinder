# This will test how much memory the 257402x257402
# adjancey matrix will take up

import numpy as np
from datetime import datetime
import time
start = datetime.now()
a = np.zeros((257402, 257402), dtype=np.bool)
end = datetime.now()
print(f"Took {end-start} seconds to initialize an array using {(a.size * a.itemsize)/1e9} GB")
