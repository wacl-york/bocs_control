"""=============================================================================
plotting
--------------------------------------------------------------------------------
Plot a window of incoming BOCS array data.
============================================================================="""
from collections import deque
import glob
import os
import sys

################################################################################
import numpy as np
import pyqtgraph as pg

################################################################################
def calibrate(data_type, data):
    """
    Calculate and return calibrated sensor values.
    """
    gain_scaled = list(map(lambda x: x * 0.0625, data))

    def voc(data):
        """
        Return median scaled VOC sensor value.
        """
        return np.median(data) / 1000

    def no(data):
        """
        Return median calibrated NO sensor value.
        """
        return (
            np.median(
                [
                    (((data[0] - 225) - (data[1] - 245)) / 309) * 1000,
                    (((data[2] - 225) - (data[3] - 245)) / 309) * 1000,
                    (((data[4] - 225) - (data[5] - 245)) / 309) * 1000,
                ]
            )
            + 276
        )

    def no2(data):
        """
        Return median calibrated NO2 sensor value.
        """
        return np.median(
            [
                (((data[0] - 225) - (data[1] - 245)) / 309) * 1000,
                (((data[2] - 225) - (data[3] - 245)) / 309) * 1000,
                (((data[4] - 225) - (data[5] - 245)) / 309) * 1000,
            ]
        )

    def co(data):
        """
        Return median calibrated CO sensor value.
        """
        return (
            np.median(
                [
                    (((data[0] - 270) - (data[1] - 340)) / 420) * 1000,
                    (((data[2] - 270) - (data[3] - 340)) / 420) * 1000,
                    (((data[4] - 270) - (data[5] - 340)) / 420) * 1000,
                ]
            )
            + +1660
        )

    def ox(data):
        """
        Return median calibrated Ox sensor value.
        """
        return (
            np.median(
                [
                    (((data[0] - 260) - (data[1] - 300)) / 298) * 1000,
                    (((data[2] - 260) - (data[3] - 300)) / 298) * 1000,
                    (((data[4] - 260) - (data[5] - 300)) / 298) * 1000,
                ]
            )
            - 100
        )

    def co2(data):
        """
        Ditch useless 'CO2' data.
        """
        return (
            np.median(
                [
                    (1350 + (3500 * data[0])) / 1000,
                    (1350 + (3500 * data[2])) / 1000,
                    (1350 + (3500 * data[4])) / 1000,
                ]
            )
            + 370
        )

    switch = {"VOC": voc, "NO": no, "CO": co, "OX": ox, "NO2": co2, "CO2": no2}

    return switch[data_type](gain_scaled)


def init_plot(plot_window, plot_dict, plot_key, title):
    """
    Initialise an empty plot into a plot dictionary at key.
    """
    axis_items = {
        "bottom": pg.AxisItem(orientation="bottom", showValues=False),
        "left": pg.AxisItem(orientation="left"),
    }
    bare_plot = plot_window.addPlot(title=title, axisItems=axis_items)
    if plot_key == "VOC":
        bare_plot.setLabel(axis="left", text="V")
    elif plot_key == "CO2":
        bare_plot.setLabel(axis="left", text="PPM")
    else:
        bare_plot.setLabel(axis="left", text="PPB")
    fill_values = (
        np.random.randint(128, 256),
        np.random.randint(128, 256),
        np.random.randint(128, 256),
        32,
    )
    plot_dict[plot_key] = bare_plot.plot(
        np.zeros(100),
        name=plot_key,
        fillLevel=0,
        fillBrush=fill_values,
        pen={"color": "w", "width": 2},
    )


def update_plots():
    """
    Update all plots in the plotting window.
    """
    try:
        data_file = open(
            max(glob.glob("logs/SENSOR_ARRAY_A/*"), key=os.path.getctime)
        )
    except OSError:
        sys.stderr.write("ERROR: UNABLE TO OPEN DATA FILE\n")
        sys.stderr.flush()
        return None

    last_data = [
        np.float64(datum) for datum in deque(data_file, 1)[0].split(",")
    ]
    data_file.close()

    timestamp = last_data[0]

    split_data = {
        "VOC": last_data[1:9],
        "NO": last_data[9:15],
        "CO": last_data[15:21],
        "OX": last_data[21:27],
        "NO2": last_data[33:39],
        "CO2": last_data[27:33],
    }

    for sensor_type, queue in DEQUES.items():
        try:
            queue.append(
                {
                    "x": timestamp,
                    "y": calibrate(sensor_type, split_data[sensor_type]),
                }
            )
            PLOTS[sensor_type].setData(
                x=[item["x"] for item in queue],
                y=[item["y"] for item in queue],
            )
        except IndexError:
            err_string = (
                f"ERROR: UNABLE TO UPDATE {sensor_type} PLOT THIS "
                "TIMESTEP, ATTEMPTING TO CONTINUE\n"
            )
            sys.stderr.write(err_string)
            sys.stderr.flush()
    return None


################################################################################
APP = pg.QtGui.QApplication([])
WINDOW = pg.GraphicsWindow(title="Live Indoor AQ Data")
WINDOW.showMaximized()
pg.setConfigOptions(antialias=True)

SENSOR_TYPES = ["VOC", "NO", "CO", "OX", "NO2", "CO2"]
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
if __name__ == "__main__":
    if sys.flags.interactive != 1 or not hasattr(pg.QtCore, "PYQT_VERSION"):
        pg.QtGui.QApplication.exec_()
