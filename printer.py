import sys
import subprocess

def print_file(file_path, copies, color_option):
    printer_name = "HP_DeskJet_2300_series"  # Get this using `lpstat -p`
    
    color_mode = "Color" if color_option == "color" else "Grayscale"
    
    for _ in range(int(copies)):
        subprocess.run(["lp", "-d", printer_name, "-o", f"ColorModel={color_mode}", file_path])

if __name__ == "__main__":
    file_path = sys.argv[1]
    copies = sys.argv[2]
    color_option = sys.argv[3]
    
    print_file(file_path, copies, color_option)
