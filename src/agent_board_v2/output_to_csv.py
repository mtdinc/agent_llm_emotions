import os
import csv
import re

def parse_filename(filename):
    """Parses the output filename to extract relevant information."""
    pattern = r"result_team(\d+)_case(\d+)_stage(\d+)_([^_]+)_(.+)\.md"
    match = re.match(pattern, filename)
    if match:
        return {
            "team": match.group(1),
            "case": match.group(2),
            "stage": match.group(3),
            "provider": match.group(4),
            "model": match.group(5),
        }
    return None

def read_markdown_file(filepath):
    """Reads the content of a markdown file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"Error reading file {filepath}: {e}")
        return None

def load_true_diagnoses(csv_filepath):
    """Loads true diagnoses from case_list.csv into a dictionary."""
    true_diagnoses = {}
    try:
        with open(csv_filepath, 'r', encoding='utf-8-sig') as csvfile:
            csv_reader = csv.DictReader(csvfile)
            for row in csv_reader:
                case_id = row['case_id']
                true_diagnosis = row['true_tx']
                true_diagnoses[case_id] = true_diagnosis
    except Exception as e:
        print(f"Error reading {csv_filepath}: {e}")
    return true_diagnoses

def create_output_csv():
    """Generates a CSV file summarizing the output files, including true diagnoses."""
    output_dir = "output"
    csv_filepath = os.path.join(output_dir, "output_summary.csv")
    output_files = [f for f in os.listdir(output_dir) if f.startswith("result_team") and f.endswith(".md")]
    cases_csv_filepath = "cases/case_list.csv"
    true_diagnosis_map = load_true_diagnoses(cases_csv_filepath)

    with open(csv_filepath, 'w', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(["Team", "Case", "Stage", "Provider", "Model", "True Diagnosis", "Output Content"]) # Header with new column

        for filename in output_files:
            file_info = parse_filename(filename)
            if file_info:
                filepath = os.path.join(output_dir, filename)
                content = read_markdown_file(filepath)
                if content:
                    case_id = file_info["case"]
                    true_diagnosis = true_diagnosis_map.get(case_id, "N/A") # Get true diagnosis, default to "N/A" if not found
                    csv_writer.writerow([
                        file_info["team"],
                        file_info["case"],
                        file_info["stage"],
                        file_info["provider"],
                        file_info["model"],
                        true_diagnosis, # Include true diagnosis in CSV
                        content.strip()
                    ])
    print(f"CSV file created successfully: {csv_filepath}")

if __name__ == "__main__":
    create_output_csv()
