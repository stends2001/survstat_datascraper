from .dirs import directories_dict
from datetime import datetime
import os
import re

log_file_path = directories_dict['project_root'] / "log.txt"

def log_script_run(disease_dict, years, log_file_path=log_file_path, append_mode=False):
    """
    Logs script execution with disease information.
    
    Parameters:
    ----------
    disease_dict : dict
        Dictionary mapping disease names to slugs
    years : list or range
        Years being processed
    log_file_path : Path, optional
        Path to log file
    append_mode : bool, optional
        If True, merges new diseases with existing ones from log file.
        If False, overwrites the entire log file (default behavior).
    """
    run_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    if append_mode:
        # Read existing diseases from log file
        existing_diseases = read_log(log_file_path)
        # Merge with new diseases (new diseases take precedence)
        merged_diseases = {**existing_diseases, **disease_dict}
        disease_dict = merged_diseases
        print(f"📝 Appending {len(disease_dict) - len(existing_diseases)} new diseases to existing {len(existing_diseases)} diseases")

    log_entries = [
        f"\n--- Script Run: {run_time} ---",
        f"Years: {min(years)}–{max(years)}",
        f"Total years: {len(years)}",
        "Diseases:"
    ]

    for name, slug in disease_dict.items():
        log_entries.append(f"- {name}: {slug}")

    log_entries.append("--------------------------------\n")

    with open(log_file_path, "w", encoding="utf-8") as log_file:
        log_file.write("\n".join(log_entries))



def read_log(log_file_path=log_file_path):
    print(log_file_path)

    if not os.path.exists(log_file_path):
        print("No log file found.")
        return {}

    disease_dict = {}
    last_run_time = None
    in_disease_section = False

    with open(log_file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()   

    # Reverse iterate over lines to find the latest run block
    for i in range(len(lines) - 1, -1, -1):
        line = lines[i].strip()

        # Start of the last run block
        if line.startswith("--- Script Run:"):
            # Extract timestamp
            ts_match = re.search(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}", line)
            if ts_match:
                last_run_time = datetime.strptime(ts_match.group(), "%Y-%m-%d %H:%M:%S")
            # We can stop searching here since we've found the latest run
            break

    # From the found run start line, move forward to collect diseases
    # Find index of run start line
    run_start_idx = None
    for idx, line in enumerate(lines):
        if line.strip().startswith("--- Script Run:"):
            # Check if this line matches the last_run_time we found
            ts_match = re.search(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}", line)
            if ts_match and datetime.strptime(ts_match.group(), "%Y-%m-%d %H:%M:%S") == last_run_time:
                run_start_idx = idx
                break

    if run_start_idx is None:
        print("Could not find the start of the last run block in the log.")
        return {}

    # Parse diseases starting after 'Diseases:' line until separator '---'
    in_disease_section = False
    for line in lines[run_start_idx:]:
        line = line.strip()
        if line == "Diseases:":
            in_disease_section = True
            continue
        if in_disease_section:
            if line.startswith("-"):
                # Parse disease line like '- Measles: measles'
                try:
                    name, slug = line[1:].split(":", 1)
                    disease_dict[name.strip()] = slug.strip()
                except ValueError:
                    pass
            elif line.startswith("---") or line == "--------------------------------":
                # End of disease section
                break

    # Print time since last run
    if last_run_time:
        delta = datetime.now() - last_run_time
        days = delta.days
        hours = delta.seconds // 3600
        minutes = (delta.seconds % 3600) // 60

        if days > 0:
            print(f"Last script run: {days} day(s) ago")
        elif hours > 0:
            print(f"Last script run: {hours} hour(s) ago")
        elif minutes > 0:
            print(f"Last script run: {minutes} minute(s) ago")
        else:
            print("Last script run: just now")
    else:
        print("No valid last run timestamp found.")

    return disease_dict

def add_diseases_to_log(new_diseases, log_file_path=log_file_path):
    """
    Convenience function to add new diseases to the existing log.
    
    Parameters:
    ----------
    new_diseases : dict
        Dictionary of new diseases to add {name: slug}
    log_file_path : Path, optional
        Path to log file
        
    Returns:
    -------
    dict
        Updated disease dictionary with all diseases (existing + new)
    """
    existing_diseases = read_log(log_file_path)
    merged_diseases = {**existing_diseases, **new_diseases}
    
    # Create a temporary years list for logging
    current_year = datetime.now().year
    all_years = range(2001, current_year + 1)
    
    # Log with append mode
    log_script_run(merged_diseases, all_years, log_file_path, append_mode=True)
    
    return merged_diseases