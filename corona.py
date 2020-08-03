# do all the imports
import threading
import time
import tkinter as tk
import database


import bs4
import plyer
import requests



# get html data of website
def get_html_data(url):
    data = requests.get(url)
    return data


# parsing html and extracting data
def get_corona_detail_of_india():
    global count,all_details
    url = "https://www.mohfw.gov.in/"
    html_data = get_html_data(url)
    bs = bs4.BeautifulSoup(html_data.text, "html.parser")
    info_div = bs.find("div", class_="site-stats-count").find_all("li", class_=["bg-blue", "bg-green", "bg-red", "bg-orange"])
    all_details = ""
    for block in info_div:
        count = block.find("strong").get_text()
        text = block.find("span").get_text()
        all_details = all_details + text + " : " + count + "\n"
    return all_details


# function use to  reload the data from website
def refresh():
    newdata = get_corona_detail_of_india()
    print("Refreshing..")
    mainLabel['text'] = newdata


# function for notifying...
def notify_me():
    while True:
        plyer.notification.notify(
            title="COVID 19 cases of INDIA",
            message=get_corona_detail_of_india(),
            timeout=10,
            app_icon='virus.ico'
        )
        time.sleep(30)


# creating gui:
root = tk.Tk()
root.geometry("500x500")
root.iconbitmap("virus.ico")
root.title("CORONA DATA TRACKER - INDIA")
root.configure(background='white')
f = ("poppins", 25, "bold")
banner = tk.PhotoImage(file="virus.png")
bannerLabel = tk.Label(root, image=banner)
bannerLabel.pack()
mainLabel = tk.Label(root, text=get_corona_detail_of_india(), font=f, bg='white')
mainLabel.pack()

reBtn = tk.Button(root, text="REFRESH", font=f, relief='solid', command=refresh)
reBtn.pack()




# create a new thread
th1 = threading.Thread(target=notify_me)
th1.setDaemon(True)
th1.start()

root.mainloop()





