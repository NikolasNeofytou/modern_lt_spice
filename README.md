# modern_lt_spice

This repository contains a very early prototype of a modernised interface to LTspice using a web based workflow.

## Usage

1. Install dependencies (ngspice, Python packages):
   ```bash
   pip install Flask PySpice
   sudo apt-get update && sudo apt-get install -y ngspice libngspice0
   ```
2. Start the development server:
   ```bash
   python webapp/app.py
   ```
3. Open `http://localhost:5000` in a browser. Enter a SPICE netlist and run the simulation to visualise voltages.
