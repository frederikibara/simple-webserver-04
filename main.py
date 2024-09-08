from http.server import BaseHTTPRequestHandler, HTTPServer
import socket
import threading
from datetime import datetime
import json
import os
import urllib.parse

# Убедитесь, что каталоги и файлы существуют
if not os.path.exists('storage'):
    os.makedirs('storage')
if not os.path.exists('storage/data.json'):
    with open('storage/data.json', 'w') as f:
        json.dump({}, f)


class MyRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.path = '/index.html'
        elif self.path == '/message.html':
            self.path = '/message.html'
        elif self.path == '/style.css':
            self.path = '/style.css'
        elif self.path == '/logo.png':
            self.path = '/logo.png'
        elif self.path == '/error.html':
            self.path = '/error.html'
        
        try:
            with open(self.path.lstrip('/'), 'rb') as file:
                self.send_response(200)
                if self.path.endswith('.css'):
                    self.send_header('Content-type', 'text/css')
                elif self.path.endswith('.png'):
                    self.send_header('Content-type', 'image/png')
                else:
                    self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(file.read())
        except FileNotFoundError:
            self.send_response(404)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open('error.html', 'rb') as file:
                self.wfile.write(file.read())
    
    
    def do_POST(self):
        if self.path == '/submit':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            print(f"Received POST data: {post_data}")  # Добавлено для отладки

            # Декодирование данных формы
            form_data = urllib.parse.parse_qs(post_data)
            print(f"Parsed form data: {form_data}")  # Добавлено для отладки
            message_data = {
                "username": form_data.get('username', [''])[0],
                "message": form_data.get('message', [''])[0]
            }

        # Отправка данных на UDP сервер
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
                sock.sendto(json.dumps(message_data).encode('utf-8'), ('localhost', 5000))
            print("Data sent to UDP server")  # Добавлено для отладки
        except Exception as e:
            print(f"Error sending data to UDP server: {e}")

        self.send_response(302)
        self.send_header('Location', '/message.html')
        self.end_headers()


def run_http_server():
    server_address = ('', 3000)
    httpd = HTTPServer(server_address, MyRequestHandler)
    print("Starting HTTP server on port 3000...")
    httpd.serve_forever()


def run_socket_server():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.bind(('localhost', 5000))
        print("Starting Socket server on port 5000...")
        while True:
            try:
                data, _ = sock.recvfrom(1024)
                print(f"Received data: {data}")  # Добавлено для отладки
                message = json.loads(data.decode('utf-8'))
                print(f"Parsed message: {message}")  # Добавлено для отладки

                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
                with open('storage/data.json', 'r+') as f:
                    try:
                        storage = json.load(f)
                    except json.JSONDecodeError:
                        storage = {}
                    storage[timestamp] = message
                    f.seek(0)
                    json.dump(storage, f, indent=4)
            except Exception as e:
                print(f"Error processing UDP data: {e}")


if __name__ == "__main__":
    http_thread = threading.Thread(target=run_http_server)
    socket_thread = threading.Thread(target=run_socket_server)
    
    http_thread.start()
    socket_thread.start()
    
    http_thread.join()
    socket_thread.join()
