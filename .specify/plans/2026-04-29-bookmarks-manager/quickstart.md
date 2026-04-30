# Quickstart: 001-bookmarks-manager

## Install
```bash
pip install groupmrk
```

## Usage
```bash
groupmrk import bookmarks.html -o organized.html
groupmrk search "python tutorials"
groupmrk organize --max-themes 5
```

## Options
- `--max-themes N`: Customize max categories (default: 10)
- `--model MODEL`: Choose classification model
- `--provider hf|ollama`: API provider (default: hf)
- `--offline`: Force Ollama even if HF available