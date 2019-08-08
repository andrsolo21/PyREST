class MyError():

    def __init__(self, text = "", num = 400):
        self.numError = num
        self.textError = text

    def isError(self):
        return True

