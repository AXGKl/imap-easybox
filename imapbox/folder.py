from collections import UserList
from typing import TYPE_CHECKING
from .email import Mail

if TYPE_CHECKING:
    from .client import ImapServer


class FoldList(UserList):
    def __getitem__(self, item):
        val = super().__getitem__(item)
        if isinstance(val, Folder):
            val.server.select(val.folder_name)
        return val


class Folder:
    def __init__(self, folder_name: str, box: 'ImapServer'):
        self.box = box
        self.server = box.server
        self.folder_name = folder_name

    @property
    def mail_counts(self):
        mails = self.search(None, 'ALL')
        return len(mails) if mails else 0

    @property
    def mails(self):
        return self.search(None, 'ALL')

    def search(self, *args):
        typ, data = self.server.search(None, *args)
        mail_ids = data[0].decode('utf8').split(' ')
        if mail_ids == ['']:
            return []
        return [Mail(i, self) for i in mail_ids]

    def rename(self, folder_name):
        """更改文件夹名称"""
        self.box.rename_folder(self.folder_name, folder_name)

    def delete(self):
        """修改文件夹名称"""
        self.box.delete_folder(self.folder_name)

    def __repr__(self):
        return f"Folder<{self.folder_name}>"
