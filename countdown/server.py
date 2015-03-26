from http.server import BaseHTTPRequestHandler, HTTPServer
from io import StringIO
from random import choice
import re
import sys
from threading import current_thread, Thread
from time import sleep

from consoleplay import LettersRoundGame

ESC = chr(27)
END = ESC + '[END'
CTDN = ESC + '[CTDN'
ORIG_OUT = sys.stdout
THREADS = {}
KEYSAFE = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ-_+`~!#$%^&*()'

def random_key(length):
    return ''.join((choice(KEYSAFE) for i in range(length)))

class GameThread:
    def __init__(self, thread):
        self.input_buffer = []
        self.output_buffer = []
        self.thread = thread
        self.wait = False
        
    def flush_output(self):
        ret = ''.join(self.output_buffer)
        self.output_buffer = []
        
        return ret

class CustomIO(StringIO):
    def write(self, s):
        tname = current_thread().name
        thread = THREADS[tname]
        
        thread.wait = True
        
        if not s.startswith('\r'):
            thread.output_buffer.append(s)

        return len(s)

    def readline(self, size=-1):
        tname = current_thread().name
        thread = THREADS[tname]
        thread.wait = False
        
        while not thread.input_buffer and thread.thread.is_alive():
            sleep(0.5)
            
        if not thread.thread.is_alive():
            del THREADS[tname]
            
        return thread.input_buffer.pop()

class ReuseAddressServer(HTTPServer):
    allow_reuse_address = True

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        game = LettersRoundGame(round_time=5)
        thread = Thread(target=game.play)
        key = random_key(16)
        while key in THREADS:
            key = random_key(16)

        thread.name = key
        THREADS[key] = GameThread(thread)
        thread.start()

        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

        self.write_game_output(key, key)

    def do_POST(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        response = self.rfile.read(int(self.headers['content-length'])).decode()
        split = response.split('\n')
        assert split[0].startswith('key=')
        key = split[0][4:]

        thread = THREADS[key]
        thread.wait = True
        thread.input_buffer.append('\n'.join(split[1:]))
        self.write_game_output(key)

    def write_game_output(self, threadname, key=None):
        # Wait for sys.stdout.output to be filled and ready 
        # (i.e. wait for game thread to ask for input, or thread to finish)
        gamethread = THREADS[threadname]
        pattern = r'\|(?: [A-Z] ){9}\|\n?'
        do_countdown = False

        while (not do_countdown) and gamethread.wait and gamethread.thread.is_alive():
            for s in gamethread.output_buffer:
                if re.search(pattern, s):
                    do_countdown = True

        # Write to wfile and clear output
        if key:
            self.wfile.write('key={}\n'.format(key).encode())
            
        if do_countdown:
            for s in gamethread.output_buffer:
                if s.startswith('You have'):
                    break

                self.wfile.write(s.encode())
            
            self.wfile.write((CTDN + '\n').encode())
            gamethread.flush_output()
        else:
            self.wfile.write(gamethread.flush_output().encode())
        
        if not gamethread.thread.is_alive():
            self.wfile.write(END.encode())
            del THREADS[threadname]

##############################################################################
if __name__ == '__main__':
    cio = CustomIO()
    sys.stdout = cio
    sys.stdin = cio
    host, port = 'localhost', 8005
    server = ReuseAddressServer((host, port), Handler)

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass

