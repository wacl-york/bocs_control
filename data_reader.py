"""=============================================================================
DataReader CLASS
--------------------------------------------------------------------------------

============================================================================="""
from datetime import datetime as dt
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
        # Looks like logging has levels, i.e. 'INFO', 'ERROR'.
        # I was under the impression it didn't
        err_string = (
            f"[{dt.now().__str__()}] INFO: DataReader {name} INITIALISING WITH PORT NAME"
            f" {port_name}\n"
        )
        sys.stderr.write(err_string)
        self.name = name
        self.port_name = port_name
        self.queue = shared_queue

        try:
            info_string = (
                f"[{dt.now().__str__()}] INFO: DataReader {self.name} CHECKING PORT "
                f"{self.port_name} AVAILABILITY\n"
            )
            sys.stderr.write(info_string)
            self.check_port_available()
        except serial.serialutil.SerialException:
            # TODO: HANDLE PORT UNAVAILABLE
            # What needs to be done with this exception? Terminate thread?
            # Reraise to let control.py handle it?
            # Seems like a fatal error, unless want to keep retrying
            err_string = (
                f"[{dt.now().__str__()}] ERROR: DataReader {self.name} THINKS PORT "
                f"{self.port_name} IS UNAVAILABLE\n"
            )
            sys.stderr.write(err_string)

        try:
            info_string = (
                f"[{dt.now().__str__()}] INFO: DataReader {self.name} CHECKING PORT "
                f"{self.port_name} FUNCTIONALITY\n"
            )
            sys.stderr.write(info_string)
            # I don't see what use this check is doing. It asserts that the
            # port can be opened, but any errors when opening the port are also
            # caught below in the next try/catch block
            self.check_port_function()
        except serial.serialutil.SerialException:
            # TODO: HANDLE INCORRECT PORT FUNCTION
            # Ditto about how to handle this
            err_string = (
                f"[{dt.now().__str__()}] ERROR: DataReader {self.name} THINKS PORT "
                f"{self.port_name} IS MALFUNCTIONING\n"
            )
            sys.stderr.write(err_string)

        try:
            info_string = (
                f"[{dt.now().__str__()}] INFO: DataReader {self.name} OPENING PORT "
                f"{self.port_name} FOR READ\n"
            )
            sys.stderr.write(info_string)
            self.port = serial.Serial(self.port_name, 9600, timeout=1)
            self.port.reset_input_buffer()
        except serial.serialutil.SerialException:
            # TODO: HANDLE PORT NOT OPENABLE EXCEPTION
            # ditto
            err_string = (
                f"[{dt.now().__str__()}] ERROR: DataReader {self.name} CAN'T OPEN "
                f"{self.port_name} FOR READ\n"
            )
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
            raise serial.serialutil.SerialException from exception

    def check_port_function(self):
        """
        Check whether or not data can be read from the serial port, and whether
        or not any data that can be read seems sensible.
        """
        try:
            port = serial.Serial(self.port_name, 9600, timeout=1)
            port.close()
        except serial.serialutil.SerialException as exception:
            raise serial.serialutil.SerialException from exception

    def read_data_line(self):
        """
        Read and return a line of attached instrument data.
        """
        # Should this be debugging level? then can set minimum level as INFO in
        # production so don't spam log files
        info_string = (
            f"[{dt.now().__str__()}] INFO: DataReader {self.name} READING DATA FROM "
            f"{self.port_name}\n"
        )
        sys.stderr.write(info_string)
        # No exceptions to catch here?
        # Looks like this will timeout after 1s (specified when Serial objected
        # created). What happens at that point? Will it just return whatever is
        # in the buffer, even if no newline character has been reached?
        data = self.port.readline()
        return data

    def enqueue_data(self, data):
        """
        Put an incoming line of data into a shared queue, ready for a DataWriter
        to process.
        """
        # again, this is more debugging logging and imo doesn't need to be in
        # production
        info_string = (
            f"[{dt.now().__str__()}] INFO: DataReader {self.name} ENQUEUEING DATA TO "
            "SHARED QUEUE\n"
        )
        sys.stderr.write(info_string)
        # This should come after the line has been added and again imo can be
        # removed in production
        sys.stderr.write(
            f"[{dt.now().__str__()}] INFO: QUEUE IS NOW SIZE {self.queue.qsize()}\n"
        )
        # What is this magic number 5 relating to? Looks to me
        # like it's stripping /dev/ away to leave SENSOR_ARRAY_X,
        # but this can just be obtained as self.name
        self.queue.put(f"{self.port_name[5:]},{data.decode()}", block=True)

    def run(self):
        """
        Main entry point for DataReader threads.
        """
        while True:
            try:
                self.enqueue_data(self.read_data_line())
            # Is this the only exception from read_data_line?
            # What about if line doesn't have X number of commas? Seen this
            # issue several times in the raw data.
            # See also earlier comment about timeout, does that raise an
            # exception or just return whatever is in the buffer?
            except UnicodeDecodeError:
                err_string = (
                    f"[{dt.now().__str__()}] INFO: DataReader {self.name} CAUGHT SOME "
                    "GARBAGE; IGNORING DATA LINE\n"
                )
                sys.stderr.write(err_string)
                continue
