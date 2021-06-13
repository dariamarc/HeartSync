from datetime import datetime


class CommentService:
    def __init__(self, comment_repo):
        self.comment_repo = comment_repo

    def save_comment(self, scanid, username, text):
        """
        Save comment in database
        :param scanid: id of scan
        :param username: username
        :param text: comment text
        :return: inserted comment
        """
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y")
        comment_id = self.comment_repo.insert_comment(scanid, username, text, dt_string)
        comment = self.comment_repo.get_comment_by_id(comment_id)

        return comment.get_data()

    def get_comments_by_scan(self, scanid):
        """
        Get comments by scan id
        :param scanid: id of scan
        :return: list of comments
        """
        return self.comment_repo.get_comments_by_scan(scanid)