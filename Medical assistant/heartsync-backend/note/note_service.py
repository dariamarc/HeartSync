
class NoteService:
    def __init__(self, note_repo):
        self.note_repo = note_repo

    def save_note(self, scan_id, text):
        """
        Save or update note in database
        :param scan_id: id of scan
        :param text: note text
        :return:
        """
        if self.note_repo.get_note_by_scan(scan_id) is None:
            note_id = self.note_repo.insert_note(scan_id, text)
            note = self.note_repo.get_note_by_id(note_id[0])
        else:
            self.note_repo.update_note(scan_id, text)
            note = self.note_repo.get_note_by_scan(scan_id)

        return note.get_data()

    def get_note_by_scan(self, scan_id):
        """
        Get note by scan id
        :param scan_id: id of scan
        :return:
        """
        note = self.note_repo.get_note_by_scan(scan_id)
        if note != None:
            return note.get_data()
        return ''
