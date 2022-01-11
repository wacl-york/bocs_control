"""
Reads incoming serial data and add it to a queue.

Classes:

    DataReader

"""
import logging
import threading
from queue import Queue
import serial
from serial.tools.list_ports import comports

import bocs_control.config as cfg


class DataReader(threading.Thread):
    """
    DataReader describes a thread whose purpose is to read lines of serial input
    from a specified serial port and enqueue said lines of serial input into a
    shared FIFO queue.
    """

    def __init__(self, name: str, port_name: str, shared_queue: Queue):
        """
        Sets up serial connection.

        Args:
            - name (str): Identifier for the instrument.
            - port_name (str): Serial port location.
            - shared_queue (Queue): Global FIFO queue to add data to.

        Returns:
            None

        Raises:
            RuntimeError
        """
        threading.Thread.__init__(self)
        logging.info(f"Initialising serial reader on port name {port_name}")
        self.name = name
        self.port_name = port_name
        self.queue = shared_queue

        logging.info(f"Checking port {self.port_name} availability")
        try:
            self.check_port_available()
        except serial.serialutil.SerialException as ex:
            logging.error(f"Port {self.port_name} is unavailable")
            raise RuntimeError() from ex

        logging.info(f"Opening port {self.port_name} for read")
        try:
            self.port = serial.Serial(self.port_name, cfg.BAUD_RATE, timeout=1)
            self.port.reset_input_buffer()
        except serial.serialutil.SerialException as ex:
            logging.error(f"Can't open {self.port_name} for read")
            raise RuntimeError() from ex

    def check_port_available(self) -> None:
        """
        Check whether or not the port_name property of this object refers to a
        valid serial port exposed through /dev.

        Args:
            None.

        Returns:
            None

        Raises:
            serial.serialutil.SerialException
        """
        try:
            port_list = [port.device for port in comports(include_links=True)]
            assert self.port_name in port_list
        except AssertionError as exception:
            raise serial.serialutil.SerialException from exception

    def read_data_line(self) -> str:
        """
        Read and return a line of attached instrument data.

        Args:
            None.

        Returns:
            A line of data encoded as a string.
        """
        logging.debug(f"{self.name} reading data from {self.port_name}")
        data = self.port.readline()
        return data

    def enqueue_data(self, data: str) -> None:
        """
        Put an incoming line of data into a shared queue, ready for a DataWriter
        to process.

        Args:
            - data (str): Line of comma-separated data.

        Returns:
            None
        """
        logging.debug(f"{self.name} enqueueing data to shared queue")
        self.queue.put(f"{self.name},{data.decode()}", block=True)

        logging.debug(f"Queue is now size {self.queue.qsize()}")

    def run(self) -> None:
        """
        Main entry point for DataReader threads.

        Args:
            None

        Returns:
            None
        """
        while True:
            try:
                self.enqueue_data(self.read_data_line())
            except UnicodeDecodeError:
                logging.error(
                    f"{self.name} caught some garbage; ignoring data line"
                )
                continue
