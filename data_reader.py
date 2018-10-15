"""=============================================================================
DataReader CLASS
--------------------------------------------------------------------------------

============================================================================="""
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
        self.name = name
        self.port_name = port_name
        self.queue = shared_queue

        try:
            self.check_port_available()
        except serialutil.SerialException:
            # TODO: HANDLE PORT UNAVAILABLE
            pass

        try:
            self.check_port_function()
        except serialutil.SerialException:
            # TODO: HANDLE INCORRECT PORT FUNCTION
            pass

        try:
            self.port = serial.Serial(self.port_name, 9600, timeout=1)
            self.port.reset_input_buffer()
        except serialutil.SerialException:
            # TODO: HANDLE PORT NOT OPENABLE EXCEPTION
            pass

    def check_port_available(self):
        """
        Check whether or not the port_name property of this object refers to a
        valid serial port exposed through /dev.
        """
        try:
            assert self.port_name in [port.dev for port in comports()]
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
        return self.port.readline()

    def enqueue_data(self, data):
        """
        Put an incoming line of data into a shared queue, ready for a DataWriter
        to process.
        """
        self.queue.put(data, block=True)

    def run(self):
        """
        Main entry point for DataReader threads.
        """
        while True:
            self.enqueue_data(self.read_data_line())
