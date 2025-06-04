# modern_lt_spice

This repository contains a very early prototype of a modernised interface to LTspice using a web based workflow.  
It now also includes a small command-line simulator implemented from scratch in pure Python.

## Usage

1. Install dependencies (ngspice, Python packages):
   ```bash
   pip install Flask PySpice
   ```
   On Linux use apt to install ngspice:
   ```bash
   sudo apt-get update && sudo apt-get install -y ngspice libngspice0
   ```
   On macOS you can use Homebrew:
   ```bash
   brew install ngspice
   ```
   On Windows download the pre-built installer from the
   [ngspice website](http://ngspice.sourceforge.net/) and add the install
   directory (e.g. `C:\Spice\bin`) to your `PATH`.
   If `ngspice` is installed in a non-standard location you can
   set the environment variable `NGSPICE_EXECUTABLE` to the full path to
   the binary. Example:
   ```bash
   # Linux / macOS
   export NGSPICE_EXECUTABLE=/opt/ngspice/bin/ngspice
   # Windows command prompt
   set "NGSPICE_EXECUTABLE=C:\Spice\bin\ngspice.exe"
   ```
   You can verify the executable is visible to Python with:
   ```bash
   python -c "import shutil, os; print(shutil.which(os.environ.get('NGSPICE_EXECUTABLE', 'ngspice')))">
   ```
   If the above command prints nothing, your path is incorrect or `ngspice` is not installed.
2. Start the development server:
   ```bash
   python webapp/app.py
   ```
3. Open `http://localhost:5000` in a browser. Components can be dragged or simply clicked in the palette to add them to the canvas. Connect terminals by dragging between the small dots that appear. Values can be edited inline and the SPICE netlist updates automatically.
   The interface now runs the simulation in the background every few seconds and
   shows an error message if the circuit fails to solve. Repeated errors will
   trigger a popup so you can spot logic problems quickly. Press **Run
   Simulation** at any time to refresh the graph manually.

## Command-line simulator

For quick experiments you can run the standalone Python simulator that parses a minimal netlist format and solves the circuit using modified nodal analysis.

```bash
python simulator.py example.cir
```

Where `example.cir` contains lines such as:

```
V1 1 0 5
R1 1 2 1k
R2 2 0 2k
.op
```

The script prints node voltages and currents through voltage sources.
