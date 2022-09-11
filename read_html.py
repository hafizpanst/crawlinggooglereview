from datetime import datetime
import pandas as pd
from bs4 import BeautifulSoup


constant = {
    "rating" : {
        "tag" : "span",
        "loc" : "Fam1ne EBe2gf",
    },
    "nama_reviewer" : {
        "tag" : "div",
        "loc" : "TSUbDb",
    },
    "review" : {
        # "tag" : "span",
        # "loc" : "review-full-text",
        "tag" : "div",
        "loc" : "Jtu6Td",
    },
    "whole_review" : {
        "tag" : "div",
        "loc" : "WMbnJf vY6njf gws-localreviews__google-review",
    },
    "waktu_review" : {
        "tag" : "div",
        "loc" : "PuaHbe",
    }
}

def data_review(nama_kpp):
    df = pd.read_csv("result/{}_html.csv".format(nama_kpp))
    result = BeautifulSoup(df.iloc[0]["html"], "html.parser")
    return result

def find_review(nama_kpp, html):
    result = []
    f = html.find_all(constant["whole_review"]["tag"], {"class" : constant["whole_review"]["loc"]})
    for i in range(len(f)):
        z = {
            "nama_kpp" : nama_kpp,
            "nama_reviewer" : None,
            "rating" : None,
            "review" : None,
            "waktu_review" : None,
            "tanggal_olah" : datetime.today(),
        }

        nama_reviewer = f[i].find_all(constant["nama_reviewer"]["tag"], {"class" : constant["nama_reviewer"]["loc"]})
        z["nama_reviewer"] = nama_reviewer[0].text

        rating = f[i].find_all(constant["rating"]["tag"], {"class" : constant["rating"]["loc"]})
        z["rating"] = rating[0]["aria-label"]
        z["waktu_review"] = f[i].find_all(constant["waktu_review"]["tag"], {"class" : constant["waktu_review"]["loc"]})[0].text

        try:
            review = f[i].find_all(constant["review"]["tag"], {"class" : constant["review"]["loc"]})
            z["review"] = review[0].text

        except Exception as e:
            None

        result += [z]
    return result

def saving_review(filename, df):
    df = pd.DataFrame(df)
    df.to_csv("result/{}_review.csv".format(filename), index = False)

def main():

    kpp_list = ['KPP Pratama Jakarta Tebet','KPP Pratama Jakarta Tanjung Priok','KPP Pratama Jakarta Tanah Abang Tiga','KPP Pratama Jakarta Tanah Abang Satu','KPP Pratama Jakarta Tanah Abang Dua','KPP Pratama Jakarta Tambora','KPP Pratama Jakarta Tamansari','KPP Pratama Jakarta Sunter','KPP Pratama Jakarta Setiabudi Tiga','KPP Pratama Jakarta Setiabudi Satu','KPP Pratama Jakarta Setiabudi Empat','KPP Pratama Jakarta Setiabudi Dua','KPP Pratama Jakarta Senen','KPP Pratama Jakarta Sawah Besar Satu','KPP Pratama Jakarta Sawah Besar Dua','KPP Pratama Jakarta Pulogadung','KPP Pratama Jakarta Pluit','KPP Pratama Jakarta Pesanggrahan','KPP Pratama Jakarta Penjaringan','KPP Pratama Jakarta Pasar Rebo','KPP Pratama Jakarta Pasar Minggu','KPP Pratama Jakarta Pancoran','KPP Pratama Jakarta Palmerah','KPP Pratama Jakarta Pademangan','KPP Pratama Jakarta Menteng Tiga','KPP Pratama Jakarta Menteng Satu','KPP Pratama Jakarta Menteng Dua','KPP Pratama Jakarta Matraman','KPP Pratama Jakarta Mampang Prapatan','KPP Pratama Jakarta Kramat Jati','KPP Pratama Jakarta Koja','KPP Pratama Jakarta Kembangan','KPP Pratama Jakarta Kemayoran','KPP Pratama Jakarta Kelapa Gading','KPP Pratama Jakarta Kebon Jeruk Satu','KPP Pratama Jakarta Kebon Jeruk Dua','KPP Pratama Jakarta Kebayoran Lama','KPP Pratama Jakarta Kebayoran Baru Tiga','KPP Pratama Jakarta Kebayoran Baru Satu','KPP Pratama Jakarta Kebayoran Baru Empat','KPP Pratama Jakarta Kebayoran Baru Dua','KPP Pratama Jakarta Kalideres','KPP Pratama Jakarta Jatinegara','KPP Pratama Jakarta Jagakarsa','KPP Pratama Jakarta Grogol Petamburan','KPP Pratama Jakarta Gambir Tiga','KPP Pratama Jakarta Gambir Satu','KPP Pratama Jakarta Gambir Empat','KPP Pratama Jakarta Gambir Dua','KPP Pratama Jakarta Duren Sawit','KPP Pratama Jakarta Cilandak','KPP Pratama Jakarta Cengkareng','KPP Pratama Jakarta Cempaka Putih','KPP Pratama Jakarta Cakung','KPP Madya Jakarta Utara','KPP Madya Jakarta Timur','KPP Madya Jakarta Selatan II','KPP Madya Jakarta Selatan I','KPP Madya Jakarta Pusat','KPP Madya Jakarta Barat','KPP Madya Dua Jakarta Utara','KPP Madya Dua Jakarta Timur','KPP Madya Dua Jakarta Selatan II','KPP Madya Dua Jakarta Selatan I','KPP Madya Dua Jakarta Pusat','KPP Madya Dua Jakarta Barat']

    # kpp_list = ["KPP Pratama Jakarta Tebet", "KPP Pratama Jakarta Tanjung Priok"]

    d_list = []
    for kpp in kpp_list:
        try:
            d_list += [{
                "nama_kpp" : kpp,
                "html" : data_review(nama_kpp=kpp),
            }]
        except:
            continue

    review = []
    for kpp in d_list:
        try:
            review += find_review(kpp["nama_kpp"], kpp["html"])

        except Exception as e:
            print(e)
            continue

    saving_review("review", review)


if __name__ == "__main__":
    main()