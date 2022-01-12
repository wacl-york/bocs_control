"""
Writes data from a shared queue to file.

Classes:

    DataWriter

"""
from datetime import datetime as dt
import logging
from queue import Queue
import re
import threading

import bocs_control.config as cfg


class DataWriter(threading.Thread):
    """
    DataWriter describes a thread whose purpose is to flush lines of serial
    input from a shared FIFO queue into different files, depending on the nature
    of the serial input to be flushed.
    """

    def __init__(self, shared_queue: Queue):
        """
        Sets queue.

        Args:
            shared_queue (Queue): Global FIFO queue.

        Returns:
            None
        """
        threading.Thread.__init__(self)
        logging.info("Initialising data logging thread")
        self.queue = shared_queue

    def dequeue_data(self) -> str:
        """
        Pull a line of data from the front of a shared queue.

        Args:
            None.

        Returns:
            A string with comma-delimited data fields.
        """
        logging.debug("Dequeueing data")
        line = self.queue.get(block=True, timeout=None)
        logging.debug(f"Queue size is now {self.queue.qsize()}")

        return line

    def write_data(self, data: str) -> None:
        """
        Write data to the appropriate log file, named by instrument name and
        date.

        Args:
            data (str): Incoming comma separated data.

        Returns:
            None
        """
        logging.debug("Writing data to log file")
        data_fields = data.split(",")

        if re.match("ERROR", data_fields[1]):
            logging.error(
                f"Error in received transmission. Check error log ({cfg.ERROR_LOG_FN}) for further details"
            )
            with open(cfg.ERROR_LOG_FN, "a") as error_log:
                error_log.write(data_fields[1])
            return

        if data_fields[0] not in cfg.INSTRUMENTS:
            logging.error(
                f"{data_fields[0]} isn't a recognised instrument identifier, taking timestamp from Pi clock"
            )
            date = dt.now()
        else:
            try:
                date = dt.utcfromtimestamp(int(data_fields[1]))
            except ValueError:
                logging.debug(
                    f"Unable to decode date from instrument timestamp: {data_fields[1]}"
                )
                return

        date_string = date.strftime("%Y-%m-%d")
        filename = f"{date_string}_data.log"
        try:
            with open(f"{cfg.DATA_LOG_DIR}/{filename}", "a") as data_log:
                data_log.write(",".join(data_fields[1:]))
        except OSError:
            logging.error(
                f"Unable to append to data log {cfg.DATA_LOG_DIR}/{filename}"
            )

    def run(self) -> None:
        """
        Main entry point for DataWriter threads.

        Runs an infinite loop that polls the queue and writes the available data
        to a file.

        Args:
            None.

        Returns:
            None.
        """
        logging.info("Starting data writing loop")
        while True:
            self.write_data(self.dequeue_data())
