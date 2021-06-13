import json

from sqlalchemy import Table, select, delete

from comment.comment import Comment


class CommentRepo:
    def __init__(self, con, metadata, engine, app):
        self.con = con
        self.app = app
        self.comments = Table('comments', metadata, autoload=True, autoload_with=engine)

    def insert_comment(self, scanid, username, text, date):
        """
        Insert comment in database
        :param scanid: id of scan
        :param username: username
        :param text: comment text
        :param date: date of the comment
        :return: inserted primary key of comment
        """
        ins = self.comments.insert().values(scanid=scanid, text=text, username=username, date=date)
        result = self.con.execute(ins)

        return result.inserted_primary_key

    def get_comment_by_id(self, id):
        """
        Get comment by id
        :param id: id of comment
        :return: comment with primary key id
        """
        query = select([self.comments]).where(self.comments.c.id == id[0])
        comment = None
        for row in self.con.execute(query):
            comment = Comment(row[0], row[1], row[2], row[3], row[4])

        return comment

    def get_comments_by_scan(self, scanid):
        """
        Get comments by scan id
        :param scanid: id of the scan
        :return: list of comments
        """
        query = select([self.comments]).where(self.comments.c.scanid == scanid)
        result_proxy = self.con.execute(query)
        result_set = result_proxy.fetchall()
        comments = []
        for i, row in enumerate(result_set):
            comment = Comment(row[0], row[1], row[2], row[3], row[4])
            comments.append(comment.get_data())
        return json.dumps(comments)

    def delete_comment(self, id):
        """
        Deletes comment with id
        :param id: id of comment
        :return:
        """
        deldb = delete(self.comments).where(self.comments.c.id == id)
        self.con.execute(deldb)
