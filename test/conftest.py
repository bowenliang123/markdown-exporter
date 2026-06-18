import sys
from pathlib import Path

TEST_ROOT = Path(__file__).parent
sys.path.insert(0, str(TEST_ROOT))
sys.path.insert(0, str(TEST_ROOT / "utils"))
