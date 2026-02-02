#!/usr/bin/env python3
"""
Format USS Qualifier JSON Report
This script formats the minified report.json to be human-readable with proper indentation.
"""
import json
import sys
from pathlib import Path


def format_json_report(input_path: Path, output_path: Path = None, indent: int = 2):
    """
    Format a minified JSON report to be human-readable.
    
    Args:
        input_path: Path to the minified JSON report
        output_path: Path to save formatted report (defaults to input_path with .formatted.json)
        indent: Number of spaces for indentation (default: 2)
    """
    print(f"[INFO] Reading JSON from: {input_path}")
    
    # Read the minified JSON
    with open(input_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Determine output path
    if output_path is None:
        output_path = input_path.parent / f"{input_path.stem}.formatted.json"
    
    print(f"[INFO] Writing formatted JSON to: {output_path}")
    
    # Write formatted JSON
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=indent, ensure_ascii=False)
    
    # Get file sizes
    original_size = input_path.stat().st_size
    formatted_size = output_path.stat().st_size
    
    print(f"[INFO] Formatting complete!")
    print(f"  Original:  {original_size:,} bytes")
    print(f"  Formatted: {formatted_size:,} bytes ({(formatted_size/original_size - 1)*100:+.1f}%)")
    
    return output_path


def main():
    if len(sys.argv) < 2:
        print("Usage: python format-report.py <input_json_file> [output_json_file] [indent]")
        print("\nExample:")
        print("  python format-report.py ./output/airwayz_rid_test/report.json")
        print("  python format-report.py report.json readable_report.json 4")
        sys.exit(1)
    
    input_path = Path(sys.argv[1])
    
    if not input_path.exists():
        print(f"[ERROR] File not found: {input_path}")
        sys.exit(1)
    
    output_path = Path(sys.argv[2]) if len(sys.argv) > 2 else None
    indent = int(sys.argv[3]) if len(sys.argv) > 3 else 2
    
    try:
        format_json_report(input_path, output_path, indent)
        print("\n[SUCCESS] Report formatted successfully!")
    except json.JSONDecodeError as e:
        print(f"[ERROR] Invalid JSON: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"[ERROR] Failed to format report: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
