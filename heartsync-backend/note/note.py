
class Note:
    def __init__(self, id, scanid, text):
        self.id = id
        self.scanid = scanid
        self.text = text

    def get_data(self):
        """
        Return note data in dictionary format
        :return:
        """
        return {
            'id': self.id,
            'scanid': self.scanid,
            'text': self.text
        }