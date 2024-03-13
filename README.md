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

# Docker

## Introduction
Docker is a platform for developing, shipping, and running applications inside containers. Containers allow developers to package up an application with all its dependencies and ship it out as a single unit. This ensures that the application will run on any environment that supports Docker, regardless of differences in infrastructure.

## Installation
To install Docker, follow these steps:
1. Visit the official Docker website: [https://docs.docker.com/get-docker/](https://docs.docker.com/get-docker/)
2. Choose the appropriate installation method for your operating system (e.g., Docker Desktop for Windows or macOS, Docker Engine for Linux).
3. Follow the installation instructions provided on the website.

## Docker Usage
Once Docker is installed, you can start using it to manage containers.

### Building Docker Image
To build a Docker image from the provided Dockerfile:
1. Navigate to the directory containing the Dockerfile.
2. Open a terminal or command prompt.
3. Run the following command:
   ```bash
   docker build -t oscap-scanner .
   ```
   This command builds a Docker image named `oscap-scanner` from the Dockerfile in the current directory.

### Running Docker Container
To run a Docker container interactively using the built image:
1. Open a terminal or command prompt.
2. Run the following command:
   ```bash
   docker run -it --name oscap-scanner-container oscap-scanner
   ```
   This command starts a new Docker container named `oscap-scanner-container` from the `oscap-scanner` image. The container runs an interactive shell.

### Notes
- Make sure Docker is running before executing any Docker commands.
- Replace `oscap-scanner` with the appropriate image name if you chose a different name during the image build process.
- Additional Docker commands and options can be found in the Docker documentation: [https://docs.docker.com/](https://docs.docker.com/).
