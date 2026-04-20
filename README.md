# Game QA Pipeline Data Vision Expert

Codex skill for game QA requirement analysis and test asset generation. It is designed for game requirements that combine prose, UI screenshots, and configuration tables, with emphasis on traceability, historical bug-pattern scanning, and structured XLSX delivery.

## Contents

- `SKILL.md` - skill instructions and workflow.
- `agents/openai.yaml` - agent configuration.
- `scripts/build_game_qa_data_vision_workbook.py` - helper script for structured workbook generation.

## Install

Clone this repository into your Codex skills directory:

```powershell
git clone https://github.com/honey-yang-work/game-qa-pipeline-data-vision-expert.git "$env:USERPROFILE\.codex\skills\game-qa-pipeline-data-vision-expert"
```

If the target directory already exists, back it up or remove it before cloning.

## Usage

Invoke the skill when auditing game requirements that combine text, UI images, and configuration tables, especially when the output should include:

- Requirement decomposition and risk probes.
- Requirement-to-test traceability.
- Historical pitfall coverage.
- High-coverage test case design.
- Python-generated XLSX assets.

## Development

The helper script uses Python workbook tooling. Install project dependencies in your preferred environment before running it:

```powershell
python -m pip install openpyxl
python -m py_compile .\scripts\build_game_qa_data_vision_workbook.py
```
