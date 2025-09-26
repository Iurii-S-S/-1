import http.server
import socketserver
import webbrowser
import os

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # Добавляем CORS заголовки
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

def start_server(port=8080):
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    with socketserver.TCPServer(("0.0.0.0", port), MyHTTPRequestHandler) as httpd:
        print(f"Сервер фронтенда запущен на http://localhost:{port}")
        print("Откройте браузер и перейдите по указанному адресу")
        print("Для остановки сервера нажмите Ctrl+C")
        
        try:
            # Автоматически открываем браузер
            webbrowser.open(f'http://localhost:{port}')
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nОстановка сервера...")
            httpd.shutdown()

if __name__ == "__main__":
    start_server()