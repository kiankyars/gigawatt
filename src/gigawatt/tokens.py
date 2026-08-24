"""Design tokens — the entire aesthetic lives here (anti-slop contract).

One typeface, two line weights, one voltage-keyed color scale, flat fills only.
No gradients, no shadows, no decoration.
"""

FONT = "Inter, 'Helvetica Neue', sans-serif"
FONT_SIZE = 11  # base label size at 1:1 symbol scale

STROKE = 1.5        # standard line weight
STROKE_HEAVY = 3.0  # buses and the lit watt path

INK = "#1a1a1a"
PAPER = "#fafaf7"
FAINT = "#b5b5ad"   # port markers, construction lines on review sheets only

# Journey bar, electrical descent (keyed by voltage, not by act).
VOLTAGE = {
    "345kV": "#0b2e59",
    "34.5kV": "#175d8d",
    "20kV": "#2b7fa3",
    "480V": "#2f9e8f",
    "54V": "#57b894",
    "0.8V": "#8fd0a5",
}

# Journey bar, thermal ascent (die -> atmosphere).
THERMAL = {
    "die": "#b3261e",
    "liquid_hot": "#d3552c",
    "liquid_warm": "#e8853b",
    "air": "#f0b34e",
    "water": "#4a90d9",  # makeup/condenser water, not a heat state
}
