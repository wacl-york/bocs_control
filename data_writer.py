"""=============================================================================
DataWriter CLASS
--------------------------------------------------------------------------------

============================================================================="""
from datetime import datetime as dt
import os
import re
import sys
import threading

# ===============================================================================
class DataWriter(threading.Thread):
    """
    DataWriter describes a thread whose purpose is to flush lines of serial
    input from a shared FIFO queue into different files, depending on the nature
    of the serial input to be flushed.
    """

    def __init__(self, name, shared_queue, instrument_names):
        threading.Thread.__init__(self)
        sys.stderr.write(
            f"[{dt.now().__str__()}] INFO: DataWriter {name} INITIALISING\n"
        )
        self.name = name
        self.queue = shared_queue
        create_log_directories(instrument_names)

    def dequeue_data(self):
        """
        Pull a line of data from the front of a shared queue.
        """
        # TODO: MODIFY CALL TO queue.get TO INCORPORATE A SUITABLE TIMEOUT,
        # BASED ON ATTACHED INSTRUMENT RESPONSE TIMES
        sys.stderr.write(
            f"[{dt.now().__str__()}] INFO: DataWriter {self.name} DEQUEUEING DATA\n"
        )
        sys.stderr.write(
            f"[{dt.now().__str__()}] INFO: QUEUE SIZE IS NOW {self.queue.qsize()}\n"
        )
        return self.queue.get(block=True, timeout=None)

    def write_data(self, data):
        """
        Write data to the appropriate log file, named by instrument name and
        date.
        """
        info_string = (
            f"[{dt.now().__str__()}] INFO: DataWriter {self.name} WRITING DATA TO LOG FILE"
            "\n"
        )
        sys.stderr.write(info_string)
        try:
            data_fields = data.split(",")
            id_string = data_fields[0]
            if re.match("ERROR", data_fields[1]):
                filename = f"{id_string}_error.log"
                with open(f"logs/{id_string}/{filename}", "a") as data_log:
                    data_log.write(data_fields[1])
            elif re.match("SENSOR_ARRAY_[AB]", data_fields[0]):
                date = dt.utcfromtimestamp(int(data_fields[1]))
            else:
                date = dt.now()

            date_string = (
                f"{date.year}-{str(date.month).zfill(2)}-"
                f"{str(date.day).zfill(2)}"
            )
            filename = f"{id_string}_{date_string}_data.log"
            with open(f"logs/{id_string}/{filename}", "a") as data_log:
                data_log.write(",".join(data_fields[1:]))
        except OSError:
            # TODO: HANDLE INABILITY TO OPEN DATA LOG
            err_string = (
                f"[{dt.now().__str__()}] ERROR: DataWriter {self.name} UNABLE TO APPEND TO "
                "DATA LOG\n"
            )
            sys.stderr.write(err_string)
        except ValueError:
            err_string = (
                f"[{dt.now().__str__()}] ERROR: UNABLE TO DECODE DATE FROM INSTRUMENT "
                "TIMESTAMP\n"
            )
            sys.stderr.write(err_string)

    def run(self):
        """
        Main entry point for DataWriter threads.
        """
        while True:
            self.write_data(self.dequeue_data())


def create_log_directories(instrument_names):
    """
    Create a directory to store instrument log files.
    """
    for instrument_name in instrument_names:
        log_directory = f"logs/{instrument_name}"
        if not os.path.isdir(log_directory):
            info_string = (
                f"[{dt.now().__str__()}] INFO: LOG DIRECTORY FOR INSTRUMENT {instrument_name}"
                " DOES NOT EXIST - CREATING\n"
            )
            sys.stderr.write(info_string)
            try:
                os.makedirs(log_directory)
            except OSError:
                # TODO: HANDLE NOT BEING ABLE TO CREATE LOG FILE
                err_string = (
                    "[{dt.now().__str__()}] ERROR: UNABLE TO CREATE LOG DIRECTORY FOR"
                    f" INSTRUMENT {instrument_name}\n"
                )
                sys.stderr.write(err_string)
