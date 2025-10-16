from http.server import BaseHTTPRequestHandler, HTTPServer
import json
data = [{
        "name":"Sam Larry",
        "track":"AI Developer"
    },
    {
        "name":"YONDA ASA",
        "track":"AI Backend"
    }]
class BasicAPI(BaseHTTPRequestHandler):
    def send_data(self, payload, status = 200):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(payload).encode())
    def do_DELETE(self):
        if data:
           data.clear()
           self.send_data({
            "Message":"Data Deleted",
            "data": []
            })
        else:
            self.send_data({
                "Message": "There no data to delete"
            })
def run():
    HTTPServer(("localhost", 5000), BasicAPI).serve_forever()
print("Application is running")
run()














