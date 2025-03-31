# analyze_outputs_llm.py
import os
import pandas as pd
from openai import OpenAI, RateLimitError, APIError
from dotenv import load_dotenv
import time

# --- Configuration ---
INPUT_CSV = "output/output_summary.csv"
OUTPUT_CSV = "output/analysis_summary_llm.csv"
MARKDOWN_COLUMN = "Output Content" # Column containing the full markdown
TRUE_DIAGNOSIS_COLUMN = "True Diagnosis" # Column with the ground truth
NEW_ACCURACY_COLUMN = "LLM_Accuracy_Match" # Checks if final diagnosis matches true
NEW_DIFFERENTIAL_COLUMN = "LLM_Differential_Inclusion" # Checks if true diagnosis is in the differential list
MODEL_NAME = "gpt-4o" # Or specify another model like "gpt-4o-mini" if preferred
MAX_RETRIES = 3
RETRY_DELAY_SECONDS = 5

# --- Load Environment Variables ---
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    print("Error: OPENAI_API_KEY not found in environment variables.")
    print("Please ensure it's set in your .env file or system environment.")
    exit(1)

# --- Initialize OpenAI Client ---
client = OpenAI(api_key=api_key)

# --- LLM Prompt Templates ---
FINAL_DIAGNOSIS_PROMPT_TEMPLATE = """
Review the following medical case discussion report and the provided true diagnosis.
Determine if the true diagnosis is semantically equivalent to the final or most likely diagnosis concluded in the report.
Consider variations in medical terminology and phrasing (e.g., "Type 2 Diabetes Mellitus" vs. "T2DM").

Output ONLY the word "True" if the true diagnosis matches the report's final conclusion, or ONLY the word "False" otherwise. Do not provide any explanation.

True Diagnosis: {true_diagnosis}

Report Content:
---
{markdown_content}
---

Is the True Diagnosis the Final Conclusion in the Report? (True/False):
"""

DIFFERENTIAL_PROMPT_TEMPLATE = """
Review the following medical case discussion report and the provided true diagnosis.
Determine if the true diagnosis is semantically equivalent to ANY diagnosis mentioned in the differential diagnosis list(s) presented within the report.
Consider variations in medical terminology and phrasing (e.g., "Type 2 Diabetes Mellitus" vs. "T2DM").

Output ONLY the word "True" if the true diagnosis is mentioned anywhere in the differential list, or ONLY the word "False" otherwise. Do not provide any explanation.

True Diagnosis: {true_diagnosis}

Report Content:
---
{markdown_content}
---

Is the True Diagnosis Mentioned in the Differential List? (True/False):
"""

# --- LLM Helper Function ---
def call_llm_with_retry(prompt, model=MODEL_NAME, max_retries=MAX_RETRIES, delay=RETRY_DELAY_SECONDS):
    """Calls the LLM with retry logic and returns the text result."""
    if not isinstance(prompt, str) or not prompt.strip():
        print("Warning: Invalid prompt provided to LLM.")
        return None

    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": "You are an expert medical analyst."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.0,
                max_tokens=10
            )
            result_text = response.choices[0].message.content.strip().lower()
            # Basic validation for expected "true" or "false"
            if result_text in ["true", "false"]:
                return result_text
            else:
                print(f"Warning: LLM returned unexpected text: '{result_text}'. Attempt {attempt + 1}/{max_retries}")
                # Optionally retry or return None/False based on desired strictness
                if attempt == max_retries - 1:
                    return None # Failed after retries

        except RateLimitError as e:
            print(f"Rate limit exceeded, retrying in {delay}s... (Attempt {attempt + 1}/{max_retries})")
            time.sleep(delay)
        except APIError as e:
            print(f"OpenAI API error: {e}. Retrying in {delay}s... (Attempt {attempt + 1}/{max_retries})")
            time.sleep(delay)
        except Exception as e:
            print(f"An unexpected error occurred during API call: {e}")
            # Don't retry on unexpected errors immediately, return None
            return None

    print(f"Error: Failed to get valid response from LLM after {max_retries} attempts.")
    return None

# --- Core Analysis Functions ---
def check_final_diagnosis_match(markdown_content, true_diagnosis):
    """Checks if the true diagnosis matches the final conclusion."""
    if not isinstance(markdown_content, str) or not markdown_content.strip() or \
       not isinstance(true_diagnosis, str) or not true_diagnosis.strip():
        print("Warning: Skipping final diagnosis check due to invalid input.")
        return None

    prompt = FINAL_DIAGNOSIS_PROMPT_TEMPLATE.format(
        true_diagnosis=true_diagnosis,
        markdown_content=markdown_content
    )
    result_text = call_llm_with_retry(prompt)

    if result_text == "true":
        return True
    elif result_text == "false":
        return False
    else:
        # Handles None from helper or unexpected text after retries
        print(f"Final diagnosis check failed or returned unexpected result for case with true diagnosis: {true_diagnosis}")
        return None # Indicate failure/uncertainty

def check_differential_inclusion(markdown_content, true_diagnosis):
    """Checks if the true diagnosis is included in the differential list."""
    if not isinstance(markdown_content, str) or not markdown_content.strip() or \
       not isinstance(true_diagnosis, str) or not true_diagnosis.strip():
        print("Warning: Skipping differential inclusion check due to invalid input.")
        return None

    prompt = DIFFERENTIAL_PROMPT_TEMPLATE.format(
        true_diagnosis=true_diagnosis,
        markdown_content=markdown_content
    )
    result_text = call_llm_with_retry(prompt)

    if result_text == "true":
        return True
    elif result_text == "false":
        return False
    else:
        # Handles None from helper or unexpected text after retries
        print(f"Differential inclusion check failed or returned unexpected result for case with true diagnosis: {true_diagnosis}")
        return None # Indicate failure/uncertainty


# --- Main Execution ---
def main():
    """Loads data, performs analysis, and saves results."""
    print(f"Loading data from {INPUT_CSV}...")
    try:
        # Ensure MARKDOWN_COLUMN is read as string, handle potential loading issues
        df = pd.read_csv(INPUT_CSV, dtype={MARKDOWN_COLUMN: str})
        # Fill potential NaN values in critical columns if necessary, or handle them
        df[MARKDOWN_COLUMN] = df[MARKDOWN_COLUMN].fillna('')
        df[TRUE_DIAGNOSIS_COLUMN] = df[TRUE_DIAGNOSIS_COLUMN].fillna('')

    except FileNotFoundError:
        print(f"Error: Input file not found at {INPUT_CSV}")
        return
    except KeyError as e:
        print(f"Error: Missing expected column in {INPUT_CSV}: {e}")
        return
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return

    print(f"Found {len(df)} rows to analyze.")

    # Apply the analysis functions
    # Use .get() with default to handle potentially missing columns gracefully if needed
    # Although the read_csv error handling should catch missing columns earlier.
    print("Starting LLM analysis for final diagnosis match (this may take some time)...")
    df[NEW_ACCURACY_COLUMN] = df.apply(
        lambda row: check_final_diagnosis_match(row.get(MARKDOWN_COLUMN, ''), row.get(TRUE_DIAGNOSIS_COLUMN, '')),
        axis=1
    )
    print("Final diagnosis analysis complete.")

    print("Starting LLM analysis for differential inclusion (this may take some time)...")
    df[NEW_DIFFERENTIAL_COLUMN] = df.apply(
        lambda row: check_differential_inclusion(row.get(MARKDOWN_COLUMN, ''), row.get(TRUE_DIAGNOSIS_COLUMN, '')),
        axis=1
    )
    print("Differential inclusion analysis complete.")

    # Save the results
    print(f"Saving results to {OUTPUT_CSV}...")
    try:
        df.to_csv(OUTPUT_CSV, index=False, encoding='utf-8')
        print("Results saved successfully.")
    except Exception as e:
        print(f"Error saving results to CSV: {e}")

    # Optional: Print summary
    print("\n--- Analysis Summary ---")
    if NEW_ACCURACY_COLUMN in df.columns:
        # Ensure boolean interpretation for value_counts
        accuracy_counts = df[NEW_ACCURACY_COLUMN].astype(object).value_counts(dropna=False)
        print(f"\nFinal Diagnosis Match ({NEW_ACCURACY_COLUMN}):")
        print(accuracy_counts)
        # Calculate accuracy based on non-None results
        valid_accuracy_results = df[NEW_ACCURACY_COLUMN].dropna()
        total_valid_acc = len(valid_accuracy_results)
        if total_valid_acc > 0:
            correct_acc = valid_accuracy_results.sum() # Sum of True values
            percent_correct_acc = (correct_acc / total_valid_acc) * 100
            print(f"Accuracy (Correct / Valid Comparisons): {percent_correct_acc:.2f}% ({correct_acc}/{total_valid_acc})")
        else:
            print("Accuracy: N/A (No valid comparisons)")

    if NEW_DIFFERENTIAL_COLUMN in df.columns:
        # Ensure boolean interpretation for value_counts
        inclusion_counts = df[NEW_DIFFERENTIAL_COLUMN].astype(object).value_counts(dropna=False)
        print(f"\nDifferential Inclusion ({NEW_DIFFERENTIAL_COLUMN}):")
        print(inclusion_counts)
        # Calculate inclusion rate based on non-None results
        valid_inclusion_results = df[NEW_DIFFERENTIAL_COLUMN].dropna()
        total_valid_inc = len(valid_inclusion_results)
        if total_valid_inc > 0:
            included_inc = valid_inclusion_results.sum() # Sum of True values
            percent_included = (included_inc / total_valid_inc) * 100
            print(f"Inclusion Rate (Included / Valid Comparisons): {percent_included:.2f}% ({included_inc}/{total_valid_inc})")
        else:
            print("Inclusion Rate: N/A (No valid comparisons)")

if __name__ == "__main__":
    main()