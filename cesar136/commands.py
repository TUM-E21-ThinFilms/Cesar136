from CeasarCommunication import MessagePacket


class commands():
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


turnOutputOff = commands(1, 0, 1)

reportPowerSupplyType = commands(128, 0, 5, [[5], [2]])
reportModelNumber = commands(129, 0, 5, [[5], [0]])
reportRFRampOnOff = commands(151, 0, 4, [[2, 4], [0, 0]])

reportReflectedPowerParameters = commands(152, 0, 3, [[1, 3], [0, 0]])
reportRegulationMode = commands(154, 0, 1, [[1], [1]])
reportActiveControlMode = commands(155, 0, 1, [[1], [1]])
