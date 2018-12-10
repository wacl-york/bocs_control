"""=============================================================================
plotting
--------------------------------------------------------------------------------
Plot a window of incoming BOCS array data.
============================================================================="""
from collections import deque
from datetime import datetime as dt
import sys
################################################################################
import numpy as np
import pyqtgraph as pg
################################################################################
def calibrate(data_type, data):
    """
    Calculate and return calibrated sensor values.
    """
    def co2(data):
        """
        Ditch useless 'CO2' data.
        """
        return np.median([data[0], data[2], data[4]])

    switch = {
        'MOS': lambda data: np.median(data) * 0.0625,
        'NO': lambda data: np.median(data) * 0.0625,
        'CO': lambda data: np.median(data) * 0.0625,
        'OX': lambda data: np.median(data) * 0.0625,
        'CO2': lambda data: co2(data)
        }
    return switch[data_type](data)

def init_plot(plot_window, plot_dict, plot_key, title):
    """
    Initialise an empty plot into a plot dictionary at key.
    """
    axis_items = {'bottom': pg.AxisItem(orientation='bottom',
                                        showValues=False),
                  'left': pg.AxisItem(orientation='left')}
    bare_plot = plot_window.addPlot(title=title, axisItems=axis_items)
    if plot_key == 'MOS':
        bare_plot.setLabel(axis='left', text='Signal (mV)')
    else:
        bare_plot.setLabel(axis='left', text='Concentration (PPM)')
    fill_values = (np.random.randint(128, 256),
                   np.random.randint(128, 256),
                   np.random.randint(128, 256),
                   32)
    plot_dict[plot_key] = bare_plot.plot(np.zeros(100), name=plot_key,
                                         fillLevel=0,
                                         fillBrush=fill_values,
                                         pen={'color': 'w', 'width': 2})

def update_plots():
    """
    Update all plots in the plotting window.
    """
    try:
        date = dt.now()
        date_string = (f'{date.year}-{str(date.month).zfill(2)}-'
                       f'{str(date.day).zfill(2)}')
        data_file = open(f'logs/SENSOR_ARRAY_1/SENSOR_ARRAY_1_{date_string}_data.log', 'r')
    except OSError:
        sys.stderr.write("ERROR: UNABLE TO OPEN DATA FILE\n")
        return None

    last_data = [np.float64(datum) for datum in deque(data_file, 1)[0].split(',')]
    data_file.close()

    timestamp = last_data[0]

    split_data = {
        'MOS': last_data[1:9],
        'NO': last_data[9:15],
        'CO': last_data[15:21],
        'OX': last_data[21:27],
        'CO2': last_data[27:33]
        }

    for sensor_type, queue in DEQUES.items():
        queue.append({
            'x': timestamp,
            'y': calibrate(sensor_type, split_data[sensor_type])
            })
        PLOTS[sensor_type].setData(x=[item['x'] for item in queue],
                                   y=[item['y'] for item in queue])
    return None
################################################################################
APP = pg.QtGui.QApplication([])
WINDOW = pg.GraphicsWindow(title='Live Indoor AQ Data')
WINDOW.showMaximized()
pg.setConfigOptions(antialias=True)

SENSOR_TYPES = ['MOS', 'NO', 'CO', 'OX', 'CO2']
PLOTS = dict()
DEQUES = dict()

for SENSOR_TYPE in SENSOR_TYPES:
    PLOTS[SENSOR_TYPE] = None
    DEQUES[SENSOR_TYPE] = deque(maxlen=100)

for index, (key, value) in enumerate(PLOTS.items()):
    init_plot(WINDOW, PLOTS, key, key)
    if index % 2 == 1:
        WINDOW.nextRow()

TIMER = pg.QtCore.QTimer()
TIMER.timeout.connect(update_plots)
TIMER.start(2000)
################################################################################
if __name__ == '__main__':
    if sys.flags.interactive != 1 or not hasattr(pg.QtCore, 'PYQT_VERSION'):
        pg.QtGui.QApplication.exec_()
