from http.server import BaseHTTPRequestHandler, HTTPServer
import json
data =[{
        "name":"Sam Larry",
        "track":"AI Developer"
    },
    {
        "name":"YONDA ASA",
        "track":"AI Backend"
    }
]
class BasicAPI(BaseHTTPRequestHandler):
    def send_data(self, payload, status = 200):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(payload).encode())
    def do_PUT(self):
        cotent_size =int(self.headers.get("Content-Length",0))
        parsed_data = self.rfile.read(cotent_size)
        pUT_data = json.loads(parsed_data)
        if data:
            data[0] = pUT_data
            self.send_data({
            "Message":"Data Replaced",
            "data":data[0]
        })
        else:
          data.append(pUT_data)
          self.send_data({
            "Message":"Data Addeded",
            "data":pUT_data
        })
def run():
    HTTPServer(("localhost", 5000), BasicAPI).serve_forever()
print("Application is running")
run()






