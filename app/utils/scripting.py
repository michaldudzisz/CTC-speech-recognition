import subprocess
import sys

def run_sricpt(script, logs = None):
    if logs == None:
        process = subprocess.Popen(script, stdout=subprocess.PIPE)
        for line in iter(process.stdout.readline, b''):
            sys.stdout.write(line.decode(sys.stdout.encoding))
    else:
        with open(logs, 'wb') as f: 
            process = subprocess.Popen(script, stdout=subprocess.PIPE)
            for line in iter(process.stdout.readline, b''):
                sys.stdout.write(line.decode(sys.stdout.encoding))
                f.write(line)

