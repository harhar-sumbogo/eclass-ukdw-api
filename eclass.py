import requests as req
from bs4 import BeautifulSoup as bs
import re


class Eclass:
    base_url = "https://eclass.ukdw.ac.id/"
    session = req.Session()

    def __init__(self, nim: str, password: str):
        self.nim = nim
        self.password = password

    def login(self, nim: str = None, password: str = None):
        login_url = self.base_url + "id/home/do_login"
        login = self.session.post(login_url, data={
            "id": self.nim, "password": self.password})

        soup = bs(login.text, 'html.parser')
        error = soup.find("div", {"id": "error"})
        if error:
            raise Exception(error.text)

    def get_daftar_pengumuman(self):
        home = self.session.get(self.base_url)
        with open("coba.html", "wb") as f:
            f.write(home.content)

        soup = bs(home.text, "html.parser")
        list_pengumuman = soup.find_all("a", {"class": "menu mc"})
        transformed_pengumuman = []

        for pengumuman in list_pengumuman:
            href = pengumuman["href"]
            content = pengumuman.stripped_strings
            tanggal = next(content)
            next(content)
            judul = next(content)

            result = {
                "id": re.search("\d+", href).group(),
                "matkul": pengumuman["title"],
                "tanggal": tanggal,
                "judul": judul[1:],
                "detail_url": href}
            transformed_pengumuman.append(result)
        return transformed_pengumuman

    def get_detail_pengumuman(self, url_pengumuman):
        href = url_pengumuman
        id = re.search("\d+", href).group()
        pengumuman_full = self.session.get(href)
