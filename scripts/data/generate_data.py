import os
from pathlib import Path
import random
import pandas as pd

# Probabilistic generation
random.seed(42)

DATA_DIR = "data"
DATA_FILENAME = "data.csv"
NUM_PLANETS_PER_HABITABILITY = 10_000

FEATURES = {
    "Atmospheric Pressure (bar)": {
        "description": "Average pressure of the planet's atmosphere",  # Earth's atmospheric pressure is 1 bar
        "range": (0.1, 3),  # In bars
        "weight": 1.1,
        "rule": (0.5, 2.5),
    },
    "Magnetic Field Strength (µT)": {
        "description": "Strength of the planet's magnetic field",  # Earth's magnetic field is 25 to 65 microteslas
        "range": (0.01, 4),  # In microteslas
        "weight": 2.1,
        "rule": (0.01, 2.5),
    },
    "H2O Traces": {
        "description": "Presence of water on the planet",
        "range": (False, True),  # True or False
        "weight": 2.5,
        "rule": (0.1, 1),
    },
    "Average Radiation Levels (Siverts)": {
        "description": "Average amount of radiation the planet is exposed to per year",  # Recommendended radiation exposure to 0.5 Sv/year
        "range": (0.01, 1.5),  # In Sieverts
        "weight": 0.9,
        "rule": (0.01, 1),
    },
    "Alien Presence Probability": {
        "description": "Probability of alien life on the planet",
        "range": (0, 0.5),  # 0-1 scale
        "weight": 0.8,
        "rule": (0, 0.8),
    },
    "Solar Flare Frequency (per year)": {
        "description": "Frequency of solar flares on the planet per year",  # Earth's solar flare frequency is 10 per year
        "range": (0, 40),  # In flares per year
        "weight": 0.5,
        "rule": (0, 30),
    },
    "Bio-Growth Probability": {
        "description": "Potential of the planet to support life",
        "range": (0, 1),  # 0-1 scale
        "weight": 1.25,
        "rule": (0.1, 1),
    },
}

RELATIONSHIPS = [
    # Increase traces of water if atmospheric pressure is high
    {
        "source": "Atmospheric Pressure (bar)",
        "target": "H2O Traces",
        "condition": lambda x: 0.5 < x < 2,
        "effect": lambda x, _: 1 if random.uniform(0, 1) > 0.4 else x,
    },
    # Increase bio-growth potentiality if there are traces of water
    {
        "source": "H2O Traces",
        "target": "Bio-Growth Probability",
        "condition": lambda x: x,
        "effect": lambda x, _: x * random.uniform(1.1, 1.5),
    },
    # Decrease average radiation levels if magnetic field strength is high
    {
        "source": "Magnetic Field Strength (µT)",
        "target": "Average Radiation Levels (Siverts)",
        "condition": lambda x: x > 0.1,
        "effect": lambda x, y: min(x, x * (75 / y)),
    },
    # Decrease solar flare frequency if magnetic field strength is high
    {
        "source": "Magnetic Field Strength (µT)",
        "target": "Solar Flare Frequency (per year)",
        "condition": lambda x: x > 0.1,
        "effect": lambda x, y: min(x, x * (70 / y)),
    },
    # Decrease bio-growth potentiality if average radiation levels are high
    {
        "source": "Average Radiation Levels (Siverts)",
        "target": "Bio-Growth Probability",
        "condition": lambda x: x > 0.5,
        "effect": lambda x, y: min(x, x * (3 / y)),
    },
    # Increase average radiation levels if solar flare frequency is high
    {
        "source": "Solar Flare Frequency (per year)",
        "target": "Average Radiation Levels (Siverts)",
        "condition": lambda x: x > 50,
        "effect": lambda x, y: max(x, x * (y / 75)),
    },
    # Increase bio-growth potentiality if probability of alien presence is high
    {
        "source": "Alien Presence Probability",
        "target": "Bio-Growth Probability",
        "condition": lambda x: x > 0.5,
        "effect": lambda x, y: x * random.uniform(1.1, 1.5),
    },
]


# Initialize an empty list to store the generated data
habitable_planet_count = 0
non_habitable_planet_count = 0
data = []

# Generate synthetic data for each planet
while (
    sum([habitable_planet_count, non_habitable_planet_count])
    < NUM_PLANETS_PER_HABITABILITY * 2
):
    planet_data = {}
    habitability_score = 0
    rule_habitability = True

    # Generate data for each feature
    for feature, details in FEATURES.items():
        feature_range = details["range"]

        if any(isinstance(x, bool) for x in feature_range):
            planet_data[feature] = random.choice([0, 1])
        else:
            planet_data[feature] = random.uniform(*feature_range)

    # Calculate the habitability score
    for feature, details in FEATURES.items():
        feature_range = details["range"]
        weight = details["weight"]
        rule_range = details["rule"]

        # Apply relationships
        for relationship in RELATIONSHIPS:
            if feature == relationship["target"]:
                if relationship["condition"](planet_data[relationship["source"]]):
                    planet_data[feature] = relationship["effect"](
                        planet_data[feature], planet_data[relationship["source"]]
                    )

        value = planet_data[feature]

        exception = random.uniform(0, 1)
        if (
            rule_habitability
            and not (rule_range[0] <= value <= rule_range[1])
            and exception < 0.95
        ):
            rule_habitability = False

        normalized_value = (value - feature_range[0]) / (
            feature_range[1] - feature_range[0]
        )
        habitability_score += normalized_value * weight

    habitability_score /= len(FEATURES)

    # Assign the habitability label based on the score
    if habitability_score > 0.75 and rule_habitability:
        habitability = 1  # Habitable
        if habitable_planet_count >= NUM_PLANETS_PER_HABITABILITY:
            continue
        habitable_planet_count += 1
    else:
        habitability = 0  # Non-habitable
        if non_habitable_planet_count >= NUM_PLANETS_PER_HABITABILITY:
            continue
        non_habitable_planet_count += 1

    # Add the generated data and habitability label to the DataFrame
    planet_data["Habitability"] = habitability
    data.append(planet_data)

    # Print progress
    if len(data) % 100 == 0:
        print(f"Generated {len(data)} planets...", end="\r")

# Convert the list of dictionaries to a Pandas DataFrame
df = pd.DataFrame(data)

# Save the dataset to a CSV file
if not Path(DATA_DIR).exists():
    os.makedirs(DATA_DIR)
df.to_csv(os.path.join(DATA_DIR, DATA_FILENAME), index=False)
print("Generated dataset saved to {}".format(os.path.join(DATA_DIR, DATA_FILENAME)))

print("\nFeatures description:")
print(df.describe(include="all"))
