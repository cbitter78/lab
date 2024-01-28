#!/usr/bin/env python3

import logging
import json
import sys
import platform
import os
from http.server import BaseHTTPRequestHandler, HTTPServer
from logging.handlers import SysLogHandler

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class S(BaseHTTPRequestHandler):
    def _write_log(self, ip, msg):
        with open(f"{ip}.log", "a") as log_file:
            log_file.write(f"{msg}\n")

    def _parse_content(self, ip: str) -> str:
        content_length = int(self.headers['Content-Length'])
        raw = self.rfile.read(content_length).decode('utf-8')
        try:
            data = json.loads(raw)
            self._write_log(ip, raw)
            name        = data.get("name", "UNKNOWN")
            description = data.get("description", "UNKNOWN")
            event_type  = data.get("event_type", "UNKNOWN")
            origin      = data.get("origin", "UNKNOWN")
            #timestamp   = data.get("timestamp", "UNKNOWN")
            level       = data.get("level", "UNKNOWN")
            return f"{ip} {level:6}{event_type:6} {origin}/{name}: {description}"
        except json.decoder.JSONDecodeError:
            return f"{ip} {raw}"

    def do_POST(self):
        logger.info(self._parse_content(self.client_address[0]))
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def log_message(self, format, *args):
        return # Do nothing here as we have our own logging.
    
def run(server_class=HTTPServer, handler_class=S, port=8088):
    if platform.system() == 'Linux':  # If Ubuntu where we have syslog also use it.
        logger.addHandler(SysLogHandler(facility=SysLogHandler.LOG_DAEMON, address='/dev/log'))

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter("%(levelname).1s %(asctime)s %(message)s") )
    logger.addHandler(handler)
    
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    logger.info('build_logs_server started')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    logger.info('build_logs_server stopped')

if __name__ == '__main__':
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
