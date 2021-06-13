from sqlalchemy import Table, delete
from sqlalchemy import select, update

from note.note import Note


class NoteRepo():
    def __init__(self, con, metadata, engine, app):
        self.con = con
        self.app = app
        self.notes = Table('notes', metadata, autoload=True, autoload_with=engine)

    def insert_note(self, scan_id, text):
        """
        Insert note to database
        :param scan_id: id of scan
        :param text: note text
        :return: primary key of inserted note
        """
        ins = self.notes.insert().values(scanid=scan_id, text=text)
        result = self.con.execute(ins)

        return result.inserted_primary_key

    def update_note(self, scan_id, text):
        """
        Update note data in database
        :param scan_id:
        :param text:
        :return:
        """
        upd = update(self.notes).where(self.notes.c.scanid == scan_id).values(text=text)
        result = self.con.execute(upd)
        if result:
            return True
        return False

    def get_note_by_scan(self, scanid):
        """
        Get note by scan id
        :param scanid: id of scan
        :return:
        """
        query = select([self.notes]).where(self.notes.c.scanid == scanid)
        note = None
        for row in self.con.execute(query):
            note = Note(row[0], row[1], row[2])

        return note

    def get_note_by_id(self, id):
        """
        Get note by id
        :param id: id of note
        :return:
        """
        query = select([self.notes]).where(self.notes.c.id == id)
        note = None
        for row in self.con.execute(query):
            note = Note(row[0], row[1], row[2])

        return note

    def delete_note(self, id):
        """
        Deletes note with id
        :param id: id of note
        :return:
        """
        deldb = delete(self.notes).where(self.notes.c.id == id)
        self.con.execute(deldb)
