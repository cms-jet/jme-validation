#!/usr/bin/env python
"""
DBS 3 Client Example.   This script is called

python GetDasInfo.py '/*/*Fall13-POST*/GEN-SIM'

"""
import subprocess, argparse

def run_dasgoclient(dataset, output_file, user):
    """
    Runs the dasgoclient command with the given dataset name,
    and saves the output to the specified file.
    """
    if not user:
        cmd = f"dasgoclient --query 'file dataset={dataset}'"
    else:
        cmd = f"dasgoclient --query 'instance=prod/phys03 file dataset={dataset}'"
    output = subprocess.check_output(cmd, shell=True)
    with open(output_file, "w") as f:
        decoded_output = output.decode()
        decoded_output = decoded_output.rstrip(decoded_output[-1])
        preprocessed_output = "root://cms-xrd-global.cern.ch/" + decoded_output.replace('\n', '\nroot://cms-xrd-global.cern.ch/')
        f.write("# "+dataset+'\n')
        f.write(preprocessed_output)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Runs dasgoclient with the given dataset name and saves the output to a file.")
    parser.add_argument("dataset", help="the name of the dataset")
    parser.add_argument("output_file", help="the name of the output file")
    parser.add_argument('--user', default=False, action='store_true', help='query for a dataset published by a user in prod/phys03')
    args = parser.parse_args()
    
    run_dasgoclient(args.dataset, args.output_file, args.user)
    print(f"Output saved to {args.output_file}.")
