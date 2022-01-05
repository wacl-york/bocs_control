"""=============================================================================
DataReader CLASS
--------------------------------------------------------------------------------

============================================================================="""
from datetime import datetime as dt
import logging
import sys
import threading

import serial
from serial.tools.list_ports import comports

# ===============================================================================
class DataReader(threading.Thread):
    """
    DataReader describes a thread whose purpose is to read lines of serial input
    from a specified serial port and enqueue said lines of serial input into a
    shared FIFO queue.
    """

    def __init__(self, name, port_name, shared_queue):
        threading.Thread.__init__(self)
        logging.info(f"Initialising serial reader on port name {port_name}")
        self.name = name
        self.port_name = port_name
        self.queue = shared_queue

        try:
            logging.info(f"Checking port {self.port_name} availability")
            self.check_port_available()
        except serial.serialutil.SerialException as ex:
            logging.error(f"Port {self.port_name} is unavailable")
            raise RuntimeError() from ex

        try:
            logging.info(f"Opening port {self.port_name} for read")
            self.port = serial.Serial(self.port_name, 9600, timeout=1)
            self.port.reset_input_buffer()
        except serial.serialutil.SerialException as ex:
            logging.error(f"Can't open {self.port_name} for read")
            raise RuntimeError() from ex

    def check_port_available(self):
        """
        Check whether or not the port_name property of this object refers to a
        valid serial port exposed through /dev.
        """
        try:
            port_list = [port.device for port in comports(include_links=True)]
            assert self.port_name in port_list
        except AssertionError as exception:
            raise serial.serialutil.SerialException from exception

    def read_data_line(self):
        """
        Read and return a line of attached instrument data.
        """
        logging.debug(f"{self.name} reading data from {self.port_name}")
        data = self.port.readline()
        return data

    def enqueue_data(self, data):
        """
        Put an incoming line of data into a shared queue, ready for a DataWriter
        to process.
        """
        logging.debug(f"{self.name} enqueueing data to shared queue")
        self.queue.put(f"{self.name},{data.decode()}", block=True)

        logging.debug(f"Queue is now size {self.queue.qsize()}")

    def run(self):
        """
        Main entry point for DataReader threads.
        """
        while True:
            try:
                self.enqueue_data(self.read_data_line())
            except UnicodeDecodeError:
                logging.error(
                    f"{self.name} caught some garbage; ignoring data line"
                )
                continue
