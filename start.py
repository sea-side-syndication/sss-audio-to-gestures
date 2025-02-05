from ZEGGS.server import run


import os
import sys
from pathlib import Path

current_file = Path(__file__).resolve()

project_root = current_file.parent / 'ZEGGS'

print(project_root)

sys.path.append(str(project_root))


run()