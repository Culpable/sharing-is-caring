import plotly.figure_factory as ff
import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib, random
import chardet

hex_colors_dic = {}
rgb_colors_dic = {}
hex_colors_only = []
for name, hex in matplotlib.colors.cnames.items():
    hex_colors_only.append(hex)
    hex_colors_dic[name] = hex
    rgb_colors_dic[name] = matplotlib.colors.to_rgb(hex)

def find_encoding(fname):
    r_file = open(fname, 'rb').read()
    result = chardet.detect(r_file)
    charenc = result['encoding']
    return charenc

# filename = r'C:\Python\Notebook\activity-ribbons\WAIO DW - Rake Cycle Leg Actuals 2020-02-17.csv'

userinput = """Enter the name of your csv file, remembering the .csv (e.g. 'test.csv', but without the ')
Note:
- Make sure the file is in the same directory as this script
- Make sure the file contains the four headings 'Train Number','Cycle Leg Name','START_CYCLE_POINT_DATETIME','END_CYCLE_POINT_DATETIME'
Please enter your filename: 
"""

filename = input(userinput)
my_encoding = find_encoding(filename)


data = pd.read_csv(filename, encoding=my_encoding)
my = data[['Train Number','Cycle Leg Name','START_CYCLE_POINT_DATETIME','END_CYCLE_POINT_DATETIME']].copy()
new = my.groupby(['Train Number', 'Cycle Leg Name'])
my_df = []
for idx, df_select in new:
    current_train = idx[0]
    current_cycle = idx[1]
    start = df_select['START_CYCLE_POINT_DATETIME'].values[0].replace("/","-")
    finish = df_select['END_CYCLE_POINT_DATETIME'].values[0].replace("/","-")
    my_df.append(dict(Task=current_train, Start=start, Finish=finish, Cycle=current_cycle))

cycle_number = []
for ele in my_df:
    cycle_number.append(ele['Cycle'])
uni = np.unique(np.asarray(cycle_number))
colors = {}
for state in uni:
    colors[state] = random.choice(hex_colors_only)

gheight = len(my_df) * 3

fig = ff.create_gantt(my_df, colors=colors, index_col='Cycle', title='Daily Schedule', height=gheight,
                      show_colorbar=True, bar_width=0.2, showgrid_x=True, showgrid_y=True,group_tasks=True)
fig.show()