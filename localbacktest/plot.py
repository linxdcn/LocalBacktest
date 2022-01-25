import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdate

def basic_plot(nav_df):
    nav_df = nav_df.set_index(['datetime'])
    fig = plt.gcf()
    fig.set_facecolor('white')
    with pd.plotting.plot_params.use('x_compat', True):
        nav_df.nav.plot(color='r', figsize=(16, 8), grid='on', linewidth = 2.0)
        nav_df.benchmark.plot(color='b', figsize=(16, 8), grid='on', linewidth = 2.0)
    plt.style.use('seaborn-notebook')
    plt.xticks(fontsize=8, rotation=0)
    plt.yticks(fontsize=8)
    plt.xlabel('Time', fontsize=10)
    plt.ylabel('Net Value', fontsize=10)
    plt.legend(fontsize=10)
    plt.show()