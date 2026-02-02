import sys
import os
from io import StringIO

# Fix import path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from converter.cli import read_cli_input

# Input simulat
input_data = """math
-3
10
+
-13
10
2
y
1

exit
"""

# Redirectionare stdin
sys.stdin = StringIO(input_data)

try:
    read_cli_input()
except SystemExit:
    pass
