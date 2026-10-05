#!/bin/bash
# Lance tous les tests - EduPaie

echo "=== Tests EduPaie ==="
cd "$(dirname "$0")/.."
python -m pytest tests/ -v
echo "=== Tests termines ==="
