# Create pretty visualizations by Margo Kersey
# %%
# Import packages
import requests
import pandas as pd
import numpy as np
from io import StringIO
import matplotlib.pyplot as plt
# %%
def horiz_bar_plot(task_names, task_scores, save=True, save_path=''):
    # input a dataframe for one pidn
    fig, ax = plt.subplots(figsize=(4,8))
    ax.barh(task_names, task_scores)
    ax.set_xlabel('Percentile')


