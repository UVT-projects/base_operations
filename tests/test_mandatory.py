import sys
import os

# Ensure the root directory is in sys.path so we can import 'converter'
# This allows running this script directly or via main.py
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from converter.core import convert_base
from converter.complement import twos_complement

def run_tests():
    """
    Executes mandatory tests.
    """
    print("Running mandatory tests...")
    
    tests = [
        # (func, args, expected)
        (convert_base, ("-101.101", 2, 10), "-5.625"),
        (convert_base, ("-13.625", 10, 2), "-1101.101"),
        (convert_base, ("AF.3", 16, 10), "175.1875"),
    ]
    
    for func, args, expected in tests:
        result = func(*args)
        status = "PASS" if result == expected else f"FAIL (Got {result})"
        print(f"Test {args} -> {expected}: {status}")

    # Special test for 2's complement
    # -5 (base 10) -> 11111011 (binary, 8 bits)
    try:
        res_comp = twos_complement("-5", 8)
        expected_comp = "11111011"
        status_comp = "PASS" if res_comp == expected_comp else f"FAIL (Got {res_comp})"
        print(f"Test 2's Comp '-5', 8 bits -> {expected_comp}: {status_comp}")
    except Exception as e:
        print(f"Test 2's Comp FAILED with error: {e}")

if __name__ == "__main__":
    run_tests()
