# USS Qualifier Report Guide

This guide explains how to read and access the USS Qualifier test reports in a readable format.

## Report Locations

After running tests, reports are generated in:

```
./monitoring/uss_qualifier/output/<test_name>/
```

For example, the `airwayz_rid_test` reports are in:

```
./monitoring/uss_qualifier/output/airwayz_rid_test/
```

## Available Report Formats

### 1. **HTML Report (Most User-Friendly)** ⭐ RECOMMENDED

**File:** `report.html`

**How to view:**

- **Windows:** Double-click the file or run:
  ```powershell
  Start-Process monitoring\uss_qualifier\output\airwayz_rid_test\report.html
  ```
- **Linux/Mac:** Open in any browser:
  ```bash
  open monitoring/uss_qualifier/output/airwayz_rid_test/report.html
  ```

**Features:**

- ✅ Interactive and visually appealing
- ✅ Expandable test sections
- ✅ Syntax-highlighted JSON
- ✅ Easy navigation through test cases
- ✅ Shows passed/failed checks clearly

### 2. **Formatted JSON Report (For Reading/Searching)**

**File:** `report.formatted.json` (auto-generated)

**How to view:**

- Open with any text editor (VS Code, Notepad++, etc.)
- Properly indented with 2 spaces
- Easy to read and search

**How it's generated:**
The `run-tests-and-notify.sh` script automatically creates this file after each test run using:

```bash
python scripts/format-report.py monitoring/uss_qualifier/output/airwayz_rid_test/report.json
```

**Features:**

- ✅ Well-formatted JSON with proper indentation
- ✅ Easy to read in any text editor
- ✅ Searchable with Ctrl+F
- ✅ Good for extracting specific data

### 3. **Raw JSON Report (For Programmatic Access)**

**File:** `report.json`

**How to view:**

- ⚠️ **Not recommended for human reading** - single line, minified
- Use for programmatic access or parsing with tools

**To format manually:**

```bash
python scripts/format-report.py <path-to-report.json>
```

## Format Report Script

### Usage

```bash
python scripts/format-report.py <input_json> [output_json] [indent]
```

### Examples

```bash
# Format with default settings (2-space indent, auto-named output)
python scripts/format-report.py ./output/airwayz_rid_test/report.json

# Format with custom output path
python scripts/format-report.py report.json readable_report.json

# Format with 4-space indentation
python scripts/format-report.py report.json formatted.json 4
```

### Output

```
[INFO] Reading JSON from: monitoring\uss_qualifier\output\airwayz_rid_test\report.json
[INFO] Writing formatted JSON to: monitoring\uss_qualifier\output\airwayz_rid_test\report.formatted.json
[INFO] Formatting complete!
  Original:  19,649 bytes
  Formatted: 43,854 bytes (+123.2%)
[SUCCESS] Report formatted successfully!
```

## What's in the Reports?

The reports contain:

1. **Configuration** - Test configuration and resource declarations
2. **Test Results**
   - Test suite name and documentation links
   - Test scenarios executed
   - Test cases and steps
   - Passed/failed checks
   - API queries and responses
3. **Codebase Info** - Git commit hash and version
4. **Timestamps** - Start/end times for all tests and steps

## Automatic Formatting

The `run-tests-and-notify.sh` script has been updated to **automatically format** the JSON report after each test run. You don't need to do anything manually - both reports are generated automatically:

1. ✅ `report.json` - Raw minified JSON (for tools)
2. ✅ `report.formatted.json` - Human-readable formatted JSON (for you)
3. ✅ `report.html` - Interactive HTML (best for browsing)

## Recommendation

**For reviewing test results:**

1. Start with `report.html` - it's the most user-friendly
2. Use `report.formatted.json` when you need to search for specific details or want to work in your code editor
3. Avoid `report.json` unless you're writing scripts to parse it

## Troubleshooting

### The formatted report doesn't exist

Run the formatter manually:

```bash
python scripts/format-report.py monitoring/uss_qualifier/output/airwayz_rid_test/report.json
```

### HTML report won't open

Make sure you have a web browser installed. The HTML report is a standalone file that works in any modern browser.

### JSON is still unreadable

Make sure you're opening `report.formatted.json`, not `report.json`. The latter is intentionally minified for efficiency.
