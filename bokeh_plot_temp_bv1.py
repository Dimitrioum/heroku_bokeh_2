import pandas as pd
import numpy as np
from bokeh.plotting import figure, curdoc
from bokeh.io import output_file, show, output_notebook
from bokeh.models import CustomJS
from bokeh.models.widgets import CheckboxGroup
from bokeh.layouts import row, column
from bokeh.palettes import Category20
from bokeh.models.annotations import Title, Legend
from bokeh.models import LinearAxis, Range1d
Category10 = Category20[14]
# from bokeh.plotting import reset_output
# reset_output()

bv1 = pd.read_csv('datasets/bv1_sensors_rus_v3.csv')
# bv2 = pd.read_csv('datasets/bv2_sensors_rus_v4.csv')

bv1['время формирования точки на БВ'] = pd.to_datetime(bv1['время формирования точки на БВ'])
bv1['время прихода точки на сервере'] = pd.to_datetime(bv1['время прихода точки на сервере'])

# bv2['время формирования точки на БВ'] = pd.to_datetime(bv2['время формирования точки на БВ'])
# bv2['время прихода точки на сервере'] = pd.to_datetime(bv2['время прихода точки на сервере'])

df = bv1[(bv1['Секция №1 Температура НП, t°'] < bv1['Секция №1 Температура НП, t°'].quantile(.96))
    & (bv1['Секция №3 Температура НП, t°'] < bv1['Секция №3 Температура НП, t°'].quantile(.83))]

df['время формирования точки на БВ'] = pd.to_datetime(df['время формирования точки на БВ'], format='%d/%m/%Y')

p1 = figure(x_axis_type='datetime', plot_width=2500)
# p1.extra_y_ranges = {"binary": Range1d(start=-2, end=2)}
aline = p1.circle(df['время формирования точки на БВ'], df['Секция №1 Температура НП, t°'], line_width=2, color=Category10[0])
bline = p1.circle(df['время формирования точки на БВ'], df['Секция №3 Температура НП, t°'], line_width=2, color=Category10[4])

# p2 = figure(x_axis_type='datetime', plot_width=10000)
# eline = p1.circle(df['время прихода точки на сервере'], df['Скорость'], line_width=2, color=Viridis6[5])

p1.yaxis.axis_label = 'Температура НП'
p1.xaxis.axis_label = 'время формирования точки на БВ'
# p2.yaxis.axis_label = 'Скорость'
# p2.xaxis.axis_label = 'время формирования точки на БВ'

legend = Legend(items=[
    ("Секция №1 Заливная горловина", [aline]),
    ("Секция №1 Датчик на дне отсека", [bline]),
    ("Секция №1 Датчик в сливной магистрали", [cline]),
    ("Секция №1 Уровень НП", [dline]),
    ("Cекция №3 Заливная горловина", [eline]),
    ("Секция №3 Датчик на дне отсека", [fline]),
    ("Секция №3 Датчик в сливной магистрали", [gline]),
    ("Секция №3 Уровень НП", [hline]),
    ("Cекция №4 Заливная горловина", [iline]),
    ("Секция №4 Датчик на дне отсека", [jline]),
    ("Секция №4 Датчик в сливной магистрали", [kline]),
], location=(0, 250))

t = Title()
t.text = 'Temperatures_BV1'
p1.title = t
# p2.title = t
p1.add_layout(legend, 'left')
p1.add_layout(LinearAxis(y_range_name="binary"), 'right')
# p2.add_layout(legend, 'left')
checkboxes = CheckboxGroup(labels=list(['Секция №1 Температура НП, БВ1', 'Секция №3 Температура НП, БВ1']),
                           active=[0, 1])
callback = CustomJS(code="""aline.visible = false; // aline and etc.. are 
                            bline.visible = false; // passed in from args
        
                            // cb_obj is injected in thanks to the callback
                            if (cb_obj.active.includes(0)){aline.visible = true;} 
                                // 0 index box is aline
                            if (cb_obj.active.includes(1)){bline.visible = true;} 
                                // 1 index box is bline
                            """,
                            args={'aline': aline, 'bline': bline})
checkboxes.js_on_click(callback)
layout = row(p1, checkboxes)
# output_file('BV2_DUT_sensors_134_sections.html')
# show(column(p1, p2, checkboxes))
curdoc().add_root(layout)
curdoc().title="Tenperatures_BV2"

show(layout)