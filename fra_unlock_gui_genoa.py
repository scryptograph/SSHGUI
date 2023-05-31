# FRA Unlock Automation Script
# GUI Version - Powered by Python 3, Selenium, Firefox v102+ and Tkinter
# Author - Jerry Paul
# 07/28/2022

import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import *
import time
from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.by import By
import getpass
import os
import json
import shutil

# Selenium Configuration
options = FirefoxOptions()
options.headless = True
options.accept_insecure_certs = True
serialNum = []
fraKey = []
driver = webdriver.Firefox(options=options)

# Tkinter Window Configuration
window = tk.Tk()
window.geometry("700x450")
window.title("FRA Unlock")
progress = Progressbar(window, orient=HORIZONTAL, length=100, mode="determinate")

# Function to generate FRA Keys
def get_FRA():
    # Update Progress Bar and Change UI Elements
    submitButton["state"] = DISABLED
    submitButton["text"] = 'Fetching FRA Keys'
    progress.pack(pady=10)
    progress['value'] = 20
    window.update_idletasks()
    # Fetch FRA Keys
    fetch_fra()
    # UI Element Update
    progress['value'] = 80
    window.update_idletasks()
    submitButton["text"] = 'Generating Config File'
    # Generate Config File
    gen_FRAConf()
    # UI Element Update + Success Message
    progress['value'] = 100
    window.update_idletasks()
    messagebox.showinfo("Done", "Fra Keys Generated")
    progress.pack_forget()
    submitButton["state"] = NORMAL
    submitButton["text"] = 'Generate FRA Config File'

def fetch_fra():
    user = username.get()
    passWD = passwd.get()
    driver.get("https://" + user + ":" + passWD + "@atlkds-proxy01.amd.com/pspseta/fraPassword.action#mainMenu")
    print(driver.title)
    print("Reading FRA Serial Numbers...")
    try:
        serial_file = open('FRAKey.log', 'r')
    except:
        print("FRAKey.log file missing from location")
    lines = serial_file.readlines()
    for l in lines:
        serialNum.append(l[2:])
    # Send Query
    for i in serialNum:
        driver.find_element(By.ID, "fraPassword_asicUnitID").clear()
        driver.find_element(By.ID, "fraPassword_asicUnitID").send_keys(i)
        driver.find_element(By.CSS_SELECTOR, "tr:nth-child(4) input").click()
        fraKey.append(driver.find_element(By.XPATH, "/html/body/div[4]/table/tbody[2]/tr[1]/td[2]/div").text)

def gen_FRAConf():
    dictionary = {
        "ManId": "0002B0008001003",
        "Model": "01h",
        "Product": "STONES",
        "FraKeys": {
            "DIE0FraKey": "{}".format(fraKey[0].strip()),
            "DIE1FraKey": "{}".format(fraKey[1].strip()),
            "DIE2FraKey": "{}".format(fraKey[2].strip()),
            "DIE3FraKey": "{}".format(fraKey[3].strip()),
            "DIE4FraKey": "{}".format(fraKey[4].strip()),
            "DIE5FraKey": "{}".format(fraKey[5].strip()),
            "DIE6FraKey": "{}".format(fraKey[6].strip()),
            "DIE7FraKey": "{}".format(fraKey[7].strip()),
            "DIE8FraKey": "{}".format(fraKey[8].strip()),
            "DIE9FraKey": "{}".format(fraKey[9].strip()),
            "DIE10FraKey": "{}".format(fraKey[10].strip()),
            "DIE11FraKey": "{}".format(fraKey[11].strip()),
            "DIE12FraKey": "{}".format(fraKey[12].strip()),
        }
    }
    json_object = json.dumps(dictionary, indent=4)
    with open("FraConfig.json", "w") as outfile:
        outfile.write(json_object)
    source_path = "/usr/local/sslt_client/FraConfig.json"
    destination_path = "/usr/local/sslt_client/conf/dropins/FraConfig.json"
    shutil.move(source_path,destination_path)
    driver.close()

# Generate Tkinter Elements
label = tk.Label(text="FRA Unlock Tool", font="Helvetica 30")
label.pack(pady=35)
label1 = tk.Label(text="This script will automatically use the KDS Keys Website to generate the FRA Config File needed for unlocking the part", font="Helvetica 12")
label1.pack(pady=5)
label2 = tk.Label(text="Sign-in using AMD SSO Username and Password. Make sure the user has access to KDS Keys FRA Unlock!", font="Helvetica 12")
label2.pack(pady=5)
spacer1 = tk.Label(window, text="")
spacer1.pack(pady=5)
usernameLabel = tk.Label(text="Username:", font="Helvetica 12")
usernameLabel.pack()
username = tk.Entry(font="Helvetica 12")
username.pack(pady=5)
passwordLabel = tk.Label(text="Password:", font="Helvetica 12")
passwordLabel.pack()
passwd = tk.Entry(show="*")
passwd.pack(pady=5)
submitButton = tk.Button(
    text="Generate FRA Config File",
    width="25",
    height="5",
    command=get_FRA
)
submitButton.pack(pady=20)

window.mainloop()

