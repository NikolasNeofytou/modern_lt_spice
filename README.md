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
3. Open `http://localhost:5000` in a browser. Drag components from the palette onto the canvas and connect their terminals. Each component shows an inline field for the numeric value and a drop-down for the prefix. The displayed SPICE netlist updates automatically as you edit and the waveforms are plotted when you press **Run Simulation**.
