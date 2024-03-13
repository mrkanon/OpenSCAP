import os
import subprocess
import datetime
from lxml import etree
import argparse
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)
stream_handler = logging.StreamHandler()
formatter = logging.Formatter('%(message)s') 
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)

class OpenSCAPScanner:
    def __init__(self, output_dir):
        self.output_dir = output_dir

    def run_scan(self, verbose=False):
        scap_profile = "xccdf_org.ssgproject.content_profile_stig"
        name = f"openscap_scan_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}"
        result_path = os.path.join(self.output_dir, name+".xml")
        os.makedirs(self.output_dir, exist_ok=True)
        scan_command = [
            "oscap", "xccdf", "eval",
            "--profile", scap_profile,
            "--results", result_path,
            "--cpe", "/usr/share/xml/scap/ssg/content/ssg-ol8-cpe-dictionary.xml",
            "/usr/share/xml/scap/ssg/content/ssg-ol8-xccdf.xml"
        ]
        if verbose:
            logger.setLevel(logging.DEBUG)

        logger.info("Running scan...")
        subprocess.run(scan_command, capture_output=not verbose)
        return result_path

class OpenSCAPAnalyzer:
    def __init__(self, output_dir):
        self.output_dir = output_dir

    def parse_xml(self, file_path):
        if not os.path.isfile(file_path):
            raise FileNotFoundError(f"The file {file_path} not found.")
        tree = etree.parse(file_path)
        root = tree.getroot()
        return root

    def summary_scan(self,scan_root,scan_file):
        file_name = scan_file.split("/")[-1]
        passed = 0
        failed = 0
        total = 0

        for rule in scan_root.iter("{*}rule-result"):
            scan_result = rule.find("{*}result").text
            if scan_result == "fail":
                failed += 1
            elif scan_result == "pass":
                passed += 1
            total += 1
        logger.info(f"\nSummary of {file_name} | Pass {passed} | Fail {failed} | Total {total}")

    def compare_scans(self, scan1_file, scan2_file):
        scan1_root = self.parse_xml(scan1_file)
        scan2_root = self.parse_xml(scan2_file)
        namespace1 = scan1_root.tag.split('}')[0] + '}'
        namespace2 = scan1_root.tag.split('}')[0] + '}'
        if namespace1 == namespace2:
            differences = 0
            fixed = 0
            fail = 0
            new_rule = 0
            for rule in scan1_root.iter(f"{namespace1}rule-result"):
                rule_idref = rule.get("idref")
                scan1_result = rule.find(f"{namespace1}result").text
                scan2_result = scan2_root.find(f".//{namespace2}rule-result[@idref='{rule_idref}']/{namespace2}result").text
                if scan1_result != scan2_result:
                    differences += 1
                    if scan1_result == "fail" & scan2_result == "pass":
                        fixed +=1
                        print(f"The rule {rule_idref} that failed in the first scan was corrected in the second scan.")
                    if scan1_result == "pass" & scan2_result == "fail":
                        fail += 1
                        print(f"The rule {rule_idref} failed in the second scan.")
                    if (scan1_result == "notselected" or scan1_result == "notapplicable") and (scan2_result == "pass" or scan2_result == "fail"):
                        new_rule += 1
                        print(f"The rule {rule_idref} was added in the second scan with the status: {scan2_result} .")
            logger.info(f"\nTotal differences found: {differences} | Fixed {fixed} | Fail {fail} | New {new_rule}")
            self.summary_scan(scan1_root,scan1_file)
            self.summary_scan(scan2_root,scan2_file)
        else:
            logger.warning("The scans don´t match.")

def run_scan(scanner, verbose=False):
    scan_path = scanner.run_scan(verbose)
    logger.info(f"Scan completed. Results saved in: {scan_path}")

def list_scans(output_dir):
    if not os.path.exists(output_dir):
        logger.error(f"Directory {output_dir} does not exist.")
        return
    files = os.listdir(output_dir)
    logger.info("Previous scans:")
    for file in files:
        logger.info(file)

def print_scan(output_dir, file_name):
    file_path = os.path.join(output_dir, file_name)
    if not os.path.exists(file_path):
        logger.error(f"File {file_name} not found in {output_dir}.")
        return
    try:
        command = ["vi", os.path.join(output_dir, file_name)]
        subprocess.run(command)
    except FileNotFoundError:
        logger.error("File not found.")

def compare_scans(analyzer, output_dir, scan1_file, scan2_file):
    try:
        analyzer.compare_scans(os.path.join(output_dir, scan1_file), os.path.join(output_dir, scan2_file))
    except FileNotFoundError:
        logger.error("File not found.")

def exit_program():
    logger.info("Exiting the program.")
    exit()
    
def main():
    parser = argparse.ArgumentParser(
            prog='OpenSCAP Scaner Tool',
            description='This is a tool to run, compare, print and list oscap test with the profile stig.')
    parser.add_argument('--output-dir', default="/var/log/openscap", help='Output directory for scan results')
    parser.add_argument('--run-scan', action='store_true', help='Run a new scan')
    parser.add_argument('--list-scans', action='store_true', help='List previous scans')
    parser.add_argument('--print-scan', metavar='FILE', help='Print a specific scan')
    parser.add_argument('--compare-scans', metavar=('FILE1', 'FILE2'), nargs=2, help='Compare two previous scans')
    parser.add_argument('--verbose', action='store_true', help='Verbose mode')
    args = parser.parse_args()
    output_dir = args.output_dir
    scanner = OpenSCAPScanner(output_dir)
    analyzer = OpenSCAPAnalyzer(output_dir)
    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)
    if args.run_scan:
        run_scan(scanner,args.verbose)
    elif args.list_scans:
        list_scans(output_dir)
    elif args.print_scan:
        print_scan(output_dir, args.print_scan)
    elif args.compare_scans:
        compare_scans(analyzer, output_dir, args.compare_scans[0], args.compare_scans[1])

if __name__ == "__main__":
    main()

