# Copyright 2022 Shuhei Nitta. All rights reserved.
__version__ = "0.0.6"

import pandas as pd
import matplotlib.pyplot as plt

pd.options.display.float_format = "{:.4g}".format
plt.rcParams["figure.figsize"] = (6, 9)
plt.style.use("seaborn")
