
import sys
import os

print("[TEST] Starting Environment & Logic Verification...")

# 1. Check Bazi (lunar_python)
print("\n[1/4] Testing Bazi (lunar_python)...")
try:
    from bazi_calculator import calculate_bazi_chart
    chart = calculate_bazi_chart(1990, 1, 31, 4, 'male')
    print("[OK] Bazi Calculation Success")
    print(f"   Day Master: {chart['day_master']}")
except Exception as e:
    import traceback
    traceback.print_exc()
    print(f"[FAIL] Bazi Failed: {e}")

# 2. Check Astrology (kerykeion)
print("\n[2/4] Testing Astrology (kerykeion)...")
try:
    from kerykeion import AstrologicalSubject
    subject = AstrologicalSubject("Test", 1990, 1, 31, 12, 0, "Taipei", "TW", lat=25.03, lng=121.56, online=False)
    print("[OK] Astrology Data Generated")
    print(f"   Sun Sign: {subject.sun.sign}")
except ImportError:
    print("[FAIL] kerykeion not installed")
except Exception as e:
    import traceback
    traceback.print_exc()
    print(f"[FAIL] Astrology Failed: {e}")

# 3. Check Human Design (ephem)
print("\n[3/4] Testing Human Design (ephem)...")
try:
    import ephem
    sun = ephem.Sun()
    sun.compute('1990/1/31')
    print("[OK] Ephem Computation Success")
    print(f"   Sun Pos: {sun.hlon}")
except Exception as e:
    print(f"[FAIL] Ephem Failed: {e}")

# 4. Check Ziwei (internal logic)
print("\n[4/4] Testing Ziwei (ziwei_calculator)...")
try:
    from ziwei_calculator import calculate_ziwei_chart
    # Correct function name
    print("[OK] Ziwei Module Imported")
except ImportError:
    print("[FAIL] Ziwei Module Missing")
except Exception as e:
    print(f"[FAIL] Ziwei Failed: {e}")

print("\n[DONE] Verification Complete.")
