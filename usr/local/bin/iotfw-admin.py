#!/usr/bin/env python3

import getopt
from http.server import BaseHTTPRequestHandler, HTTPServer
from jinja2 import Template, Environment, FileSystemLoader
from os import getpid, path
import pickle
from sys import argv
import time

hostName = "0.0.0.0"

class AdminServer(BaseHTTPRequestHandler):

    def __init__(self, *args):
        # Load configuration hashes
        try:
            with open('/etc/iotfw/cluster.db', 'rb') as handle:
                self.cluster = pickle.loads(handle.read())
        except FileNotFoundError:
            self.cluster = {}

        try:
            with open('/etc/iotfw/config.db', 'rb') as handle:
                self.config = pickle.loads(handle.read())
        except FileNotFoundError:
            self.config = {}

        BaseHTTPRequestHandler.__init__(self, *args)

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
            self.wfile.write(bytes(template.render(cluster=self.cluster), "utf-8"))
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

    def do_POST(self):
        if self.path.startswith('/api'):
            if self.path == '/api/cluster/join':
                return
        elif self.path == '/save/cluster':
            # Save cluster hash
            with open('/etc/iotfw/cluster.db', 'wb') as handle:
                pickle.dump(self.cluster, handle)

            self.send_response(302)
            self.send_header('Location', '/clustering.html')
            self.end_headers()
            return

        elif self.path == '/save/settings':
            # Save settings hash
            with open('/etc/iotfw/settings.db', 'wb') as handle:
                pickle.dump(self.settings, handle)

            self.send_response(302)
            self.send_header('Location', '/settings.html')
            self.end_headers()
            return

        else:
            self.send_response(404)
            self.end_headers()
            return

if __name__ == "__main__":        

    # Parse command-line options
    opts, args = getopt.getopt(argv[1:], "i:p:")

    pidfn = '/var/run/iotfw/iotfw-admin.pid'
    serverPort = 8080

    for opt, arg in opts:
        print(opt)
        if opt == '-i':
            pidfn = arg
        if opt == '-p':
            serverPort = int(arg)

    # Write PID file
    with open(pidfn, 'w', encoding='utf-8') as pidfile:
        pidfile.write(str(getpid()))

    webServer = HTTPServer((hostName, serverPort), AdminServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
