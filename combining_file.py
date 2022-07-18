import os
import pandas as pd


kpp_list = ['KPP Pratama Jakarta Tebet','KPP Pratama Jakarta Tanjung Priok','KPP Pratama Jakarta Tanah Abang Tiga','KPP Pratama Jakarta Tanah Abang Satu','KPP Pratama Jakarta Tanah Abang Dua','KPP Pratama Jakarta Tambora','KPP Pratama Jakarta Tamansari','KPP Pratama Jakarta Sunter','KPP Pratama Jakarta Setiabudi Tiga','KPP Pratama Jakarta Setiabudi Satu','KPP Pratama Jakarta Setiabudi Empat','KPP Pratama Jakarta Setiabudi Dua','KPP Pratama Jakarta Senen','KPP Pratama Jakarta Sawah Besar Satu','KPP Pratama Jakarta Sawah Besar Dua','KPP Pratama Jakarta Pulogadung','KPP Pratama Jakarta Pluit','KPP Pratama Jakarta Pesanggrahan','KPP Pratama Jakarta Penjaringan','KPP Pratama Jakarta Pasar Rebo','KPP Pratama Jakarta Pasar Minggu','KPP Pratama Jakarta Pancoran','KPP Pratama Jakarta Palmerah','KPP Pratama Jakarta Pademangan','KPP Pratama Jakarta Menteng Tiga','KPP Pratama Jakarta Menteng Satu','KPP Pratama Jakarta Menteng Dua','KPP Pratama Jakarta Matraman','KPP Pratama Jakarta Mampang Prapatan','KPP Pratama Jakarta Kramat Jati','KPP Pratama Jakarta Koja','KPP Pratama Jakarta Kembangan','KPP Pratama Jakarta Kemayoran','KPP Pratama Jakarta Kelapa Gading','KPP Pratama Jakarta Kebon Jeruk Satu','KPP Pratama Jakarta Kebon Jeruk Dua','KPP Pratama Jakarta Kebayoran Lama','KPP Pratama Jakarta Kebayoran Baru Tiga','KPP Pratama Jakarta Kebayoran Baru Satu','KPP Pratama Jakarta Kebayoran Baru Empat','KPP Pratama Jakarta Kebayoran Baru Dua','KPP Pratama Jakarta Kalideres','KPP Pratama Jakarta Jatinegara','KPP Pratama Jakarta Jagakarsa','KPP Pratama Jakarta Grogol Petamburan','KPP Pratama Jakarta Gambir Tiga','KPP Pratama Jakarta Gambir Satu','KPP Pratama Jakarta Gambir Empat','KPP Pratama Jakarta Gambir Dua','KPP Pratama Jakarta Duren Sawit','KPP Pratama Jakarta Cilandak','KPP Pratama Jakarta Cengkareng','KPP Pratama Jakarta Cempaka Putih','KPP Pratama Jakarta Cakung','KPP Madya Jakarta Utara','KPP Madya Jakarta Timur','KPP Madya Jakarta Selatan II','KPP Madya Jakarta Selatan I','KPP Madya Jakarta Pusat','KPP Madya Jakarta Barat','KPP Madya Dua Jakarta Utara','KPP Madya Dua Jakarta Timur','KPP Madya Dua Jakarta Selatan II','KPP Madya Dua Jakarta Selatan I','KPP Madya Dua Jakarta Pusat','KPP Madya Dua Jakarta Barat']

def read_file(filename):
    df = pd.read_csv(filename)
    return df

def combining_data():
    list_file = os.listdir("result")
    list_review = []
    list_page_source = []

    for f in list_file:
        try:
            if "_html" in f:
                d_list = pd.read_csv("result/{}".format(f))
                for d in range(len(d_list)):
                    list_page_source += [{
                        "kpp" : d_list.iloc[d]["nama_kpp"],
                        "page_source" : d_list.iloc[d]["html"],
                    }]
            
            elif ".csv" in f:
                d_list = pd.read_csv("result/{}".format(f))
                for d in range(len(d_list)):
                    list_review += [{
                        "kpp" : d_list.iloc[d]["kpp"],
                        "review" : d_list.iloc[d]["review"],
                    }]

            else:
                continue
        except:
            continue

    df_review = pd.DataFrame(list_review)
    df_review.to_csv("result/gabungan_review.csv", index = False)

    df_page_source = pd.DataFrame(list_page_source)
    df_page_source.to_csv("result/gabungan_page_source.csv", index = False)


def check_undowndloaded():
    df = pd.read_csv("result/gabungan_review.csv")
    k_list = []
    for k in range(len(df)):
        k_list += [df.iloc[k]["kpp"]]
    
    for kpp in kpp_list:
        if kpp in k_list:
            continue
        print(kpp)


if __name__ == "__main__":
    combining_data()
    check_undowndloaded()
