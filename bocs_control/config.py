"""
Contains package level constants.

Misc variables:

    ERROR_LOG_FN (str)
    DATA_LOG_DIR (str)
    INSTRUMENTS (list[str])
    HEADER (list[str])
"""
ERROR_LOG_FN = "/home/pi/bocs/error.log"
DATA_LOG_DIR = "/home/pi/bocs/data"
INSTRUMENTS = ["BOCS_SENSOR_ARRAY"]
HEADER = [
    "timestamp,voc_voltage,voc_current,voc_power,heater_voltage,heater_current,heater_power,voc_1,voc_2,voc_3,voc_4,voc_5,voc_6,voc_7,voc_8,no_voltage,no_current,no_power,no_1_working,no_1_aux,no_2_working,no_2_aux,no_3_working,no_3_aux,co_voltage,co_current,co_power,co_1_working,co_1_aux,co_2_working,co_2_aux,co_3_working,co_3_aux,ox_voltage,ox_current,ox_power,ox_1_working,ox_1_aux,ox_2_working,ox_2_aux,ox_3_working,ox_3_aux,no2_voltage,no2_current,no2_power,no2_1_working,no2_1_aux,no2_2_working,no2_2_aux,no2_3_working,no2_3_aux,co2_voltage,co2_current,co2_power,co2_1_measurement,co2_1_reference,co2_2_measurement,co2_2_reference,co2_3_measurement,co2_3_reference,pump_voltage,pump_current,pump_power,pressure,flow_rate,relative_humidity,temperature\n"
]
BAUD_RATE = 9600
