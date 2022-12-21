import requests as req
from bs4 import BeautifulSoup as bs
import re


class Eclass:
    base_url = "https://eclass.ukdw.ac.id/"

    def __init__(self, nim: str, password: str):
        self.nim = nim
        self.password = password

    def login(self) -> req.Session:
        session = req.Session()
        login_url = self.base_url + "id/home/do_login"
        login = session.post(login_url, data={
            "id": self.nim, "password": self.password})

        soup = bs(login.text, 'html.parser')
        error = soup.find("div", {"id": "error"})
        if error:
            raise Exception(error.text)

        return session

    def get_daftar_pengumuman(self) -> dict:
        with self.login() as session:
            home = session.get(self.base_url)
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

    def get_detail_pengumuman(self, id) -> dict:
        href = f"https://eclass.ukdw.ac.id/e-class/id/pengumuman/baca/{id}"
        with self.login() as session:
            pengumuman_full = session.get(href)
            soup = bs(pengumuman_full.text, "html.parser")

            pengumuman = soup.find("div", {"id": "content-right"})

            # mengambil judul dan tanggal pengumuman dari header
            header = pengumuman.find("tr", {"class": "thread"}).td
            header = header.stripped_strings
            judul = next(header)
            tanggal = next(header)

            # mendapatkan isi konten dari pengumuman
            isi = pengumuman.find("tr", {"class": "isithread"}).td
            isi = isi.stripped_strings
            result_isi = [re.sub("\s+", " ", content) for content in isi]
            matkul = result_isi[1]
            dosen = result_isi[-1]
            isi_pengumuman = "\n".join(result_isi[2:-1])

            return {
                "id": id,
                "matkul": matkul,
                "dosen": dosen,
                "judul": judul,
                "tanggal": tanggal,
                "isi_pengumuman": isi_pengumuman
            }