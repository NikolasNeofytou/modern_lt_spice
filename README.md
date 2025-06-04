# modern_lt_spice

This repository contains a very early prototype of a modernised interface to LTspice using a web based workflow.

## Usage

1. Install dependencies (ngspice, Python packages):
   ```bash
   pip install Flask PySpice
   ```
   On Linux use apt to install ngspice:
   ```bash
   sudo apt-get update && sudo apt-get install -y ngspice libngspice0
   ```
   set the environment variable `NGSPICE_EXECUTABLE` to the full path to
   the binary. Example:
   ```bash
   # Linux / macOS
   export NGSPICE_EXECUTABLE=/opt/ngspice/bin/ngspice
   # Windows command prompt
   set "NGSPICE_EXECUTABLE=C:\Spice\bin\ngspice.exe"
   ```
   ```bash
   brew install ngspice
   ```
   On Windows download the pre-built installer from the
   [ngspice website](http://ngspice.sourceforge.net/) and add the install
   directory (e.g. `C:\Spice\bin`) to your `PATH`.
   If `ngspice` is installed in a non-standard location you can
   set the environment variable `NGSPICE_EXECUTABLE` to the full path
   to the binary.

2. Start the development server:
   ```bash
   python webapp/app.py
   ```
3. Open `http://localhost:5000` in a browser. Enter a SPICE netlist and run the simulation to visualise voltages.
