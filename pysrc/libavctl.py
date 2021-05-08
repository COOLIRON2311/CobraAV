from hashlib import md5, new
from os import remove, rename, stat, system
from os.path import isfile, getsize
from typing import Generator

# Configuration constants
WHITELIST_PATH = r'/opt/cobraav/signatures/whitelist.fp'  # whitelisted signatures database path
BLACKLIST_PATH = r'/opt/cobraav/signatures/blacklist.hdb'  # custom blacklisted signatures db path

class DataBase:
    __BUF_SIZE = 65536  # Hashing buffer size, default: 64kb

    @staticmethod
    def __hash(path: str, alg: new = md5) -> str:
        """efficiently calculates file hash"""
        h = alg()
        with open(path, 'rb') as f:
            while True:
                data = f.read(DataBase.__BUF_SIZE)
                if not data:
                    break
                h.update(data)
        return h.hexdigest()

    @staticmethod
    def __signature(path: str) -> str:
        """generates valid libclamav signature"""
        if isfile(path):
            return '{}:{}:CustomSignature\n' \
                    .format(DataBase.__hash(path), stat(path).st_size)
        else:
            raise FileNotFoundError("file does not exist")

    @staticmethod
    def __remove_signature(sig: str, db: str) -> None:
        """removes signature from database"""
        try:
            with open(db, 'r') as r, open(db+'_temp', 'w') as w:
                t = r.readline()
                while t != '':
                    if t != sig:
                        w.write(t)
                    t = r.readline()
            remove(db)
            if getsize(db+'_temp') == 0:
                remove(db+'_temp')
            else:
                rename(db+'_temp', db)
        except FileNotFoundError:
            pass

    @staticmethod
    def whitelist(path: str) -> None:
        """adds file signature to whitelist"""
        if isfile(path):
            sig = DataBase.__signature(path)
        else:
            raise FileNotFoundError("file does not exist")
        with open(WHITELIST_PATH, 'a') as f:
            f.write(sig)
        DataBase.__remove_signature(sig, BLACKLIST_PATH)

    @staticmethod
    def blacklist(path: str) -> None:
        """adds file signature to blacklist"""
        if isfile(path):
            sig = DataBase.__signature(path)
        else:
            raise FileNotFoundError("file does not exist")
        with open(BLACKLIST_PATH, 'a') as f:
            f.write(sig)
        DataBase.__remove_signature(sig, WHITELIST_PATH)

    @staticmethod
    def get_db_iterator(db: str) -> 'Generator[str]':
        """returns contents of the database"""
        if isfile(db):
            with open(db) as f:
                t = f.readline()
                while t:
                    yield t[:-1]
                    t = f.readline()
        else:
            raise FileNotFoundError("file does not exist")

    @staticmethod
    def find(path: str, db: str) -> str:
        """returns file signature if the database contains it"""
        if isfile(path):
            sig = DataBase.__signature(path)[:-1]
        else:
            raise FileNotFoundError("file does not exist")
        for i in DataBase.get_db_iterator(db):
            if i == sig:
                return sig
        return ''


def enqueue_scan(path: str, fifo_path: str = '/tmp/cobra.sock') -> None:
    if isfile(path):
        with open(fifo_path, 'w') as pipe:
            pipe.write(path)
    else:
        raise FileNotFoundError("file does not exist")


def send_reload() -> None:
    system('systemctl restart cobra-sentinel.service')

