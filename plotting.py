"""=============================================================================
plotting
--------------------------------------------------------------------------------
Plot a window of incoming BOCS array data.
============================================================================="""
from collections import deque
import csv
import sys
################################################################################
import numpy as np
import pyqtgraph as pg
################################################################################
def median_mos(data):
    """
    Calculate and return median MOS sensor readings.
    """
    return np.median(data)

def median_no_ppm(data):
    """
    Calculate and return median NO sensor readings in PPM.
    """
    return np.median(data)

def median_co_ppm(data):
    """
    Calculate and return median CO sensor readings in PPM.
    """
    return np.median(data)

def median_ox_ppm(data):
    """
    Calculate and return median Ox sensor readings in PPM.
    """
    return np.median(data)

def median_no2_ppm(data):
    """
    Calculate and return median NO2 sensor readings in PPM.
    """
    return np.median(data)

def median_co2_ppm(data):
    """
    Calculate and return median CO2 sensor readings in PPM.
    """
    return np.median(data)

def init_plot(plot_window, plot_dict, plot_key, title):
    """
    Initialise an empty plot into a plot dictionary at key.
    """
    axis_items = {'bottom': pg.AxisItem(orientation='bottom',
                                        showValues=False),
                  'left': pg.AxisItem(orientation='left')}
    plot_dict[plot_key] = plot_window.addPlot(title=title, axisItems=axis_items)
    plot_dict[plot_key].plot(np.zeros(300),
                             name=plot_key,
                             pen={'color': 'g', 'width': 1})
    if plot_key == 'MOS':
        plot_dict[plot_key].setLabel(axis='left', text='Signal (mV)')
    else:
        plot_dict[plot_key].setLabel(axis='left', text='Concentration (PPM)')

def update_plots():
    """
    Update all plots in the plotting window.
    """
    try:
        data_file = open('logs/SENSOR_ARRAY_1.log', 'r')
    except OSError:
        sys.stderr.write("ERROR: UNABLE TO OPEN DATA FILE\n")
        return None

    last_data = deque(data_file, 1)[0].split(',')
    data_file.close()

    timestamp = last_data[0]

    split_data = {
        'MOS': last_data[1:8],
        'NO': last_data[9:14],
        'CO': last_data[15:20],
        'OX': last_data[21:26],
        'NO2': last_data[27:32],
        'CO2': last_data[33:38]
        }

    for sensor_type, dq in DEQUES.items():
        pass
################################################################################
APP = pg.QtGui.QApplication([])
WINDOW = pg.GraphicsWindow(title='Live Indoor AQ Data')
pg.setConfigOptions(antialias=True)

SENSOR_TYPES = ['MOS', 'NO', 'CO', 'OX', 'NO2', 'CO2']
PLOTS = dict()
DEQUES = dict()

for SENSOR_TYPE in SENSOR_TYPES:
    PLOTS[SENSOR_TYPE] = None
    DEQUES[SENSOR_TYPE] = deque(maxlen=100)

for index, (key, value) in enumerate(PLOTS.items()):
    init_plot(WINDOW, PLOTS, key, key)
    if index % 2 == 1:
        WINDOW.nextRow()

#timer = pg.QtCore.QTimer()
#timer.timeout.connect(update_plots)
#timer.start(2000)
################################################################################
if __name__ == '__main__':
    if sys.flags.interactive != 1 or not hasattr(pg.QtCore, 'PYQT_VERSION'):
        pg.QtGui.QApplication.exec_()
