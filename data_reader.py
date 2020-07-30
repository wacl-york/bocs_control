"""=============================================================================
DataReader CLASS
--------------------------------------------------------------------------------

============================================================================="""
from datetime import datetime as dt
import sys
import threading

import serial
from serial import serialutil
from serial.tools.list_ports import comports
#===============================================================================
class DataReader(threading.Thread):
    """
    DataReader describes a thread whose purpose is to read lines of serial input
    from a specified serial port and enqueue said lines of serial input into a
    shared FIFO queue.
    """
    def __init__(self, name, port_name, shared_queue):
        threading.Thread.__init__(self)
        err_string = (f"[{dt.now().__str__()}] INFO: DataReader {name} INITIALISING WITH PORT NAME"
                      f" {port_name}\n")
        sys.stderr.write(err_string)
        self.name = name
        self.port_name = port_name
        self.queue = shared_queue

        try:
            info_string = (f"[{dt.now().__str__()}] INFO: DataReader {self.name} CHECKING PORT "
                           f"{self.port_name} AVAILABILITY\n")
            sys.stderr.write(info_string)
            self.check_port_available()
        except serialutil.SerialException:
            # TODO: HANDLE PORT UNAVAILABLE
            err_string = (f"[{dt.now().__str__()}] ERROR: DataReader {self.name} THINKS PORT "
                          f"{self.port_name} IS UNAVAILABLE\n")
            sys.stderr.write(err_string)

        try:
            info_string = (f"[{dt.now().__str__()}] INFO: DataReader {self.name} CHECKING PORT "
                           f"{self.port_name} FUNCTIONALITY\n")
            sys.stderr.write(info_string)
            self.check_port_function()
        except serialutil.SerialException:
            # TODO: HANDLE INCORRECT PORT FUNCTION
            err_string = (f"[{dt.now().__str__()}] ERROR: DataReader {self.name} THINKS PORT "
                          f"{self.port_name} IS MALFUNCTIONING\n")
            sys.stderr.write(err_string)

        try:
            info_string = (f"[{dt.now().__str__()}] INFO: DataReader {self.name} OPENING PORT "
                           f"{self.port_name} FOR READ\n")
            sys.stderr.write(info_string)
            self.port = serial.Serial(self.port_name, 9600, timeout=1)
            self.port.reset_input_buffer()
        except serialutil.SerialException:
            # TODO: HANDLE PORT NOT OPENABLE EXCEPTION
            err_string = (f"[{dt.now().__str__()}] ERROR: DataReader {self.name} CAN'T OPEN "
                          f"{self.port_name} FOR READ\n")
            sys.stderr.write(err_string)

    def check_port_available(self):
        """
        Check whether or not the port_name property of this object refers to a
        valid serial port exposed through /dev.
        """
        try:
            port_list = [port.device for port in comports(include_links=True)]
            assert self.port_name in port_list
        except AssertionError as exception:
            raise serialutil.SerialException from exception

    def check_port_function(self):
        """
        Check whether or not data can be read from the serial port, and whether
        or not any data that can be read seems sensible.
        """
        try:
            port = serial.Serial(self.port_name, 9600, timeout=1)
            port.close()
        except serialutil.SerialException as exception:
            raise serialutil.SerialException from exception

    def read_data_line(self):
        """
        Read and return a line of attached instrument data.
        """
        info_string = (f"[{dt.now().__str__()}] INFO: DataReader {self.name} READING DATA FROM "
                       f"{self.port_name}\n")
        sys.stderr.write(info_string)
        data = self.port.readline()
        return data

    def enqueue_data(self, data):
        """
        Put an incoming line of data into a shared queue, ready for a DataWriter
        to process.
        """
        info_string = (f"[{dt.now().__str__()}] INFO: DataReader {self.name} ENQUEUEING DATA TO "
                       "SHARED QUEUE\n")
        sys.stderr.write(info_string)
        sys.stderr.write(f"[{dt.now().__str__()}] INFO: QUEUE IS NOW SIZE {self.queue.qsize()}\n")
        self.queue.put(f"{self.port_name[5:]},{data.decode()}", block=True)

    def run(self):
        """
        Main entry point for DataReader threads.
        """
        while True:
            try:
                self.enqueue_data(self.read_data_line())
            except UnicodeDecodeError as exception:
                err_string = (f"[{dt.now().__str__()}] INFO: DataReader {self.name} CAUGHT SOME "
                              "GARBAGE; IGNORING DATA LINE\n")
                sys.stderr.write(err_string)
                continue
