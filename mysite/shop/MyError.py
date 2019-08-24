class MyError():

    """Class have text and number of http error"""

    def __init__(self, text = "", num = 400):

        """
        :param text: text error
        :param num: number of http error
        """

        self.numError = num
        self.textError = text

    def isError(self):

        """
        It is return true
        :return: TRUE
        """

        return True

    def as_json(self):

        """"
        :return: dictionary, where key - error, value - text of error
        """

        return dict(
            error = self.textError
        )

