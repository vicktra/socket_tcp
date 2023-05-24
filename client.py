import socket
import threading
from time import sleep

# khai báo cổng và địa chỉ server
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = socket.gethostbyname(socket.gethostname())

#tạo socket cho client với địa chỉ và cổng khai báo và thực hiện kết nối
ADDR = (SERVER,PORT)
client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect(ADDR)
connected = True

#hàm xử lý gói tin nhận được từ server nếu kết nối thành công ta thực hiện câu lệnh while bên dưới
#và thực hiện nhận gói tin từ server với độ dài 1024 byte và giải mã theo chuẩn utf-8
#sau đó in ra nội dung gói tin với các câu lệnh print bên dưới
def handle_rev(client):
    global connected
    while connected:
        msg = client.recv(1024).decode(FORMAT)
        print("" + msg)
        print("C01>")
       # print(len(msg))

#hàm xử lý gói tin gửi đi cho server nếu kết nối thành công ta thực hiện câu lệnh while bên dưới
#và thực hiện gửi gói tin với độ dài 1024 byte và mã hóa theo chuẩn utf-8
#với thông điệp là tên client + nội dung gửi đi và nếu trong nội dung chỉ có từ !DISCONNECT thì dừng lại
def handle_send(client):
    global connected
    while connected:
        msg = input("C01>")
        send("[Client 01]  " + msg)
        if msg == DISCONNECT_MESSAGE:
            connected = False
#hàm thực hiện kết nối  và tạo luồng kết nối gửi đi và tạo luồng kết nối nhận về 
#khi thực hiện gửi đi ta mã hóa nội dung tin nhắn theo chuẩn utf-8 và thực hiện lệnh send()
#sau đó thực hiện chờ các phản hồi tiếp theo từ server cho đến khi client ngắt kết nối
def send(msg):
    message = msg.encode(FORMAT)
    message+= b' ' * (30 - len(message))
    client.send(message)
thead = threading.Thread(target=handle_rev,args=(client,))
thead.start()
thead = threading.Thread(target=handle_send,args=(client,))
thead.start()
while connected:
    sleep(2)