from selenium import webdriver
from time import sleep
from selenium.webdriver.common.action_chains import ActionChains
import pandas as pd
from bs4 import BeautifulSoup as bs
from datetime import datetime
from combining_file import combining_data
from read_html import main as read_html_main



kpp_list = ['KPP Pratama Jakarta Tebet','KPP Pratama Jakarta Tanjung Priok','KPP Pratama Jakarta Tanah Abang Tiga','KPP Pratama Jakarta Tanah Abang Satu','KPP Pratama Jakarta Tanah Abang Dua','KPP Pratama Jakarta Tambora','KPP Pratama Jakarta Tamansari','KPP Pratama Jakarta Sunter','KPP Pratama Jakarta Setiabudi Tiga','KPP Pratama Jakarta Setiabudi Satu','KPP Pratama Jakarta Setiabudi Empat','KPP Pratama Jakarta Setiabudi Dua','KPP Pratama Jakarta Senen','KPP Pratama Jakarta Sawah Besar Satu','KPP Pratama Jakarta Sawah Besar Dua','KPP Pratama Jakarta Pulogadung','KPP Pratama Jakarta Pluit','KPP Pratama Jakarta Pesanggrahan','KPP Pratama Jakarta Penjaringan','KPP Pratama Jakarta Pasar Rebo','KPP Pratama Jakarta Pasar Minggu','KPP Pratama Jakarta Pancoran','KPP Pratama Jakarta Palmerah','KPP Pratama Jakarta Pademangan','KPP Pratama Jakarta Menteng Tiga','KPP Pratama Jakarta Menteng Satu','KPP Pratama Jakarta Menteng Dua','KPP Pratama Jakarta Matraman','KPP Pratama Jakarta Mampang Prapatan','KPP Pratama Jakarta Kramat Jati','KPP Pratama Jakarta Koja','KPP Pratama Jakarta Kembangan','KPP Pratama Jakarta Kemayoran','KPP Pratama Jakarta Kelapa Gading','KPP Pratama Jakarta Kebon Jeruk Satu','KPP Pratama Jakarta Kebon Jeruk Dua','KPP Pratama Jakarta Kebayoran Lama','KPP Pratama Jakarta Kebayoran Baru Tiga','KPP Pratama Jakarta Kebayoran Baru Satu','KPP Pratama Jakarta Kebayoran Baru Empat','KPP Pratama Jakarta Kebayoran Baru Dua','KPP Pratama Jakarta Kalideres','KPP Pratama Jakarta Jatinegara','KPP Pratama Jakarta Jagakarsa','KPP Pratama Jakarta Grogol Petamburan','KPP Pratama Jakarta Gambir Tiga','KPP Pratama Jakarta Gambir Satu','KPP Pratama Jakarta Gambir Empat','KPP Pratama Jakarta Gambir Dua','KPP Pratama Jakarta Duren Sawit','KPP Pratama Jakarta Cilandak','KPP Pratama Jakarta Cengkareng','KPP Pratama Jakarta Cempaka Putih','KPP Pratama Jakarta Cakung','KPP Madya Jakarta Utara','KPP Madya Jakarta Timur','KPP Madya Jakarta Selatan II','KPP Madya Jakarta Selatan I','KPP Madya Jakarta Pusat','KPP Madya Jakarta Barat','KPP Madya Dua Jakarta Utara','KPP Madya Dua Jakarta Timur','KPP Madya Dua Jakarta Selatan II','KPP Madya Dua Jakarta Selatan I','KPP Madya Dua Jakarta Pusat','KPP Madya Dua Jakarta Barat']

def saving_page(filename, f):
    with open(filename, "w") as fhtml:
        fhtml.write(f)
        fhtml.close()


def crawl(driver,nama_kpp):
    error = {}

    kpp = nama_kpp.split(" ")
    kpp = "+".join(kpp)

    link = "https://www.google.com/search?q=google+review+{}".format(kpp)
    print(link)

    driver.maximize_window()

    ulang = 0
    while ulang < 5:
        ulang += 1
        try:
            driver.get(link)
            sleep(5)
            a = driver.find_element_by_link_text("Lihat semua ulasan Google")
            a.click()
            break

        except:
            continue

    list_review = []
    try:
        sleep(2)
        count_review = driver.find_element_by_xpath("/html/body/span[2]/g-lightbox/div/div[2]/div[3]/span/div/div/div/div[1]/div[3]/div[1]/div/span/span").text

        count_review = count_review.split(" ")[0]
        count_review = int(count_review)
        print("searching {}".format(count_review))

        sleep(2)

        i = 0
        j = 0
        for x in range(count_review + int(count_review/10)):
            r = ""
            if len(list_review) > count_review:
                break
            try:
                r = driver.find_element_by_xpath("/html/body/span[2]/g-lightbox/div/div[2]/div[3]/span/div/div/div/div[2]/div[4]/div[{i}]/div[2]/div[{j}]".format(
                    i = i+1,
                    j = j+1,
                )).text
                j += 1


            except:
                target = driver.find_element_by_xpath("/html/body/span[2]/g-lightbox/div/div[2]/div[3]/span/div/div/div/div[2]/div[4]/div[{i}]/div[2]/div[{j}]".format(
                    i = i+1,
                    j = j,
                ))
                actions = ActionChains(driver)
                actions.move_to_element(target)
                actions.perform()
                driver.execute_script("""
                    let scroll_to_bottom = document.getElementsByClassName('review-dialog-list')[0]
                    function scrollBottom(element) {
                        element.scroll({ top: element.scrollHeight, behavior: "smooth"})
                        }

                    scrollBottom(scroll_to_bottom);"""
                )

                sleep(2)
                i += 1
                j = 0

                expand_list = ["More", "Lengkapnya"]
                for t in expand_list:
                    for c in range(5):
                        more_list = driver.find_elements_by_link_text(t)
                        for m in more_list:
                            m.click()

                sleep(1)
                continue

            list_review += [{
                "kpp": nama_kpp,
                "id" : x,
                "review" : r,
            }]

    except Exception as e:
        error = {
            "kpp" : nama_kpp,
            "error" : e,
            "time" : datetime.now(),
        }


    # export data review
    df = pd.DataFrame(list_review)
    df.to_csv("result/{}.csv".format(nama_kpp), index=False)

    # export html
    z = pd.DataFrame([{
        "nama_kpp" : nama_kpp,
        "html" : bs(driver.page_source, "lxml"),
    }])
    z.to_csv("result/{}_html.csv".format(nama_kpp), index=False)
    
    return error


def initDriver():
    options = webdriver.ChromeOptions()
    options.add_experimental_option(
        "prefs", {
            "intl.accept_languages" : "id",
        }
    )
    options.add_argument("--incognito")
    driver_chrome = webdriver.Chrome(options=options)
    return driver_chrome

def main():
    driver_chrome = initDriver()
    
    error_list = []
    count_kpp = 0
    for kpp in kpp_list:
        count_kpp +=1

        if count_kpp %5 == 4:
            driver_chrome.close()
            driver_chrome = initDriver()

        e = crawl(driver_chrome, kpp)
        if e != {}:
            error_list += [e]

        if count_kpp == len(kpp_list):
            driver_chrome.close()

    df_error = pd.DataFrame(error_list)
    df_error.to_csv("log.csv", index = False)

    combining_data()
    read_html_main()

if __name__ == "__main__":
    main()


# /html/body/span[2]/g-lightbox/div/div[2]/div[3]/span/div/div/div/div[2]/div[4]/div[2]/div[2]/div[10]/div[1]/div[3]/div[2]/span/span/a