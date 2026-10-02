import math
import matplotlib.pyplot as plt
import numpy as np

def calculate_indices(species_abundances, input_type="Counts"):
    """
    species_abundances: list of (species_name, abundance_value) tuples
    input_type: "Counts" or "Percentages"
    Returns dictionary with S, N, H, D, 1-D, 1/D, J, and sorted_abundances for plotting.
    """
    if not species_abundances:
        raise ValueError("At least one species is required.")
    if len(species_abundances) > 30:
        raise ValueError("Maximum 30 species allowed.")
    # Extract abundances
    species = []
    abundances = []
    for sp, ab in species_abundances:
        if not isinstance(sp, str) or not sp.strip():
            raise ValueError(f"Invalid species name: {sp}")
        if not isinstance(ab, (int, float)) or ab < 0:
            raise ValueError(f"Abundance must be non-negative number, got {ab}")
        species.append(sp.strip())
        abundances.append(float(ab))
    total = sum(abundances)
    if total == 0:
        raise ValueError("Total abundance must be greater than zero.")
    S = len(species)
    if input_type == "Percentages":
        # Normalize to sum to 1
        total_fraction = total  # may be >100? but we treat as percentages
        # Actually percentages should sum to 100, but we normalize to avoid issues
        proportions = [a / total for a in abundances]
        N = total  # sum of percentages (e.g., 100 if input sums to 100)
    else:
        proportions = [a / total for a in abundances]
        N = total
    # Shannon
    H = 0.0
    for p in proportions:
        if p > 0:
            H -= p * math.log(p)
    # Simpson
    D = sum(p*p for p in proportions)
    one_minus_D = 1 - D
    one_over_D = 1 / D if D > 0 else float('inf')
    # Pielou
    if S > 1:
        J = H / math.log(S)
    else:
        J = 1.0  # by convention for single species
    # Sort abundances for plot (highest to lowest)
    sorted_pairs = sorted(zip(species, abundances), key=lambda x: x[1], reverse=True)
    sorted_abundances = [(name, val) for name, val in sorted_pairs]
    return {
        "S": S,
        "N": N,
        "H": H,
        "D": D,
        "1-D": one_minus_D,
        "1/D": one_over_D,
        "J": J,
        "sorted_abundances": sorted_abundances
    }

def create_abundance_plot(sorted_abundances):
    """
    Returns a matplotlib Figure with a bar plot of species abundances sorted descending.
    """
    if not sorted_abundances:
        fig, ax = plt.subplots()
        ax.text(0.5, 0.5, "No data", ha="center", va="center")
        return fig
    species_names = [name for name, _ in sorted_abundances]
    abundances_vals = [val for _, val in sorted_abundances]
    fig, ax = plt.subplots(figsize=(8, 5))
    bars = ax.bar(range(len(species_names)), abundances_vals, color="steelblue")
    ax.set_xticks(range(len(species_names)))
    ax.set_xticklabels(species_names, rotation=45, ha="right", fontsize=10)
    ax.set_ylabel("Abundance")
    ax.set_xlabel("Species")
    ax.set_title("Sorted Species Abundances")
    # Optionally add value labels on bars
    for bar, val in zip(bars, abundances_vals):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + max(abundances_vals)*0.02, 
                f"{val:.2f}", ha="center", va="bottom", fontsize=8)
    plt.tight_layout()
    return fig
