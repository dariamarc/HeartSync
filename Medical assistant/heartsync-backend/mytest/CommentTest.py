import unittest


class CommentTest:
    def __init__(self, comment_repo, comment_service):
        self.comment_repo = comment_repo
        self.comment_service = comment_service

    def comment_repo_test(self):
        scanid = 13
        username = 'dariamarc'
        text = 'mytest'
        date = '13/05/1999'
        id = self.comment_repo.insert_comment(scanid, username, text, date)
        assert(self.comment_repo.get_comment_by_id(id[0]) is not None)
        assert(self.comment_repo.get_comments_by_scan(scanid) != "")
        self.comment_repo.delete_comment(id)

    def comment_service_test(self):
        scanid = 13
        username = 'dariamarc'
        text = 'mytest'
        date = '13/05/1999'
        comment = self.comment_service.save_comment(scanid, username, text)
        assert(comment['scanid'] == 13)
        assert(comment['username'] == 'dariamarc')
        assert(comment['text'] == 'mytest')
        assert(self.comment_service.get_comments_by_scan(scanid) != "")
        self.comment_repo.delete_comment(comment['id'])
