
from api import get_astrology_calculation_result

def test_fallback():
    print("Testing Astrology Calculation Fallback...")
    try:
        # Simulate an input that we know works (or should work with fallback)
        res = get_astrology_calculation_result(1990, 1, 1, 12, 0, "Taipei", 25.03, 121.56)
        
        print(f"Success: {res['success']}")
        print(f"Sun Sign: {res['sunSign']}")
        print(f"Moon Sign: {res['moonSign']}")
        print(f"Planets: {list(res['planets'].keys())}")
        
        # Verify professional data availability
        print(f"Houses Count: {len(res['houses'])}")
        if len(res['houses']) > 0:
             print(f"House 1: {res['houses'][0]}")
        print(f"Aspects Count: {len(res['aspects'])}")
        
    except Exception as e:
        print(f"Test Failed: {e}")

if __name__ == "__main__":
    test_fallback()
