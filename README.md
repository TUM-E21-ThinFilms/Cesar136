# Cesar136
Python implementation of the serial interface for the Cesar 136 RF Power Supply


# Installation
Using the python installer
```bash
python setup.py install
```

# Usage
Setting up the code is straight-forward 
```python
import logging
from e21_util.serial_connection import Serial
from cesar136.factory import Factory

# See the pyserial documentation for initialization
transport = Serial('/dev/ttyUSB0', 19200, 'O', 1, 0.1)
driver = Factory.create(transport, logging.get_logger())
```
## Sending commands
All driver commands return a Response object which contains all information from the device. 
Every response has a CSR (Command Status Response) Code, but which might be empty (or not set).   
```python    
from cesar136.constants import Parameter

response = driver.turn_on()

if response.is_csr():
    if response.get_csr().get() == Parameter.CSRCode.ACCEPTED:
        # worked
    else:
        # did not work
```
If a device returns some additional data, then access it via `get_parameter`:
```python   
response = driver.get_reflected_power_parameters()

timelimit = response.get_parameter(Parameter.ReflectedPowerParameter.TimeLimit).get()
trigger = response.get_parameter(Parameter.ReflectedPowerParameter.PowerTrigger).get()
```
If the device returns just a single parameter, then simply access it via `get_parameter` without specifiying the desired parameter.
```python 
response = driver.get_regulation_mode()

control_mode = response.get_parameter().get()
```    
Furthermore, the device can return bit-flags and they can be accessed using `get_bit`
```python 
response = driver.get_status()

interlock_set = response.get_parameter().get_bit(Parameter.Status.BIT_INTERLOCK)
```


## Example
A standard example is setting the output on with predefined powers. This works as follows
```python
# We want to regulate the forward power
driver.set_regulation_mode(Parameter.Regulation.FORWARD_POWER)

# Do not reflect more than 30W
driver.set_reflected_power_limit(30)

# Put 60 W onto the output
driver.set_setpoint(60)

# Set OnTime to 3 seconds
driver.set_time_limit(3)

# Turn it on for ~20 seconds
for i in range(0, 20):
    driver.turn_on()
    time.sleep(1)
    
# When done, turn it off
driver.turn_off()
```
Note that after three seconds (time_limit), the device will turn off automatically, since we set the time_limit to three seconds.
Usually, one re-sends the `turn_on` command every second and when done, turn it of using `turn_off`.
In general, it a good practice to use a low value for the time_limit and re-send the `turn_on` command as often as possible. 
This is a good security approach, if the controlling device has problems or the serial connection gets lost.  

     
      
