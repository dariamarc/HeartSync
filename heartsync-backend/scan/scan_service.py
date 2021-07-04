
class ScanService:
    def __init__(self, scan_repo):
        self.scan_repo = scan_repo

    def save_scan(self, username, fileid, name):
        """
        Save scan
        :param username: username
        :param fileid: id of file
        :param name: name of scan
        :return:
        """
        scan_id = self.scan_repo.insert_scan(username, fileid, name)
        scan = self.scan_repo.get_scan(scan_id[0])
        return scan.get_data()

    def get_user_scans(self, username):
        """
        Get list of scans by username
        :param username: username
        :return:
        """
        return self.scan_repo.get_user_scans(username)

    def get_scan_file(self, scan_id):
        """
        Get file id of scan
        :param scan_id: id of scan
        :return:
        """
        scan = self.scan_repo.get_scan(scan_id)
        return scan.fileid

    def get_scan_by_id(self, scan_id):
        """
        Get scan by id
        :param scan_id: id of scan
        :return:
        """
        scan = self.scan_repo.get_scan(scan_id)
        if scan is not None:
            return scan.get_data()
        return None
