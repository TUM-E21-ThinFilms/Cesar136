from cesar import get_transport
from CeasarCommunication import *
from command import *

ser = get_transport()
CSRCodes = {0: "Command accepted",
            1: "Control code is incorrect",
            2: "Output is on (change not allowed)",
            4: "Data is out of range",
            7: "Active fault(s) exist",
            9: "Data byte count is incorrect",
            19: "Recipe is active (change not allowed)",
            50: "The frequency is out of range",
            51: "The duty cycle is out of range",
            53: "The device controlled by the command is not detected",
            99: "Command not accepted (there is no such command)"}


def interactionProcess(Command):
    Command.prepareInteraction()
    ser.write(bytearray(Command._intArray))
    response = ReceivedByteArray(bytearray(ser.read(10))[1::])
    if response.checkForCompletness() != 0:
        raise RuntimeError("Computer received no valid response, try again.")
    else:
        if Command.CSRonly:
            if response._lenData == 1:
                answer = CSRCodes[response._data]
            else:
                raise ValueError("Something must be wrong, CSR contained more data")
        else:
            response.extractData(Command.DataConfig)
            answer = response.formatedData
    return answer


def Output_Off():
    print(interactionProcess(turnOutputOff))


def getModelNumber():
    print(interactionProcess(reportModelNumber))


def getPowerSupplyType():
    print(interactionProcess(reportPowerSupplyType))


def getRFRampOnOff():
    print(interactionProcess(reportRFRampOnOff))
