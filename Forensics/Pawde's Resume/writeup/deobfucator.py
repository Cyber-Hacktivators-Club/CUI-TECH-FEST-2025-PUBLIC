#!/usr/bin/env python3
"""
Enhanced deobfuscator for batch files with proper formatting restoration.
"""
import sys
import re
from pathlib import Path

def parse_variable_mappings(content):
    """Extract all SET variable=value mappings."""
    mappings = {}
    pattern = re.compile(r'^\s*set\s+([^=\s]+)=(.+?)\s*$', re.IGNORECASE | re.MULTILINE)
    
    for match in pattern.finditer(content):
        var_name = match.group(1).strip()
        value = match.group(2).strip()
        mappings[var_name] = value
    
    return mappings

def expand_variables(text, mappings, max_iterations=100):
    """Recursively expand %VARIABLE% references."""
    pattern = re.compile(r'%([^%\s]+)%')
    
    for _ in range(max_iterations):
        changed = False
        
        def replace_var(match):
            nonlocal changed
            var_name = match.group(1)
            if var_name in mappings:
                changed = True
                return mappings[var_name]
            return match.group(0)
        
        new_text = pattern.sub(replace_var, text)
        if not changed:
            break
        text = new_text
    
    return text

def restore_formatting(text):
    """Restore proper batch file formatting."""
    lines = []
    
    for line in text.split('\n'):
        # Skip lines that are just variable definitions for single characters
        if re.match(r'^\s*set\s+[A-Za-z]{2}=[^a-zA-Z0-9\s]?\s*$', line, re.IGNORECASE):
            continue
        
        # Skip the setlocal EnableDelayedExpansion if it appears twice
        if 'setlocalenabledelayedexpansion' in line.lower().replace(' ', '') and \
            any('setlocal' in i.lower() for i in lines):
            continue
        
        # Restore spaces around operators and keywords
        line = re.sub(r'@echooff', '@echo off', line, flags=re.IGNORECASE)
        line = re.sub(r'setlocal', 'setlocal ', line, flags=re.IGNORECASE)
        line = re.sub(r'enabledelayedexpansion', 'enabledelayedexpansion', line, flags=re.IGNORECASE)
        line = re.sub(r'title([A-Z])', r'title \1', line)
        
        # Fix cmd /c spacing
        line = re.sub(r'cmd/c', 'cmd /c ', line, flags=re.IGNORECASE)
        
        # Fix set /a spacing
        line = re.sub(r'set/a', 'set /a ', line, flags=re.IGNORECASE)
        
        # Fix if statements
        line = re.sub(r'ifnot', 'if not ', line, flags=re.IGNORECASE)
        line = re.sub(r'iferrorlevel', 'if errorlevel ', line, flags=re.IGNORECASE)
        line = re.sub(r'ifexist', 'if exist ', line, flags=re.IGNORECASE)
        
        # Fix goto statements
        line = re.sub(r'goto:', 'goto :', line, flags=re.IGNORECASE)
        
        # Fix exit statements
        line = re.sub(r'exit/b', 'exit /b ', line, flags=re.IGNORECASE)
        
        # Fix for statements
        line = re.sub(r'for/f', 'for /f ', line, flags=re.IGNORECASE)
        
        # Fix mkdir, rd commands
        line = re.sub(r'mkdir', 'mkdir ', line, flags=re.IGNORECASE)
        line = re.sub(r'rd/s/q', 'rd /s /q ', line, flags=re.IGNORECASE)
        
        # Fix timeout
        line = re.sub(r'timeout/t', 'timeout /t ', line, flags=re.IGNORECASE)
        
        # Fix reg query
        line = re.sub(r'regquery', 'reg query ', line, flags=re.IGNORECASE)
        
        # Add quotes around paths with % variables
        line = re.sub(r'(set\s+\w+=)(%[^%]+%[^"\n]*)', r'\1"\2"', line, flags=re.IGNORECASE)
        
        # Add spaces after commas in set commands
        line = re.sub(r'(set\s+)"([^=]+)=([^"]+)"', lambda m: f'{m.group(1)}"{m.group(2)}={m.group(3)}"', line, flags=re.IGNORECASE)
        
        # Fix REM formatting
        line = re.sub(r'^REM([A-Z])', r'REM \1', line, flags=re.IGNORECASE)
        
        # Fix common command concatenations
        line = re.sub(r'>nul2>&1', '>nul 2>&1', line)
        line = re.sub(r'2\^>nul', '2^>nul', line)
        
        # Fix tokens= in for loops
        line = re.sub(r'tokens=(\d+-\d+)delims=', r'tokens=\1 delims=', line, flags=re.IGNORECASE)
        line = re.sub(r'tokens=\*', 'tokens=*', line, flags=re.IGNORECASE)
        
        # Fix echo statements
        line = re.sub(r'echo([A-Z])', r'echo \1', line, flags=re.IGNORECASE)
        
        # Clean up multiple spaces (but preserve indentation)
        if line.strip():
            leading = len(line) - len(line.lstrip())
            content = ' '.join(line.split())
            line = ' ' * leading + content
        
        lines.append(line)
    
    return '\n'.join(lines)

def deobfuscate_file(input_path):
    """Main deobfuscation routine."""
    path = Path(input_path)
    
    if not path.exists():
        print(f"Error: File not found: {input_path}")
        return None
    
    content = path.read_text(encoding='utf-8', errors='ignore')
    
    print("[*] Parsing variable mappings...")
    mappings = parse_variable_mappings(content)
    print(f"[+] Found {len(mappings)} variable mappings")
    
    print("[*] Expanding variables...")
    expanded = expand_variables(content, mappings)
    
    print("[*] Restoring formatting...")
    cleaned = restore_formatting(expanded)
    
    # Write output
    output_file = path.parent / f"{path.stem}_deobfuscated.bat"
    output_file.write_text(cleaned, encoding='utf-8')
    
    print("\n[+] Deobfuscation complete!")
    print(f"[+] Output file: {output_file}")
    
    return cleaned

def main():
    if len(sys.argv) < 2:
        print("Usage: python deobfuscate_ctf.py <obfuscated_file.bat>")
        return 1
    
    result = deobfuscate_file(sys.argv[1])
    
    if result:
        print("\n" + "="*60)
        print("PREVIEW (first 30 lines):")
        print("="*60)
        for i, line in enumerate(result.split('\n')[:30], 1):
            print(f"{i:3}: {line}")
    
    return 0

if __name__ == '__main__':
    sys.exit(main())