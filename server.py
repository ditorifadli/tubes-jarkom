from socket import *
import threading

def handle_connection(connectionSocket):
    message = connectionSocket.recv(1024).decode()
    print(message)

    # memparsing request dari client
    request_method = message.split()[0]
    file_requested = message.split()[1]

    #index.html sebagai default ketika server dijalankan
    if file_requested == '/':
        file_requested = '/index.html'
        
    # dictionary untuk mapping file extension dengan content type
    content_types = {
        'html': 'text/html',
        'css': 'text/css',
        'jpeg': 'image/jpeg',
        'jpg': 'image/jpeg',
        'png': 'image/png',
        'txt': 'text/plain',
        'js': 'application/javascript',
        'video': 'video/mp4',
        'pdf': 'application/pdf',
        'mp3': 'audio/mpeg',
        'mp4': 'video/mp4',   
    }

    # membuka file yang diminta oleh client
    try:
        file_extension = file_requested.split('.')[-1]
        file = open(file_requested[1:], 'rb')
        file_content = file.read()
        file.close()

        # mencari content type berdasarkan file extension
        content_type = content_types.get(file_extension, 'application/octet-stream')

        # membuat HTTP response message yang terdiri dari header dan file yang diminta
        response_header = f'HTTP/1.1 200 OK\r\nContent-Type: {content_type}\r\n\r\n'
        response_content = file_content

        # mengirimkan HTTP response message ke client
        connectionSocket.send(response_header.encode())
        connectionSocket.send(response_content)

    # mengirimkan pesan "404 Not Found" jika file yang diminta tidak ditemukan
    except IOError:
        file = open('404.html', 'rb')
        file_content = file.read()
        file.close()

        response_header = 'HTTP/1.1 404 Not Found\r\nContent-Type: text/html\r\n\r\n'
        response_content = file_content

        # mengirimkan HTTP response message ke client
        connectionSocket.send(response_header.encode())
        connectionSocket.send(response_content)
    # menutup koneksi
    connectionSocket.close()

# membuat TCP socket
serverSocket = socket(AF_INET, SOCK_STREAM)

# mengaitkan socket ke alamat dan port tertentu
serverHost = 'localhost'  # alamat IP lokal
serverPort = 80 # port yang digunakan

#bind: menyatukan host dan port
serverSocket.bind((serverHost, serverPort))

# menyediakan server socket untuk menerima koneksi dari client
serverSocket.listen(1)

print(f'Server berjalan di http://{serverHost}:{serverPort}/')
print("Server siap digunakan!")
while True:
    # menerima koneksi dari client
    connectionSocket, addr = serverSocket.accept()

    # membuat thread baru untuk menangani koneksi
    t = threading.Thread(target=handle_connection, args=(connectionSocket,))
    t.start()
