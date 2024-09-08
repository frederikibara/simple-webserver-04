# from http.server import BaseHTTPRequestHandler, HTTPServer
# import socket
# import threading
# from datetime import datetime
# import json
# import os
# import urllib.parse


# if not os.path.exists('storage'):
#     os.makedirs('storage')
# if not os.path.exists('storage/data.json'):
#     with open('storage/data.json', 'w') as f:
#         json.dump({}, f)


# class MyRequestHandler(BaseHTTPRequestHandler):
#     """
#     This class handles requests
#     to the server by providing static files and processing forms.

#     Methods:
#     - do_GET: Handles HTTP GET requests. Returns static files
#       (HTML, CSS, PNG) or a 404 error page if no file is found.
#     - do_POST: Handles HTTP POST requests. Receives form data and
#       sends them via UDP socket to another server for further processing.
#     """

#     def do_GET(self):

#         # Определите путь к статическим файлам
#         if self.path.startswith('/static/'):
#             file_path = self.path.lstrip('/')
#         else:
#             # Путь по умолчанию к HTML файлам
#             if self.path == '/':
#                 file_path = '/pages/index.html'
#             elif self.path == '/message.html':
#                 file_path = '/pages/message.html'
#             else:
#                 file_path = '/pages/error.html'
        
#         # Постройте полный путь к файлу
#         full_path = '.' + file_path

#         try:
#             with open(full_path, 'rb') as file:
#                 self.send_response(200)
#                 if file_path.endswith('.css'):
#                     self.send_header('Content-type', 'text/css')
#                 elif file_path.endswith('.png'):
#                     self.send_header('Content-type', 'image/png')
#                 elif file_path.endswith('.jpg'):
#                     self.send_header('Content-type', 'image/jpeg')
#                 else:
#                     self.send_header('Content-type', 'text/html')
#                 self.end_headers()
#                 self.wfile.write(file.read())
#         except FileNotFoundError:
#             self.send_response(404)
#             self.send_header('Content-type', 'text/html')
#             self.end_headers()
#             with open('pages/error.html', 'rb') as file:
#                 self.wfile.write(file.read())
                
            


# def run_http_server():
#     server_address = ('', 3000)
#     httpd = HTTPServer(server_address, MyRequestHandler)
#     print("Starting HTTP server on port 3000...")
#     httpd.serve_forever()


# def run_socket_server():
#     with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
#         sock.bind(('localhost', 5000))
#         print("Starting Socket server on port 5000...")
#         while True:
#             try:
#                 data, _ = sock.recvfrom(1024)
#                 print(f"Received data: {data}")  # Добавлено для отладки
#                 message = json.loads(data.decode('utf-8'))
#                 print(f"Parsed message: {message}")  # Добавлено для отладки

#                 timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
#                 with open('storage/data.json', 'r+') as f:
#                     try:
#                         storage = json.load(f)
#                     except json.JSONDecodeError:
#                         storage = {}
#                     storage[timestamp] = message
#                     f.seek(0)
#                     json.dump(storage, f, indent=4)
#             except Exception as e:
#                 print(f"Error processing UDP data: {e}")


# if __name__ == "__main__":
#     http_thread = threading.Thread(target=run_http_server)
#     socket_thread = threading.Thread(target=run_socket_server)
    
#     http_thread.start()
#     socket_thread.start()
    
#     http_thread.join()
#     socket_thread.join()



from http.server import SimpleHTTPRequestHandler, HTTPServer
import socket
import threading
import json
import datetime
import urllib.parse

class RequestHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        # Перевірка шляху і зміна для спеціальних випадків
        if self.path == '/':
            self.path = '/pages/index.html'
        elif self.path == '/message.html':
            self.path = '/pages/message.html'
        elif self.path == '/error.html':
            self.path = '/pages/error.html'
        
        # Дозволити обробку статичних файлів за допомогою батьківського класу
        return super().do_GET()

    def do_POST(self):
        if self.path == '/send_message':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            parsed_data = urllib.parse.parse_qs(post_data.decode('utf-8'))
            username = parsed_data.get('username', [''])[0]
            message = parsed_data.get('message', [''])[0]
            data = {
                'username': username,
                'message': message
            }
            udp_send_data = json.dumps(data).encode('utf-8')
            
            # Відправити дані на UDP сервер
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.sendto(udp_send_data, ('localhost', 5000))
            sock.close()
            
            self.send_response(302)
            self.send_header('Location', '/')
            self.end_headers()
        else:
            self.send_error(404, "File not found")

# UDP сервер
class UDPServer(threading.Thread):
    def __init__(self, port):
        super().__init__()
        self.port = port

    def run(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(('localhost', self.port))
        print(f"UDP server running on port {self.port}")
        while True:
            data, _ = sock.recvfrom(1024)
            if data:
                try:
                    message_data = json.loads(data.decode('utf-8'))
                    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
                    with open('storage/data.json', 'r+') as file:
                        try:
                            json_data = json.load(file)
                        except json.JSONDecodeError:
                            json_data = {}
                        json_data[timestamp] = message_data
                        file.seek(0)
                        json.dump(json_data, file, indent=4)
                except Exception as e:
                    print(f"Error processing data: {e}")

# HTTP сервер
def start_http_server(port):
    server = HTTPServer(('localhost', port), RequestHandler)
    print(f"HTTP server running on port {port}")
    server.serve_forever()

if __name__ == "__main__":
    # Запустити UDP сервер в окремому потоці
    udp_server_thread = UDPServer(5000)
    udp_server_thread.start()

    # Запустити HTTP сервер
    start_http_server(3000)

