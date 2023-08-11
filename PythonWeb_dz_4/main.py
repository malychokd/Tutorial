from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse
import mimetypes
import pathlib
import mimetypes
import json
import socket
from datetime import datetime
from threading import Thread

BASE_DIR = pathlib.Path()

class MainServer(BaseHTTPRequestHandler):
    
    def do_POST(self):
        data = self.rfile.read(int(self.headers['Content-Length']))
        #print("data:")
        #print(data)
        self.send_data_via_socket(data.decode())
        #self.save_data_to_json(data)
        self.send_response(200)
        self.send_header('Location', '/message')
        self.end_headers()

    def do_GET(self):
        return self.router()

    def router(self):
        pr_url = urllib.parse.urlparse(self.path)

        if pr_url.path == '/':
            self.send_html_file('index.html')
        elif pr_url.path == '/message':
            self.send_html_file('message.html')
        else:
            file = BASE_DIR.joinpath(pr_url.path[1:])
            if file.exists():
                self.send_static(file)
            else:
                self.send_html_file('error.html', 404)

    def send_static(self, file):
        self.send_response(200)
        mt = mimetypes.guess_type(self.path)
        if mt:
            self.send_header("Content-type", mt[0])
        else:
            self.send_header("Content-type", 'text/plain')
        self.end_headers()
        with open(file, 'rb') as fd:
            self.wfile.write(fd.read())

    def send_html_file(self, filename, status=200):
        self.send_response(status)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        with open(filename, 'rb') as fd:
            self.wfile.write(fd.read())

    def send_data_via_socket(self, message):
        host = socket.gethostname()
        port = 5000

        client_socket = socket.socket()
        client_socket.connect((host, port))
        
        while message.lower():
            client_socket.send(message.encode())
            data = client_socket.recv(1024).decode()
            print(f'received message: {data}')
            message = input('--> ')

        client_socket.close()

def run(server_class=HTTPServer, handler_class=MainServer):
    server_address = ('', 3000)
    http = server_class(server_address, handler_class)
    try:
        print("Start running")
        socket_server = Thread(target=server_socket)
        socket_server.start()
        http.serve_forever()
    except KeyboardInterrupt:
        http.server_close()

def server_socket():
    print("socket start listening")
    host = socket.gethostname()
    port = 5000

    server_socket = socket.socket()
    server_socket.bind((host, port))
    server_socket.listen(2)
    conn, address = server_socket.accept()
    print(f'Connection from {address}')
    while True:
        data = conn.recv(100).decode()

        if not data:
            break
        #print(f'received message: {data}')
        data_parse = urllib.parse.unquote_plus(data)
        data_parse = {key: value for key, value in [el.split('=') for el in data_parse.split('&')]}

        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        new_message = {
            current_time: {
                "username": data_parse.get('username'),
                "message": data_parse.get('message')
            }
        }
        # Зчитуємо наявний вміст файлу (якщо файл вже існує)
        try:
            with open(BASE_DIR.joinpath('storage/data.json'), 'r') as file:
                data_f = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            # Якщо файл не існує або порожній, створюємо новий словник
            data_f = {}
        # Додаємо нове повідомлення до словника
        data_f.update(new_message)
        with open(BASE_DIR.joinpath('storage/data.json'), 'w', encoding='utf-8') as file:
            json.dump(data_f, file, ensure_ascii=False, indent=2)
    conn.close()        

run()
