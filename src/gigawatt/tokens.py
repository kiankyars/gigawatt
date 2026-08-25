"""Design tokens — the entire aesthetic lives here (anti-slop contract).

One typeface, two line weights, one voltage-keyed color scale, flat fills only.
No gradients, no shadows, no decoration.
"""

FONT = "Inter, 'Helvetica Neue', sans-serif"
FONT_SIZE = 12  # base label size at 1:1 symbol scale

STROKE = 1.5        # standard line weight
STROKE_HEAVY = 3.0  # buses and the lit watt path

INK = "#1a1a1a"
PAPER = "#fafaf7"
MUTED_TEXT = "#5f5f59"   # informational text; > 6:1 contrast on PAPER
FAINT_GUIDE = "#d4d4cd"  # construction lines and dimmed geometry only
FAINT = FAINT_GUIDE       # legacy mock/symbol-sheet alias; never use for text

# Journey bar, electrical descent (keyed by carrier/state, not by act).
VOLTAGE = {
    "source_branches": "#0b2e59",
    "138kV": "#143f70",
    "345kV": "#0b2e59",
    "generator_terminal_mv": "#2b7fa3",
    "campus_mv": "#175d8d",
    "facility_lv_ac": "#2f9e8f",
    "rack_ac": "#2f9e8f",
    "rack_dc": "#57b894",
    "core_voltage": "#8fd0a5",
}

JOURNEY_LABEL = {
    "source_branches": "HV / gen MV",
    "138kV": "138 kV",
    "345kV": "345 kV",
    "generator_terminal_mv": "generator MV",
    "campus_mv": "campus MV",
    "facility_lv_ac": "facility AC",
    "rack_ac": "rack AC",
    "rack_dc": "50–51 VDC",
    "core_voltage": "core V",
    "die_heat": "die heat",
    "technology_return": "tech return",
    "facility_return": "facility return",
    "atmosphere": "atmosphere",
}

# Journey bar, thermal ascent (die -> atmosphere).
THERMAL = {
    "die_heat": "#b3261e",
    "technology_return": "#d3552c",
    "technology_supply": "#4a90d9",
    "facility_return": "#e8853b",
    "facility_supply": "#67a9cf",
    "air": "#f0b34e",
    "atmosphere": "#f0b34e",
    "water": "#4a90d9",  # initial fill / maintenance, not heat rejection
}
