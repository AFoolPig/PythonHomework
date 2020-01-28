import ftplib
import os
import re

ftp_client = ftplib.FTP_TLS('domain', 'username', 'password')
remote_dir = '/WholeFS/Documents/steel-edge/temp12'
ftp_client.cwd(remote_dir)
print(ftp_client.pwd())

space_split = re.compile('[ ]+')


class FileInfo(object):
    def __init__(self, remote_dir, file_info):
        super(FileInfo, self).__init__()
        (self.permission, _, self.user, self.group, self.size,
         self.month, self.day, self.time, self.name) = space_split.split(file_info, 8)
        self.size = int(self.size)
        self.remote_dir = remote_dir

    def __str__(self) -> str:
        return '{permission:"%s",name:"%s",size:"%s"}' % (self.permission, self.name, self.size)


file_infos = []


def record_files(file_info):
    file_info = FileInfo(remote_dir, file_info)
    if not file_info.name.startswith('.'):
        file_infos.append(file_info)


ftp_client.retrlines('LIST', record_files)

file_infos.sort(key=lambda info: info.name)

# print(ftp_client.nlst('/WholeFS/Documents/steel-edge/temp1'))

remote_file_path = os.path.join(remote_dir, file_infos[0].name)
local_file_path = '/home/ds05/Documents/temp/file.tiff'


class FileWriter(object):
    def __init__(self, local_dir, file_info):
        super(FileWriter, self).__init__()
        self.local_dir = local_dir
        self.file_info = file_info
        self.open_file = None
        self.written_length = None
        self.writing_callback = None

    def set_writing_callback(self, callback):
        self.writing_callback = callback

    def write(self, data):
        self.written_length += len(data)
        if self.writing_callback:
            self.writing_callback(self.file_info, self.written_length)
        self.open_file.write(data)

    def open(self):
        self.open_file = open(os.path.join(self.local_dir, self.file_info.name), 'wb')
        self.written_length = 0

    def close(self):
        self.open_file.close()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        return True

    def __enter__(self):
        self.open()
        return self


def writing_callback(file_info, written_length):
    print('(%d/%d) %03d%% %s' % (written_length, file_info.size,
                                 int(100 * written_length / file_info.size), file_info.name))


with FileWriter('/home/ds05/Documents/temp', file_infos[0]) as f:
    buf_size = 1024
    f.set_writing_callback(writing_callback)
    ftp_client.retrbinary('RETR %s' % remote_file_path, f.write, buf_size)

pass
