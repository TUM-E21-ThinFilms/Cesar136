from CeasarCommunication import MessagePacket


class Command():
    def __init__(self, commandNumber, DataBytesTosend, DatabytesExpected, DataConfig=None):
        self.commandNumber = commandNumber
        self.DataBytesToSend = DataBytesTosend
        self.DataBytesExpected = DatabytesExpected
        if self.commandNumber < 128:
            self.CSRonly = True
        else:
            self.CSRonly = False
            self.DataConfig = DataConfig

    def set_data(self, data):
        self.data = data

    def prepareInteraction(self):
        if self.DataBytesToSend != 0:
            self.intBinArray = MessagePacket().createMessagePacket(self.commandNumber, self.data)
        else:
            self.intBinArray = MessagePacket().createMessagePacket(self.commandNumber)


turnOutputOff = Command(1, 0, 1)

reportPowerSupplyType = Command(128, 0, 5, [[5], [2]])
reportModelNumber = Command(129, 0, 5, [[5], [0]])
reportRFRampOnOff = Command(151, 0, 4, [[2, 4], [0, 0]])

reportReflectedPowerParameters = Command(152, 0, 3, [[1, 3], [0, 0]])
reportRegulationMode = Command(154, 0, 1, [[1], [1]])
reportActiveControlMode = Command(155, 0, 1, [[1], [1]])
