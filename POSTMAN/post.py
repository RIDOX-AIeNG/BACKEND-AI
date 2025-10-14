from http.server import BaseHTTPRequestHandler, HTTPServer

import json

data = []
class BasicAPI(BaseHTTPRequestHandler):
    def send_data(self, data, status = 200):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def do_POST(self):
        contact_size = int(self.headers.get('COntent-Length', 0))
        parsed_data = self.rfile.read(contact_size)

        post_data = json.loads(parsed_data)
        data.append(post_data) #saving data to database
        self.send_data({
            "Message": "Data Recieved",
            "data": post_data
        })

def run():
    HTTPServer(('localhost', 5000), BasicAPI).serve_forever()

print("Application is running")
run()

