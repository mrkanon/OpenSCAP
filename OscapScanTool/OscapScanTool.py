import subprocess
import os
import datetime
from lxml import etree
import xml.dom.minidom

class OpenSCAPScanner:
    def __init__(self, output_dir):
        self.output_dir = output_dir
    
    def run_scan(self):
        scap_profile = "xccdf_org.ssgproject.content_profile_stig"
        name = f"openscap_scan_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}"
        report_path = os.path.join(self.output_dir, name+".html")
        result_path = os.path.join(self.output_dir, name+".xml")

        os.makedirs(self.output_dir, exist_ok=True)

        scan_command = [
            "oscap", "xccdf", "eval",
            "--profile", scap_profile,
            "--results", result_path,
            "--report", report_path,
            "--oval-results",
            "--cpe", "/usr/share/xml/scap/ssg/content/ssg-ol8-cpe-dictionary.xml",
            "/usr/share/xml/scap/ssg/content/ssg-ol8-xccdf.xml"
        ]
        subprocess.run(scan_command)

        return report_path

class OpenSCAPAnalyzer:
    def __init__(self, output_dir):
        self.output_dir = output_dir
    
    def parse_xml(self, file_path):
        tree = etree.parse(file_path)
        root = tree.getroot()
        return root

    def summary_scan(self,scan_file):
        scan_root = self.parse_xml(scan_file)
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
        print(f"\nEstadisticas de {scan_file} | Pass {passed} | Fail {failed} | Total {total}")
    
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
                        print(f"La Regla {rule_idref} que fallo en el primer escaneo fue corregida en el segundo escaneo.")
                    if scan1_result == "pass" & scan2_result == "fail":
                        fail += 1
                        print(f"La Regla {rule_idref} fallo en el segundo escaneo.")
                    if (scan1_result == "notselected" | scan1_result == "notapplicable") & (scan2_result == "pass" | scan2_result == "fail"):
                        new_rule += 1
                        print(f"La Regla {rule_idref} se agrego en el segundo escaneo con el estatus: {scan2_result} .")
            print(f"\nTotal de diferencias encontradas: {differences} | Solucionadas {fixed} | Fallaron {fail} | Nuevas {new_rule}")
            self.summary_scan(scan1_file)
            self.summary_scan(scan2_file)
        else:
            print("Los escaneos no coinciden.")

def run_scan(scanner):
    scan_path = scanner.run_scan()
    print(f"Escaneo completado. Resultados guardados en: {scan_path}")

def list_scans(output_dir):
    files = os.listdir(output_dir)
    print("Escaneos anteriores:")
    for file in files:
        print(file)

def print_scan(output_dir):
    file_name = input("Ingrese el nombre del archivo de escaneo a imprimir: ")
    try:
        with open(os.path.join(output_dir, file_name), "r") as file:
            xml_string = file.read()
            dom = xml.dom.minidom.parseString(xml_string)
            pretty_xml = dom.toprettyxml()
            print(pretty_xml)
    except FileNotFoundError:
        print("Archivo no encontrado.")

def compare_scans(analyzer, output_dir):
    scan1_file = input("Ingrese el nombre del primer archivo de escaneo: ")
    scan2_file = input("Ingrese el nombre del segundo archivo de escaneo: ")
    try:
        analyzer.compare_scans(os.path.join(output_dir, scan1_file), os.path.join(output_dir, scan2_file))
    except FileNotFoundError:
        print("Archivo no encontrado.")

def exit_program():
    print("Saliendo del programa.")
    exit()
    
def main():
    output_dir = "/var/log/openscap"
    scanner = OpenSCAPScanner(output_dir)
    analyzer = OpenSCAPAnalyzer(output_dir)

    actions = {
        "1": lambda: run_scan(scanner),
        "2": lambda: list_scans(output_dir),
        "3": lambda: print_scan(output_dir),
        "4": lambda: compare_scans(analyzer, output_dir),
        "5": lambda: exit_program()
    }

    while True:
        print("\nMenu:")
        print("1. Ejecutar un escaneo")
        print("2. Listar escaneos anteriores")
        print("3. Imprimir un escaneo especifico anterior")
        print("4. Comparar dos escaneos anteriores")
        print("5. Salir")

        choice = input("Seleccione una opcion: ")

        if choice in actions:
            actions[choice]()
        else:
            print("Opcion no valida. Por favor, seleccione una opcion valida.")

if __name__ == "__main__":
    main()

