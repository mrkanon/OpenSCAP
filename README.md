# OpenSCAPTool
This is a tool to run, compare, print, and list OpenSCAP tests with the STIG profile.
## Usage
```bash 
python3 OscapScanTool.py [--output-dir OUTPUT_DIR] [--run-scan] [--list-scans] [--print-scan FILE] [--compare-scans FILE1 FILE2] 
```
## Options
+ --output-dir OUTPUT_DIR: Specifies the output directory for scan results. Default is /var/log/openscap.
+ --run-scan: Run a new scan.
+ --list-scans: List previous scans.
+ --print-scan FILE: Print a specific scan.
+ --compare-scans FILE1 FILE2: Compare two previous scans.
## Examples
1. Run a scan:
```bash
python3 OscapScanTool.py --run-scan
```
2. List previous scans:
```bash
python3 OscapScanTool.py --list-scans
```
3. Print a specific scan:
```bash
python3 OscapScanTool.py --print-scan FILE
```
4. Compare two previous scans:
```bash
python3 OscapScanTool.py --compare-scans FILE1 FILE2
```
## Notes
+ Before running the tool, ensure that the required OpenSCAP tools are installed and accessible in the system environment.
+ Make sure to provide valid file names and directories when using the tool to avoid errors.
