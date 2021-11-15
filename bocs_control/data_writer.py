"""=============================================================================
DataWriter CLASS
--------------------------------------------------------------------------------

============================================================================="""
from datetime import datetime as dt
import logging
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

    def __init__(self, shared_queue, instrument_names):
        threading.Thread.__init__(self)
        logging.info("Initialising data logging thread")
        self.queue = shared_queue
        create_log_directories(instrument_names)

    def dequeue_data(self):
        """
        Pull a line of data from the front of a shared queue.
        """
        # TODO: MODIFY CALL TO queue.get TO INCORPORATE A SUITABLE TIMEOUT,
        # BASED ON ATTACHED INSTRUMENT RESPONSE TIMES
        # Is that necessary? Doesn't matter if writing thread is blocked does
        # it? a timeout wouldn't change anything - thread would leave this loop
        # iteration and continue to next to try again
        logging.debug("Dequeueing data")
        line = self.queue.get(block=True, timeout=None)
        logging.debug(f"Queue size is now {self.queue.qsize()}")

        return line

    def write_data(self, data):
        """
        Write data to the appropriate log file, named by instrument name and
        date.
        """
        logging.debug("Writing data to log file")
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
                # Should this ever be reached?
                date = dt.now()

            # Is there a logic flow problem here? if ERROR is in
            # data_fields, then 'date' doesn't get assigned, so the fstring
            # below will fail. Wouldn't want to attempt to write data anyway if
            # received error.
            # Should this flow be if (error): log error & return, else log data?

            # This would be more interpretable as date.strftime("%Y-%m-%d")
            date_string = (
                f"{date.year}-{str(date.month).zfill(2)}-"
                f"{str(date.day).zfill(2)}"
            )
            filename = f"{id_string}_{date_string}_data.log"
            with open(f"logs/{id_string}/{filename}", "a") as data_log:
                data_log.write(",".join(data_fields[1:]))
        # This is a big try/catch. hard to see where these exceptions were
        # thrown. Can it be refactored to have exceptions handled closer to
        # where they were called?
        except OSError:
            # TODO: HANDLE INABILITY TO OPEN DATA LOG
            logging.error("Unable to append to data log")
        except ValueError:
            logging.debug(
                f"Unable to decode date from instrument timestamp: {data_fields[1]}"
            )

    def run(self):
        """
        Main entry point for DataWriter threads.
        """
        logging.info("Starting data writing loop")
        while True:
            self.write_data(self.dequeue_data())


def create_log_directories(instrument_names):
    """
    Create a directory to store instrument log files.
    """
    for instrument_name in instrument_names:
        log_directory = f"logs/{instrument_name}"
        if not os.path.isdir(log_directory):
            logging.info(
                f"Log directory for instrument {instrument_name} does not exist - creating"
            )
            try:
                os.makedirs(log_directory)
            except OSError:
                # TODO: HANDLE NOT BEING ABLE TO CREATE LOG FILE
                # This seems a fatal exception. Should this be reraised and
                # handled by control.py?
                logging.error(
                    "Unable to create log directory for instrument {instrument_name}"
                )
