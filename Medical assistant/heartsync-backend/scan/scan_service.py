
class ScanService:
    def __init__(self, scan_repo):
        self.scan_repo = scan_repo

    def add_scan(self, username, fileid, name):
        scan_id = self.scan_repo.add_scan(username, fileid, name)
        scan = self.scan_repo.get_scan(scan_id)
        return scan.get_scan()

    def get_user_scans(self, username):
        return self.scan_repo.get_user_scans(username)