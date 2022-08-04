#!/usr/bin/env python3

from http.server import BaseHTTPRequestHandler, HTTPServer
from jinja2 import Template, Environment, FileSystemLoader
from os import path
import time

hostName = "0.0.0.0"
serverPort = 8080

class MyServer(BaseHTTPRequestHandler):

    def do_GET(self):
        self.env = Environment(loader=FileSystemLoader('/var/lib/iotfw-admin/templates'))
        route = None

        if self.path == "/" or self.path == "/index.html" or self.path == "/index.htm":
            route = "index.html"
        elif path.isfile("/var/lib/iotfw-admin/templates/" + self.path.split("/")[-1]):
            route = self.path.split("/")[-1]

        if route:
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            template = self.env.get_template(route)
            self.wfile.write(bytes(template.render(), "utf-8"))
            return

        if self.path.startswith("/css"):
            cssfile = self.path.split("/")[-1]
            if path.isfile("/var/lib/iotfw-admin/css/" + cssfile):
                self.send_response(200)
                self.send_header("Content-type", "text/css")
                self.end_headers()

                with open("/var/lib/iotfw-admin/css/" + cssfile, 'rb') as file:
                    self.wfile.write(file.read())
                return
            else:
                self.send_response(404)
                self.end_headers()
                return

        else:
            self.send_response(404)
            self.end_headers()

if __name__ == "__main__":        
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
