#!/usr/bin/env python3
import os
import sys
import subprocess

def run_worlds_collide_loop(num_iterations=10):
    """Run WorldsCollide multiple times with incrementing output filenames"""
    print(f"Running WorldsCollide {num_iterations} times...")
    
    # Save current directory - we're already in WorldsCollide directory
    original_dir = os.getcwd()
    wc_dir = original_dir  # We're already in the right directory
    
    # Clean up seeds directory before starting
    seeds_dir = os.path.join(wc_dir, "seeds")
    if os.path.exists(seeds_dir):
        print("Cleaning up previous seed files...")
        import glob
        # Remove all .smc and .txt files from seeds directory
        for file_pattern in ["*.smc", "*.txt"]:
            for file_path in glob.glob(os.path.join(seeds_dir, file_pattern)):
                try:
                    os.remove(file_path)
                    print(f"  Removed: {os.path.basename(file_path)}")
                except OSError as e:
                    print(f"  Warning: Could not remove {file_path}: {e}")
    else:
        # Create seeds directory if it doesn't exist
        print("Creating seeds directory...")
        os.makedirs(seeds_dir)
    
    for iteration in range(1, num_iterations + 1):
        print(f"Running iteration {iteration}/{num_iterations}...")
        
        # Change to WorldsCollide directory
        os.chdir(wc_dir)
        
        # Build the command with relative paths from WorldsCollide directory
        output_path = os.path.join("seeds", f"preset_pootsleague_tunes_{iteration}.smc")
        cmd = [
            sys.executable, "wc.py",
            "-i", "ffiii.smc",
            "-o", output_path,
            "-cg",
            "-oa", "2.2.2.2.6.6.4.9.9",
            "-ob", "3.1.1.10.20.20",
            "-oc", "30.8.8.1.1.11.8",
            "-od", "59.1.1.11.31",
            "-oe", "62.1.1.11.44",
            "-of", "26.8.8.1.1.11.26",
            "-og", "28.10.10.1.1.11.13",
            "-oh", "9.1.1.11.19",
            "-oi", "31.10.10.1.1.11.3",
            "-oj", "8.1.1.11.0",
            "-ok", "14.1.1.11.57",
            "-ol", "16.1.1.11.59",
            "-om", "27.8.8.1.1.11.40",
            "-on", "7.1.1.11.40",
            "-oo", "48.10.10.1.1.2.9.9",
            "-op", "45.10.10.1.1.4.12.12",
            "-oq", "29.125.125.1.1.11.10",
            "-or", "37.1.1.11.48",
            "-os", "38.1.1.12.7",
            "-ot", "36.1.1.6.3.3",
            "-ou", "37.1.1.3.11",
            "-sc1", "celes",
            "-sc2", "random",
            "-sc3", "random",
            "-sal",
            "-eu",
            "-csrp", "80", "125",
            "-fst",
            "-brl",
            "-slr", "4", "5",
            "-lmprp", "75", "125",
            "-lel",
            "-srr", "25", "35",
            "-rnl",
            "-rnc",
            "-sdr", "1", "3",
            "-das",
            "-dda",
            "-dns",
            "-sca",
            "-scis",
            "-com", "98989898989898989898989898",
            "-rec1", "28",
            "-rec2", "97",
            "-rec3", "5",
            "-xpm", "3",
            "-mpm", "5",
            "-gpm", "5",
            "-nxppd",
            "-lsced", "2",
            "-hmced", "2",
            "-xgced", "2",
            "-ase", "2",
            "-msl", "40",
            "-sed",
            "-bbs",
            "-bmkl",
            "-drloc", "shuffle",
            "-stloc", "mix",
            "-be",
            "-bnu",
            "-res",
            "-fer", "0",
            "-escr", "100",
            "-dgne",
            "-wnz",
            "-mmnu",
            "-cmd",
            "-esr", "2", "5",
            "-elr",
            "-ebr", "82",
            "-emprp", "75", "125",
            "-emi",
            "-nm1", "random",
            "-rnl1",
            "-rns1",
            "-nm2", "random",
            "-rnl2",
            "-rns2",
            "-nmmi",
            "-mmprp", "75", "125",
            "-gp", "5000",
            "-smc", "3",
            "-sws", "10",
            "-sfd", "10",
            "-sto", "3",
            "-idm", "3",
            "-ieor", "33",
            "-ieror", "33",
            "-ir", "9,26,27,28,82,96,148,156,162,209,211,228",
            "-csb", "5", "12",
            "-mca",
            "-stra",
            "-saw",
            "-sisr", "30",
            "-sprp", "75", "125",
            "-sdm", "5",
            "-npi",
            "-sebr",
            "-snsb",
            "-ccsr", "30",
            "-chrm", "0", "0",
            "-cms",
            "-cspp", "2.1.4.4.0.0.0.3.3.4.5.3.3.5.1.0.6.1.0.3",
            "-frw",
            "-wmhc",
            "-cor", "100",
            "-crr", "100",
            "-crvr", "125", "150",
            "-crm",
            "-ari",
            "-anca",
            "-adeh",
            "-ame", "1",
            "-nmc",
            "-noshoes",
            "-nu",
            "-nfps",
            "-fs",
            "-fe",
            "-fvd",
            "-fr",
            "-fj",
            "-fbs",
            "-fedc",
            "-fc",
            "-ond",
            "-etn",
            "-bps",
            "-ew"
        ]
        
        try:
            subprocess.run(cmd, check=True, capture_output=True, text=True)
            print(f"Iteration {iteration} completed successfully")
        except subprocess.CalledProcessError as e:
            print(f"Error in iteration {iteration}: {e}")
            print(f"Command output: {e.stdout}")
            print(f"Command error: {e.stderr}")
            print("Stopping due to error.")
            os.chdir(original_dir)
            return
    
    # Return to original directory when loop completes normally
    os.chdir(original_dir)

def main():
    print("Starting WorldsCollide batch processing...")
    
    # Check for command line argument first, then ask user
    import sys
    if len(sys.argv) > 1:
        try:
            num_iterations = int(sys.argv[1])
        except ValueError:
            num_iterations = 10
    else:
        try:
            num_iterations = int(input("How many WorldsCollide iterations do you want to run? (default: 10): ") or "10")
        except (ValueError, EOFError):
            num_iterations = 10
    
    # Run WorldsCollide multiple times
    run_worlds_collide_loop(num_iterations)
    
    print("Batch processing complete!")

if __name__ == "__main__":
    main()