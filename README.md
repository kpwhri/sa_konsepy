# Self-Harm and Suicide Attempt Event Detection

This project uses rule-based natural language processing (NLP) to identify text that may describe self-harm, suicide
attempts, or related history in clinical or narrative notes.

The project is built with the `konsepy` framework and uses regular expressions to detect specific language patterns. It
is intended to support structured review of large text corpora by flagging potentially relevant mentions for further
analysis or validation.

> **Important:** This software does not make clinical decisions. It should not be used as a substitute for professional
> judgment, risk assessment, crisis response, or patient care. Outputs should be reviewed and validated by qualified users
> before being used for research, reporting, or operational decisions.

## What This Project Detects

The primary concept in this project is suicide attempt / self-harm documentation.

The detector can identify several types of mentions, including:

- Direct suicide attempt statements
    - Example: `after a suicide attempt`
- Attempted suicide phrasing
    - Example: `attempted suicide`
- Self-harm behavior descriptions
    - Example: `deliberate self harm`
- Historical mentions
    - Example: `history of suicide attempt`
- Negated mentions
    - Example: `no history of suicide attempt`
- Family or other-subject mentions
    - Example: `family history of suicide attempt`
- Problem-list mentions
    - Example: `problem list: hx of suicide attempt`
- Action-based descriptions
    - Example: `jumped in front of traffic`

The output should be interpreted as text pattern matches, not as confirmed clinical events.

## Input Data Format

The input corpus should be a CSV file.

By default, the code expects the following columns:

| Column      | Required | Description                                                                                                |
|-------------|----------|------------------------------------------------------------------------------------------------------------|
| `studyid`   | Yes      | Subject-level identifier. If you do not have subject IDs, use the same value for all rows, such as `1`.    |
| `note_id`   | Yes      | Unique identifier for each note or document.                                                               |
| `note_text` | Yes      | The text to process.                                                                                       |
| `note_date` | No       | Date of the note. This is optional and is not required by the detection rules.                             |
| `note_line` | No       | Line order for notes split across multiple rows. Use this only if one note is divided into multiple lines. |

Example CSV:

```csv
studyid,note_id,note_text
1,1001,"Patient reports a prior suicide attempt in high school."
1,1002,"Patient denies history of suicide attempt."
```

If your data uses different column names, the command-line tools can be configured with arguments such as `--id-label`,
`--noteid-label`, and `--notetext-label`.

## Getting Started for New Python Users

This section assumes you are not already familiar with Python. Follow the steps in order.

### 1. Install Python

Install Python 3.11 or newer.

This project is compatible with Python 3.11 and later.

To check whether Python is installed, open a terminal and run:

```bash
python --version
```

On some systems, the command may be:

```bash
python3 --version
```

You should see a version such as:

```text
Python 3.13.11
```

### 2. Download or Clone the Project

Place the project somewhere easy to find.

For example:

- Windows: `C:\code\sa_konsepy`
- macOS/Linux: `~/code/sa_konsepy`

In the instructions below, this folder is referred to as `$PROJECT_PATH`.

### 3. Open a Terminal in the Project Folder

On Windows PowerShell:

```bash
cd C:\code\sa_konsepy
```

On macOS/Linux:

```bash
cd ~/code/sa_konsepy
```

### 4. Create a Virtual Environment

A virtual environment keeps this project’s Python packages separate from other Python projects on your computer.

Create one with:

```bash
python -m venv .venv
```

If `python` does not work, try:

```bash
python3 -m venv .venv
```

### 5. Activate the Virtual Environment

On Windows PowerShell:

```bash
.venv\Scripts\Activate.ps1
```

On macOS/Linux:

```bash
source .venv/bin/activate
```

After activation, your terminal prompt may show `(.venv)`.

### 6. Install Required Packages

Install the project dependencies:

```bash
pip install -r requirements.txt
```

Alternatively, if you want to install the project as a local Python package:

```bash
pip install .
```

### 7. Make the Source Code Available to Python

Before running the scripts directly, set `PYTHONPATH` so Python can find the project code.

On Windows PowerShell:

```bash
$env:PYTHONPATH="$PWD\src"
```

On macOS/Linux:

```bash
export PYTHONPATH="$PWD/src"
```

You should run this command each time you open a new terminal, unless your environment is configured another way.

## Running the Code

### Run All Concepts

To process the sample corpus and write results to an output directory named `out`:

```bash
python src/run_all.py --input-files sample/corpus.csv --outdir out
```

This runs all configured concept detectors, including the suicide attempt / self-harm detector.

### Run Only the Suicide Attempt Concept

To run only the suicide attempt concept:

```bash
python src/run_concept.py --input-files sample/corpus.csv --outdir out --concept suicide_attempt
```

### Run on a Corpus Split Across Lines

If your notes are split across multiple rows and ordered by a line column, use `--noteorder-label`.

Example:

```bash
python src/run_all.py --input-files sample/corpus_lined.csv --outdir out --noteorder-label note_line
```

Or for only the suicide attempt concept:

```bash
python src/run_concept.py --input-files sample/corpus_lined.csv --outdir out --concept suicide_attempt --noteorder-label note_line
```

## Using Your Own Data

Prepare a CSV file with at least these columns:

```csv
studyid,note_id,note_text
```

Then run:

```bash
python src/run_all.py --input-files path/to/your_data.csv --outdir out
```

If your column names differ, specify them explicitly.

For example, if your file has these columns:

```csv
person_id,document_id,text
```

Run:

```bash
python src/run_all.py ^
  --input-files path/to/your_data.csv ^
  --outdir out ^
  --id-label person_id ^
  --noteid-label document_id ^
  --notetext-label text
```

On macOS/Linux, use backslashes for line continuation:

```bash
python src/run_all.py \
  --input-files path/to/your_data.csv \
  --outdir out \
  --id-label person_id \
  --noteid-label document_id \
  --notetext-label text
```

You can also write the command on one line:

```bash
python src/run_all.py --input-files path/to/your_data.csv --outdir out --id-label person_id --noteid-label document_id --notetext-label text
```

## Finding Example Text Snippets

Before running the full detector, it can be useful to inspect examples of relevant phrases in your corpus.

For example, to extract snippets containing the phrase `suicide attempt`:

```bash
python src/get_text_snippets.py --input-files sample/corpus.csv --outdir out --regexes SUICIDE_ATTEMPT=="suicide attempt"
```

To search for self-harm phrasing:

```bash
python src/get_text_snippets.py --input-files sample/corpus.csv --outdir out --regexes SELF_HARM=="self harm"
```

For a lined corpus:

```bash
python src/get_text_snippets.py --input-files sample/corpus_lined.csv --outdir out --regexes SUICIDE_ATTEMPT=="suicide attempt" --noteorder-label note_line
```

Snippet review is recommended when adapting this project to a new dataset, because language patterns can vary across
institutions, note types, and documentation practices.

## Running Tests

Tests confirm that the suicide attempt detection rules behave as expected on known examples.

Run:

```bash
pytest tests
```

A successful test run should complete without failures.

If a test fails, it usually means that a rule was changed in a way that affected expected behavior.

## Output Review

The scripts write output files to the directory specified by `--outdir`.

For example:

```bash
python src/run_all.py --input-files sample/corpus.csv --outdir out
```

will create or update files in:

```text
out/
```

Review the generated output carefully. Matches should be treated as candidate detections that may require human
validation.

## Deployment Guidance

For routine use, the recommended workflow is:

1. Prepare a CSV file containing the text to analyze.
2. Confirm the file has the required identifier and text columns.
3. Create and activate the Python virtual environment.
4. Install dependencies.
5. Run the detector on a small sample first.
6. Review the output manually.
7. If the output looks correct, run the detector on the full corpus.
8. Store outputs securely according to your organization’s privacy and data governance requirements.

Example production-style run:

```bash
python src/run_all.py --input-files data/input_notes.csv --outdir results/suicide_attempt_detection
```

If processing sensitive data, ensure that:

- The machine is approved for handling that data.
- Input and output files are stored in approved locations.
- Access is limited to authorized users.
- Any extracted snippets are treated as potentially sensitive.

## Limitations

This project uses rule-based pattern matching. As a result:

- It may miss relevant mentions that use unexpected wording.
- It may incorrectly flag irrelevant text.
- It may not fully understand context, temporality, severity, or intent.
- It cannot determine whether an event truly occurred.
- It should not be used for emergency monitoring without appropriate clinical systems and governance.

The detector is best used as a transparent, auditable first-pass text screening tool.

## Customization

Detection logic is located in:

```text
src/sa_konsepy/concepts/suicide_attempt.py
```

Tests are located in:

```text
tests/test_suicide_attempt.py
```

When changing detection rules, add or update tests to document the expected behavior.

After modifying rules, run:

```bash
pytest tests
```

## Troubleshooting

### `python` is not recognized

Try:

```bash
python3 --version
```

If that works, use `python3` instead of `python` in the commands.

### `ModuleNotFoundError`

Make sure you activated the virtual environment and set `PYTHONPATH`.

Windows PowerShell:

```bash
.venv\Scripts\Activate.ps1
$env:PYTHONPATH="$PWD\src"
```

macOS/Linux:

```bash
source .venv/bin/activate
export PYTHONPATH="$PWD/src"
```

### Package installation fails

Make sure the virtual environment is activated, then upgrade `pip`:

```bash
python -m pip install --upgrade pip
```

Then reinstall requirements:

```bash
pip install -r requirements.txt
```

### No matches are found

Check that:

- The input file path is correct.
- The text column is correctly named or specified with `--notetext-label`.
- The input text actually contains relevant terms.
- The data is saved as a readable CSV file.

You can also use `get_text_snippets.py` to inspect whether expected terms appear in your corpus.

