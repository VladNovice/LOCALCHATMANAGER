import rsa
import threading
import socket
import tkinter as tk
from tkinter import Label, PhotoImage, ttk
from tkinter import messagebox


client = None
server = None
public_partner = None
connected = False
public_key, private_key = rsa.newkeys(1024) 

def start_server():
    global server, client, public_partner, connected
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(("local ip", 9999))   # local ip
        server.listen()
        client, _ = server.accept()
        client.send(public_key.save_pkcs1("PEM"))  
        public_partner = rsa.PublicKey.load_pkcs1(client.recv(1024))  
        connected = True
        threading.Thread(target=receive_message).start()
        status_label.config(text="Подключено (Хост)")
        send_button.config(state="normal")
    except Exception as e:
        messagebox.showerror("Ошибка", f"Ошибка при подключении: {e}")


def connect_to_server():
    global client, public_partner, connected
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(("local ip", 9999))  #local ip
        public_partner = rsa.PublicKey.load_pkcs1(client.recv(1024))  
        client.send(public_key.save_pkcs1("PEM"))  
        connected = True
        threading.Thread(target=receive_message).start()
        status_label.config(text="Подключено (Клиент)")
        send_button.config(state="normal")
    except Exception as e:
        messagebox.showerror("Ошибка", f"Ошибка при подключении: {e}")

def send_message(event=None):
    if connected:
        message = entry.get()
        if message:
            encrypted_message = rsa.encrypt(message.encode(), pub_key=public_partner)
            client.send(encrypted_message)
            messages.config(state="normal")
            messages.insert(tk.END, "Вы: " + message + "\n")
            messages.config(state="disabled")
            entry.delete(0, tk.END)
    else:
        messagebox.showwarning("Предупреждение", "Сначала подключитесь к серверу")

def receive_message():
    while connected:
        try:
            encrypted_message = client.recv(1024)
            decrypted_message = rsa.decrypt(encrypted_message, private_key).decode()
            messages.config(state="normal")
            messages.insert(tk.END, "Anonim: " + decrypted_message + "\n")
            messages.config(state="disabled")
        except:
            pass


root = tk.Tk()
root.title("Чат с шифрованием")
root.geometry("600x450")
root.maxsize(width=600, height=900)
root.minsize(width=600, height=450)
icon_image = tk.PhotoImage(file='catizen.png')


root.iconphoto(False, icon_image)



server_button = ttk.Button(root, text="Стать Хостом", padding=(2, 2), command=start_server)
server_button.place(x=300, y=345)  

client_button = ttk.Button(root, text="Подключиться", padding=(2, 2), command=connect_to_server)
client_button.place(x=200, y=345)


messages = tk.Text(root, state="disabled", wrap=tk.WORD, height=20)
messages.pack()






entry = tk.Entry(root, width=50)
entry.bind("<Return>", send_message)
entry.pack()


send_button = ttk.Button(root, text="Отправить", padding=(10, 0), command=send_message, state="disabled")
send_button.place(x=400, y=323)


status_label = tk.Label(root, text="Не подключено")
status_label.place(x=245, y=380)


root.mainloop()







