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

---

# Running OscapScanTool with Python 3.11 and venv

## Prerequisites

- Python 3.11 installed on your system.
- Access to the terminal or command line.

## Setting Up the Virtual Environment

1. Open a terminal.
2. Navigate to the folder where the OscapScanTool.py file is located.

```bash
cd path_to_your_folder/sandbox
```

3. Create a new virtual environment using Python 3.11. You can do this with the following command:

```bash
python3.11 -m venv myenv
```

4. Activate the virtual environment:

On Linux/macOS:

```bash
source myenv/bin/activate
```

On Windows:

```bash
myenv\Scripts\activate
```

## Installing Dependencies

Once the virtual environment is activated, install the necessary dependencies using pip:

```bash
pip install -r requirements.txt
```

## Running the Program

After installing the dependencies, you can run the Python program using the following command:

```bash
python3.11 OscapScanTool.py [arguments]
```

Make sure to replace `[arguments]` with the specific options you want to use, such as `--run-scan`, `--list-scans`, `--print-scan`, `--compare-scans`, or `--verbose`, as defined in the program.

## Deactivating the Virtual Environment

When you're finished using the program, you can deactivate the virtual environment by typing the following command in the terminal:

```bash
deactivate
```

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
