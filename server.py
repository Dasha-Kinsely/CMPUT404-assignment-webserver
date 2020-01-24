#  coding: utf-8
import socketserver
import sys
import os

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/

# Copyright 2020 Yun Tai Liu
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved


class MyWebServer(socketserver.BaseRequestHandler):
    source_dir = os.getcwd() + '/www/'

    def handle(self):
        self.data = self.request.recv(1024).strip()
        # print(self.data.decode('utf-8')) OKAY?
        request, header = self.data.decode('utf-8').split('\r\n', 1)
        method, req_dir, http_header = request.split()
        # print(method)||print(req_dir)||print(http_header)
        if method != 'GET':
            raise Err.MethodForbiddenError()
        elif http_header != 'HTTP/1.1':
            raise Err.HeaderForbiddenError()
        # Only happens if method and header are correct
        elif (method == 'GET') and (http_header == 'HTTP/1.1'):
            self.get_file(req_dir)
        else:
            raise Err.UnkownError()

    def get_file(self, req_dir):
        if ".html" in req_dir:
            mimetype = 'text/html'
        elif ".css" in req_dir:
            mimetype = 'text/css'
        elif req_dir[-1] == "/":
            mimetype = 'text/html'
            req_dir += "index.html"  # serves index in that folder
        else:
            mimetype = "text/html"
        try:  # the normal case
            f_name = MyWebServer.source_dir+(req_dir)
            file = open(f_name, 'r')
            content = file.read()
            self.request.sendall(bytearray(
                (self.res_header(200, 'OK', mimetype)+content), 'utf-8'
            ))
            file.close()
        except FileNotFoundError:
            self.request.sendall(bytearray(
                (self.res_header(404, 'Not Found', mimetype) +
                 "<html><body><h1 style = 'text-align:center'>404 NOT FOUND ERROR</h1></body></html>"), 'utf-8'
            ))

    def res_header(self, status_code, status_desc, mimetype):
        res_header_str = (
            'HTTP/1.1 '+str(status_code) + ' ' + status_desc + '\r\n' +
            'Content-Type: '+mimetype + '\r\n\r\n'
        )
        print(res_header_str)
        return res_header_str


class Err():
    def Details(self, param):
        print(param)

    def E301(self):
        self.Deatils("Moved Permenantly")

    def NotFoundError(self):
        self.Details('File not found....')

    def MethodForbiddenError(self):
        self.Details('You cannot post, delete or put!!!!')

    def HeaderForbiddenError(self):
        self.Details('Only http 1.1 is allowed')

    def UnknownError(self):
        self.Details("Error Unknown...")


# DO NOT MODIFY
if __name__ == "__main__":
    HOST, PORT = "localhost", 8080
    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)
    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
