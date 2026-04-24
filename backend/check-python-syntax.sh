#!/bin/bash
find . -name "*.py" -not -path "./.venv/*" | while read f; do
  if ! .venv/bin/python -m py_compile "$f"; then
    echo "FAILED: $f"
    exit 1
  else
    echo "OK: $f"
  fi
done
