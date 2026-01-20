from kerykeion import AstrologicalSubject
import warnings
warnings.filterwarnings("ignore")

try:
    print("Testing Astrology with KrInstance...")
    from kerykeion import KrInstance
    # KrInstance often uses positional for name, y, m, d, h, m and keyword for the rest
    subject = KrInstance("Test", 1990, 1, 31, 12, 0, city="Taipei", lat=25.03, lng=121.56, tz_str="Asia/Taipei")
    print(f"Success! Sun Sign: {subject.sun.sign}")
except Exception as e:
    print(f"Failed! Error: {e}")
