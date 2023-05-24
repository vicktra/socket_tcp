import socket
import threading

PORT = 5050    #cổng kết nối
SERVER = socket.gethostbyname(socket.gethostname()) # lấy địa chỉ server
ADDR = (SERVER,PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
clients = []
#tạo socket cho server tham số : socket.AF_INET tham số truyền vào phiên bản IP chúng ta sẽ sử dụng và socket.SOCK_STREAM loại kết nối là TCP
server = socket.socket(socket.AF_INET,socket.SOCK_STREAM) 
#Đăng ký tên, gán địa chỉ vào socket
server.bind(ADDR)
#quản lý khi client kết nối tới sever 
def handle_client(conn,addr):
    print(f"[NEW CONNECTION] {addr} connectted .")
    #khi có kết nối tới sever thì thực hiện vòng lặp
    while True:
     try:
        #client gửi dữ liệu tới sever đọc dữ liệu với độ dài là 1024 byte giải mã theo chuẩn utf-8
        msg = conn.recv(1024).decode(FORMAT)
        #kiểm tra nếu client gửi '!DISCONNECT' thì dừng kết nói với client đó 
        if msg[13:13+len(DISCONNECT_MESSAGE)] == DISCONNECT_MESSAGE:
            clients.remove(conn)
            #hiển thị máy client nào đã ngắt kết nối sau nghi gửi !DISCONNECT
            print(f"[{addr}] ---end---")
            break
        print(f"[{addr}] {msg}")
        print(len(msg))
        #nếu không phải !DISCONNECT thì thực hiện gửi lại nội dung y hệt mà client đã gửi tới sever
        for remote_client in clients:
            #thực hiện gửi nội dung đó cho các client khác mà không gửi lại chính client đã gửi
            #ví dụ client 1 gửi '123' cho server thì server chỉ gửi lại '123' cho client 2,client 3 mà không gửi về client 1 nữa
            if remote_client != conn:
                remote_client.send(msg.encode(FORMAT))
     except:
        #nếu client thực hiện việc tắt nóng thì tự động xóa client đó ra khỏi server
            clients.remove(conn)
            print(f"[{addr}] ---end---")
            break
    conn.close()
    #tạo kết nối 
def start():
    #thực hiện lắng nghe và chờ đợi liên tục cho đến khi có kết nối
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        #Server chấp nhận nối kết của client, khi đó một kênh giao tiếp ảo được hình thành, Client và server có thể trao đổi thông tin với nhau thông qua kênh ảo này.
        #sau đó cho biết hiện tại có bao nhiêu kết nối đến server với câu lệnh print tiếp 
        conn,addr = server.accept()
        print(f"[ACTIVE CONNECTIONS]{threading.active_count()-1}")

        #thực hiện thêm client vào server với câu lệnh append thêm cuối danh sách client
        clients.append(conn)

        #tạo một luồng kết nối giữa server và client và khởi động luồng kết nối
        thread = threading.Thread(target= handle_client,args=(conn,addr))
        thread.start()
        
          #sau đó tiếp tục chờ cho đến khi có kết nối mới hoặc có ngắt kết nối
print("[STARTING] server is starting...")
start()