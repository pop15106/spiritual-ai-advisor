
# 64 Gates order on the Rave Mandala (Counter-Clockwise)
# Starting from Gate 41 (Aquarius) which is the start of the Rave New Year.
RAVE_MANDALA_ORDER = [
    41, 19, 13, 49, 30, 55, 37, 63, 22, 36, 25, 17, 21, 51, 42, 3, 27, 24, 2, 23, 
    8, 20, 16, 35, 45, 12, 15, 52, 39, 53, 62, 56, 31, 33, 7, 4, 29, 59, 40, 64, 
    47, 6, 46, 18, 48, 57, 32, 50, 28, 44, 1, 43, 14, 34, 9, 5, 26, 11, 10, 58, 
    38, 54, 61, 60
]

# Start degree of Gate 41 (approx 02°15'00" Aquarius = 302.25 degrees)
# Gate 41 is the start of the annual cycle.
# 360 degrees / 64 gates = 5.625 degrees per gate.
# 5.625 / 6 lines = 0.9375 degrees per line.
GATE_41_START_LONGITUDE = 302.25

def get_gate_from_longitude(longitude: float):
    """
    Convert zodiac longitude (0-360) to Human Design Gate and Line.
    
    Args:
        longitude: float (0.0 to 360.0), 0 = Aries 0
        
    Returns:
        dict: {
            "gate": int,
            "line": int,
            "hexagram": str, # optional
            "base": int, # (simplified, optional)
            "tone": int, # (simplified, optional)
            "color": int # (simplified, optional)
        }
    """
    
    # Normalize longitude relative to Gate 41 start
    # If lon < 302.25, we add 360 to handle the wrap around for calculation
    # Actually, simpler: calculate distance from Gate 41 start
    
    # Ensure longitude is 0-360
    longitude = longitude % 360
    
    # Calculate offset from Gate 41 start
    # We want positive distance moving CCW
    distance = (longitude - GATE_41_START_LONGITUDE) % 360
    
    # Determine which gate index (0-63)
    gate_index = int(distance // 5.625)
    
    # Determine gate number from order
    gate_number = RAVE_MANDALA_ORDER[gate_index]
    
    # Determine position within the gate (0.0 to 5.625)
    in_gate_degree = distance % 5.625
    
    # Determine Line (1-6)
    # Each line is 0.9375 degrees
    line_number = int(in_gate_degree // 0.9375) + 1
    
    return {
        "gate": gate_number,
        "line": line_number,
        "str": f"{gate_number}.{line_number}"
    }

# Mapping of Gates to Centers
# Head: 64, 61, 63
# Ajna: 47, 24, 4, 17, 43, 11
# Throat: 62, 23, 56, 16, 20, 31, 8, 33, 35, 12, 45
# G (Identity): 1, 13, 25, 46, 2, 15, 10, 7
# Heart (Ego): 21, 40, 26, 51
# Sacral: 42, 3, 9, 52, 34, 27, 59, 29, 14
# Splenic: 48, 57, 44, 50, 32, 28, 18
# Solar Plexus: 36, 22, 37, 6, 49, 55, 30
# Root: 41, 39, 19, 38, 58, 54, 53, 60, 52(Wait 52 is Root not Sacral? No. 52 is Root)

# Correction: 52 is Root (Mountain). Let's verify standard chart.
# 52 -> 9 (Format channel of Concentration). 9 is Sacral. 52 is Root. Yes.

GATE_TO_CENTER = {
    # Head
    64: "Head", 61: "Head", 63: "Head",
    # Ajna
    47: "Ajna", 24: "Ajna", 4: "Ajna", 17: "Ajna", 43: "Ajna", 11: "Ajna",
    # Throat
    62: "Throat", 23: "Throat", 56: "Throat", 16: "Throat", 20: "Throat", 
    31: "Throat", 8: "Throat", 33: "Throat", 35: "Throat", 12: "Throat", 45: "Throat",
    # G
    1: "G", 13: "G", 25: "G", 46: "G", 2: "G", 15: "G", 10: "G", 7: "G",
    # Heart
    21: "Heart", 40: "Heart", 26: "Heart", 51: "Heart",
    # Sacral
    42: "Sacral", 3: "Sacral", 9: "Sacral", 34: "Sacral", 27: "Sacral", 59: "Sacral", 29: "Sacral", 14: "Sacral", 5: "Sacral",
    # Splenic
    48: "Spleen", 57: "Spleen", 44: "Spleen", 50: "Spleen", 32: "Spleen", 28: "Spleen", 18: "Spleen",
    # Solar Plexus
    36: "Solar", 22: "Solar", 37: "Solar", 6: "Solar", 49: "Solar", 55: "Solar", 30: "Solar",
    # Root
    41: "Root", 39: "Root", 19: "Root", 38: "Root", 58: "Root", 54: "Root", 53: "Root", 60: "Root", 52: "Root"
}

# Channels Definition
# (Gate 1, Gate 2, Type, Circuitry)
CHANNELS_LIST = [
    (1, 8, "Inspiration", "Creative"),
    (2, 14, "The Beat", "Individual"),
    (3, 60, "Mutation", "Individual"),
    (4, 63, "Logic", "Collective"),
    (5, 15, "Rhythm", "Collective"),
    (6, 59, "Mating", "Tribal"),
    (7, 31, "The Alpha", "Collective"),
    (9, 52, "Concentration", "Collective"),
    (10, 20, "Awakening", "Individual"),
    (10, 34, "Exploration", "Individual"),
    (10, 57, "Perfected Form", "Individual"),
    (11, 56, "Curiosity", "Collective"),
    (12, 22, "Openness", "Individual"),
    (13, 33, "The Prodigal", "Collective"),
    (16, 48, "Wavelength", "Collective"),
    (17, 62, "Acceptance", "Collective"),
    (18, 58, "Judgment", "Collective"),
    (19, 49, "Synthesis", "Tribal"),
    (20, 34, "Charisma", "Individual"),
    (20, 57, "The Brainwave", "Individual"),
    (21, 45, "Money", "Tribal"),
    (23, 43, "Structuring", "Individual"),
    (24, 61, "Awareness", "Individual"),
    (25, 51, "Initiation", "Individual"),
    (26, 44, "Surrender", "Tribal"),
    (27, 50, "Preservation", "Tribal"),
    (28, 38, "Struggle", "Individual"),
    (29, 46, "Discovery", "Collective"),
    (30, 41, "Recognition", "Collective"),
    (32, 54, "Transformation", "Tribal"),
    (34, 57, "Power", "Individual"),
    (35, 36, "Transitoriness", "Collective"),
    (37, 40, "Community", "Tribal"),
    (39, 55, "Emoting", "Individual"),
    (42, 53, "Maturation", "Collective"),
    (47, 64, "Abstraction", "Collective")
]

