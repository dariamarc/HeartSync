
class Comment:
    def __init__(self, id, scanid, username, text, date):
        self.id = id
        self.scanid = scanid
        self.username = username
        self.text = text
        self.date = date

    def get_data(self):
        """
        Return comment data in dictionary format
        :return:
        """
        data = {
            'id': self.id,
            'scanid': self.scanid,
            'username': self.username,
            'text': self.text,
            'date': self.date
        }
        return data