from flask import Flask, render_template, request
import tempfile
import subprocess
import os
import json

app = Flask(__name__)

# Path to ngspice executable can be customised via environment variable
NGSPICE_CMD = os.environ.get('NGSPICE_EXECUTABLE', 'ngspice')

# Default example circuit
DEFAULT_NETLIST = """* Simple RC circuit\nV1 input 0 PULSE(0 5 0 0 0 10m 20m)\nR1 input output 1k\nC1 output 0 1u\n.tran 1m 20m\n.print tran v(input) v(output)\n.end"""

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        netlist = request.form.get('netlist', '')
        try:
            data = run_ngspice(netlist)
            return render_template('index.html', netlist=netlist,
                                   data=json.dumps(data), error=None)
        except FileNotFoundError:

            err = 'ngspice binary not found. Ensure it is installed and in your PATH.'

            return render_template('index.html', netlist=netlist, data=None, error=err)
        except subprocess.CalledProcessError as e:
            err = 'ngspice error: ' + (e.stderr or e.stdout)
            return render_template('index.html', netlist=netlist, data=None, error=err)
    return render_template('index.html', netlist=DEFAULT_NETLIST, data=None, error=None)

def run_ngspice(netlist_text):
    """Run ngspice in batch ascii mode and parse output."""
    with tempfile.TemporaryDirectory() as tmpdir:
        circuit_path = os.path.join(tmpdir, 'circuit.cir')
        with open(circuit_path, 'w') as f:
            f.write(netlist_text)

        output = subprocess.run(['ngspice', '-b', '-a', circuit_path],

                                capture_output=True, text=True, check=True)
        lines = output.stdout.splitlines()
        # Data starts after header. We'll collect numeric rows with at least 4 columns
        data = []
        for line in lines:
            parts = line.strip().split()
            if len(parts) >= 3 and all(p.replace('.', '').replace('e', '').replace('-', '').isdigit() for p in parts[1:]):
                try:
                    idx = int(parts[0])
                    time_val = float(parts[1])
                    values = list(map(float, parts[2:]))
                    data.append([time_val] + values)
                except ValueError:
                    continue
        return data

if __name__ == '__main__':
    app.run(debug=True)
