class transactionManagementException(Exception):
    def __init__(self, message):
        self.Message = message
        super().__init__(self.Message)

    @property
    def message(self):
        return self.Message

    @message.setter
    def message(self, value):
        self.Message = value
