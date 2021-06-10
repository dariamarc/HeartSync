
class ScanService:
    def __init__(self, scan_repo):
        self.scan_repo = scan_repo

    def add_scan(self, username, fileid, name):
        scan_id = self.scan_repo.add_scan(username, fileid, name)
        return scan_id[0]

    def get_user_scans(self, username):
        return self.scan_repo.get_user_scans(username)