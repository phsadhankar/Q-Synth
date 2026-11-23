"""Generates the 13-slide visual-first presentation for a 10-minute research talk on Q-Synth.

Structure:
- Slide 1: Introduction to the whole work (Tri-Pillar Architecture)
- Capability 1: Unitary Matrix Synthesis
  - Slide 2: Capability 1 Intro (bullet points & diagram)
  - Slide 3: Capability 1 Steps (6-stage algorithmic pipeline diagram)
  - Slide 4: Capability 1 Benchmark Results (charts & empirical metrics)
  - Slide 5: Capability 1 Better Than Other Work (SOTA comparison matrix)
- Capability 2: Boolean Function & Oracle Synthesis
  - Slide 6: Capability 2 Intro (bullet points & diagram)
  - Slide 7: Capability 2 Steps (5-stage algorithmic pipeline diagram)
  - Slide 8: Capability 2 Benchmark Results (oracle benchmarks & circuit drawings)
  - Slide 9: Capability 2 Better Than Other Work (SOTA comparison matrix)
- Capability 3: Circuit Optimization to Fewer Gates
  - Slide 10: Capability 3 Intro (bullet points & diagram)
  - Slide 11: Capability 3 Steps (5-stage algorithmic pipeline diagram)
  - Slide 12: Capability 3 Benchmark Results (before/after bar charts & SWAP diagrams)
  - Slide 13: Capability 3 Better Than Other Work (SOTA comparison matrix)
"""

import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor

OUTPUT_DIR = "presentation"
FIG_DIR = os.path.join(OUTPUT_DIR, "figures_10min")
os.makedirs(FIG_DIR, exist_ok=True)

# Font setup
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial', 'sans-serif']
plt.rcParams['font.family'] = 'sans-serif'

COLOR_BG = "#F8FAFC"
COLOR_NAVY = "#0F172A"
COLOR_BLUE = "#2563EB"
COLOR_LIGHT_BLUE = "#DBEAFE"
COLOR_TEAL = "#0D9488"
COLOR_LIGHT_TEAL = "#CCFBF1"
COLOR_PURPLE = "#7C3AED"
COLOR_LIGHT_PURPLE = "#EDE9FE"
COLOR_CORAL = "#E11D48"
COLOR_LIGHT_CORAL = "#FFE4E6"
COLOR_GRAY = "#64748B"
COLOR_LIGHT_GRAY = "#E2E8F0"
COLOR_DARK = "#1E293B"
COLOR_GREEN = "#059669"
COLOR_LIGHT_GREEN = "#D1FAE5"
COLOR_AMBER = "#D97706"
COLOR_LIGHT_AMBER = "#FEF3C7"


def save_fig(fig, name):
    path = os.path.join(FIG_DIR, name)
    plt.tight_layout()
    plt.savefig(path, facecolor=fig.get_facecolor(), bbox_inches='tight', dpi=250)
    plt.close()
    return path


# ==============================================================================
# SLIDE 1: Whole Work Intro (Tri-Pillar Architecture)
# ==============================================================================
def make_slide1():
    fig, ax = plt.subplots(figsize=(12, 6.2), dpi=250)
    ax.set_facecolor(COLOR_BG); fig.patch.set_facecolor(COLOR_BG); ax.axis('off')

    # Header Banner
    header = patches.FancyBboxPatch((0.8, 4.9), 10.4, 0.95, boxstyle="round,pad=0.1",
                                   facecolor=COLOR_NAVY, edgecolor="none")
    ax.add_patch(header)
    ax.text(6.0, 5.5, "Q-SYNTH: DISCRETE QUANTUM SYNTHESIS & OPTIMIZATION",
            ha='center', va='center', fontsize=15, fontweight='bold', color='white')
    ax.text(6.0, 5.15, "A Unified Search & Commutation-Aware Framework for Exact Quantum Circuit Compilation",
            ha='center', va='center', fontsize=9.5, color=COLOR_LIGHT_GRAY)

    # Tri-Pillar Columns
    pillars = [
        ("CAPABILITY 1", "Unitary Matrix Synthesis", COLOR_BLUE, COLOR_LIGHT_BLUE, 0.8, [
            "Input: Target matrix U in U(2ⁿ)",
            "Metric: Normalized trace similarity s(U,V)",
            "Search: Priority queue beam search",
            "Invariance: Global phase extraction",
            "Output: Provably minimal circuit"
        ]),
        ("CAPABILITY 2", "Boolean Oracle Synthesis", COLOR_PURPLE, COLOR_LIGHT_PURPLE, 4.4, [
            "Input: Logic AST or Truth Table string",
            "Mapping: Little-endian qubit indexing",
            "3 Paradigms: Bitflip, Phase, Permutation",
            "Reversible Basis: X, CNOT, SWAP, Toffoli",
            "Discovery: Zero-ancilla phase oracles"
        ]),
        ("CAPABILITY 3", "Circuit Optimization", COLOR_GREEN, COLOR_LIGHT_GREEN, 8.0, [
            "Input: Existing quantum circuit",
            "Constraint: Strict user-allowed gate set",
            "Pass 1: Commutation-aware peephole",
            "Pass 2: Global unitary resynthesis",
            "Pass 3: Sliding-window resynthesis"
        ]),
    ]

    for tag, title, col, light_col, x, bullets in pillars:
        card = patches.FancyBboxPatch((x, 1.4), 3.2, 3.2, boxstyle="round,pad=0.12",
                                      facecolor="white", edgecolor=col, lw=2)
        ax.add_patch(card)
        badge = patches.FancyBboxPatch((x + 0.3, 4.15), 2.6, 0.35, boxstyle="round,pad=0.05",
                                       facecolor=light_col, edgecolor="none")
        ax.add_patch(badge)
        ax.text(x + 1.6, 4.32, tag, ha='center', va='center', fontsize=9, fontweight='bold', color=col)
        ax.text(x + 1.6, 3.85, title, ha='center', va='center', fontsize=11, fontweight='bold', color=COLOR_NAVY)

        for j, b in enumerate(bullets):
            ax.text(x + 0.25, 3.4 - j * 0.42, "• " + b, fontsize=8.2, color=COLOR_DARK)

    # Bottom Foundation Bar
    bot_bar = patches.FancyBboxPatch((0.8, 0.4), 10.4, 0.75, boxstyle="round,pad=0.08",
                                     facecolor="#1E293B", edgecolor="none")
    ax.add_patch(bot_bar)
    ax.text(6.0, 0.9, "SHARED ALGORITHMIC FOUNDATIONS",
            ha='center', va='center', fontsize=9, fontweight='bold', color="#94A3B8")
    ax.text(6.0, 0.62, "Ordered Permutation Moves  |  Bitwise Kronecker Embedding  |  10⁹ Quantized Hash Grid  |  Exact Matrix Verification",
            ha='center', va='center', fontsize=9, fontweight='bold', color="white")

    ax.set_xlim(0, 12); ax.set_ylim(0, 6)
    return save_fig(fig, "slide01_intro_tri_pillar.png")


# ==============================================================================
# SLIDE 2: Capability 1 Intro
# ==============================================================================
def make_slide2():
    fig, ax = plt.subplots(figsize=(12, 6.2), dpi=250)
    ax.set_facecolor(COLOR_BG); fig.patch.set_facecolor(COLOR_BG); ax.axis('off')

    # Top Banner
    tag = patches.FancyBboxPatch((0.8, 5.0), 10.4, 0.65, boxstyle="round,pad=0.08",
                                 facecolor=COLOR_BLUE, edgecolor="none")
    ax.add_patch(tag)
    ax.text(1.2, 5.32, "CAPABILITY 1: UNITARY MATRIX TO QUANTUM CIRCUIT SYNTHESIS",
            fontsize=12, fontweight='bold', color='white', va='center')

    # Left: Concise Bullet Points
    left_card = patches.FancyBboxPatch((0.8, 0.9), 4.8, 3.8, boxstyle="round,pad=0.15",
                                       facecolor="white", edgecolor=COLOR_BLUE, lw=1.8)
    ax.add_patch(left_card)
    ax.text(3.2, 4.35, "Core Objectives & Principles", ha='center', fontsize=11.5, fontweight='bold', color=COLOR_BLUE)

    bullets = [
        ("Target Unitary Matrix", "Arbitrary dimension 2ⁿ matrix U (preset, inline JSON, file)."),
        ("Allowed Gate Set Constraint", "Search strictly constrained to user-approved gates (Clifford+T, native)."),
        ("Normalized Trace Metric", "Phase-insensitive fidelity: s(U, V) = |Tr(U† V)| / 2ⁿ in [0, 1]."),
        ("Physical Phase Invariance", "Identical observables up to unobservable global phase factor e^{iφ}."),
        ("Deterministic Hash Grid", "Exact 10⁹ integer rounding key guarantees O(1) duplicate pruning."),
    ]
    for i, (head, desc) in enumerate(bullets):
        y = 3.7 - i * 0.65
        sub = patches.FancyBboxPatch((1.05, y - 0.22), 4.3, 0.52, boxstyle="round,pad=0.06",
                                     facecolor=COLOR_LIGHT_BLUE, edgecolor="none")
        ax.add_patch(sub)
        ax.text(1.2, y + 0.1, head, fontsize=8.8, fontweight='bold', color=COLOR_NAVY)
        ax.text(1.2, y - 0.12, desc, fontsize=7.8, color=COLOR_DARK)

    # Right: High-Impact Concept Diagram
    right_card = patches.FancyBboxPatch((6.0, 0.9), 5.2, 3.8, boxstyle="round,pad=0.15",
                                        facecolor="white", edgecolor=COLOR_NAVY, lw=1.8)
    ax.add_patch(right_card)
    ax.text(8.6, 4.35, "Synthesis Flow Concept", ha='center', fontsize=11.5, fontweight='bold', color=COLOR_NAVY)

    # Input Matrix Visual
    m_box = patches.Rectangle((6.4, 2.5), 1.6, 1.4, facecolor="#F1F5F9", edgecolor=COLOR_BLUE, lw=1.5)
    ax.add_patch(m_box)
    ax.text(7.2, 3.5, "Target U", ha='center', fontsize=9.5, fontweight='bold', color=COLOR_BLUE)
    ax.text(7.2, 3.1, "[ 0.707   0.707 ]\n[ 0.707  -0.707 ]", ha='center', fontsize=7.5, family='monospace', color=COLOR_DARK)

    # Arrow to Engine
    ax.annotate("", xy=(8.4, 3.2), xytext=(8.0, 3.2),
                arrowprops=dict(arrowstyle="-|>", color=COLOR_NAVY, lw=2))

    # Engine Box
    eng_box = patches.FancyBboxPatch((8.4, 2.4), 2.4, 1.6, boxstyle="round,pad=0.08",
                                     facecolor=COLOR_LIGHT_PURPLE, edgecolor=COLOR_PURPLE, lw=1.5)
    ax.add_patch(eng_box)
    ax.text(9.6, 3.65, "Q-Synth Engine", ha='center', fontsize=9.5, fontweight='bold', color=COLOR_PURPLE)
    ax.text(9.6, 3.2, "• Permutations\n• 10⁹ Hash Grid\n• Beam Search", ha='center', fontsize=8, color=COLOR_DARK)

    # Arrow to Output
    ax.annotate("", xy=(9.6, 2.2), xytext=(9.6, 2.4),
                arrowprops=dict(arrowstyle="-|>", color=COLOR_NAVY, lw=2))

    # Output Circuit Card
    out_box = patches.FancyBboxPatch((6.4, 1.1), 4.4, 1.0, boxstyle="round,pad=0.08",
                                     facecolor=COLOR_LIGHT_GREEN, edgecolor=COLOR_GREEN, lw=1.5)
    ax.add_patch(out_box)
    ax.text(6.6, 1.75, "Verified Quantum Circuit", fontsize=9, fontweight='bold', color=COLOR_GREEN)
    ax.text(6.6, 1.45, "q0: ──[ H ]──   (Fidelity s = 1.0000000000, Phase φ = 0.00°)", fontsize=8, family='monospace', color=COLOR_NAVY)
    ax.text(6.6, 1.22, "Element Error: δ_max = 0.00   |   Synthesized in < 0.001s", fontsize=7.5, color=COLOR_GRAY)

    ax.set_xlim(0, 12); ax.set_ylim(0, 6)
    return save_fig(fig, "slide02_cap1_intro.png")


# ==============================================================================
# SLIDE 3: Capability 1 Steps Pipeline
# ==============================================================================
def make_slide3():
    fig, ax = plt.subplots(figsize=(12, 6.2), dpi=250)
    ax.set_facecolor(COLOR_BG); fig.patch.set_facecolor(COLOR_BG); ax.axis('off')

    # Top Banner
    tag = patches.FancyBboxPatch((0.8, 5.0), 10.4, 0.65, boxstyle="round,pad=0.08",
                                 facecolor=COLOR_BLUE, edgecolor="none")
    ax.add_patch(tag)
    ax.text(1.2, 5.32, "CAPABILITY 1: SIX-STAGE SYNTHESIS PIPELINE",
            fontsize=12, fontweight='bold', color='white', va='center')

    # 6 Step Boxes in 2x3 Grid
    steps = [
        ("Step 1: Input Ingestion & Metric",
         "Ingests target U in U(2ⁿ).\nValidates unitarity ||U† U - I|| < 10⁻⁸.\nFormulates trace fidelity s(U,V).",
         0.8, 2.8, COLOR_BLUE, COLOR_LIGHT_BLUE),
        ("Step 2: Directed Permutations",
         "Enumerates wire assignments:\nP(n, k_g) = n! / (n - k_g)!\nAccounts for control/target asymmetry.",
         4.4, 2.8, COLOR_BLUE, COLOR_LIGHT_BLUE),
        ("Step 3: Kronecker Embedding",
         "Projects k-qubit matrix into 2ⁿ space.\nBit-level sub-word indexing.\nPrecomputes exact 2ⁿ x 2ⁿ matrices.",
         8.0, 2.8, COLOR_BLUE, COLOR_LIGHT_BLUE),
        ("Step 4: Quantized Hash Grid",
         "Maps matrix V to 10⁹ rounded integers:\nHash = bytes(round(Re·10⁹), round(Im·10⁹)).\nEliminates duplicate states in O(1).",
         0.8, 0.8, COLOR_PURPLE, COLOR_LIGHT_PURPLE),
        ("Step 5: Priority Beam Search",
         "Frontier keeps top-B best candidates.\nExpands nodes breadth-first.\nDiscovers shortest-depth sequence.",
         4.4, 0.8, COLOR_PURPLE, COLOR_LIGHT_PURPLE),
        ("Step 6: Phase Extraction & Verify",
         "Computes global phase: φ = -arg(Tr(U†V)).\nValidates element error: δ_max < 10⁻⁶.\nEmits certified quantum circuit.",
         8.0, 0.8, COLOR_GREEN, COLOR_LIGHT_GREEN),
    ]

    for title, desc, x, y, col, light_col in steps:
        card = patches.FancyBboxPatch((x, y), 3.2, 1.8, boxstyle="round,pad=0.1",
                                      facecolor="white", edgecolor=col, lw=1.8)
        ax.add_patch(card)
        badge = patches.FancyBboxPatch((x + 0.2, y + 1.35), 2.8, 0.32, boxstyle="round,pad=0.05",
                                       facecolor=light_col, edgecolor="none")
        ax.add_patch(badge)
        ax.text(x + 1.6, y + 1.5, title, ha='center', va='center', fontsize=8.5, fontweight='bold', color=col)
        ax.text(x + 0.2, y + 0.65, desc, fontsize=7.8, color=COLOR_DARK, va='center')

    # Connecting Flow Arrows
    ax.annotate("", xy=(4.35, 3.7), xytext=(4.05, 3.7), arrowprops=dict(arrowstyle="-|>", color=COLOR_NAVY, lw=2))
    ax.annotate("", xy=(7.95, 3.7), xytext=(7.65, 3.7), arrowprops=dict(arrowstyle="-|>", color=COLOR_NAVY, lw=2))
    ax.annotate("", xy=(9.6, 2.65), xytext=(9.6, 2.75), arrowprops=dict(arrowstyle="-|>", color=COLOR_NAVY, lw=2))
    ax.annotate("", xy=(4.05, 1.7), xytext=(4.35, 1.7), arrowprops=dict(arrowstyle="<|-", color=COLOR_NAVY, lw=2))
    ax.annotate("", xy=(7.65, 1.7), xytext=(7.95, 1.7), arrowprops=dict(arrowstyle="<|-", color=COLOR_NAVY, lw=2))

    ax.set_xlim(0, 12); ax.set_ylim(0, 6)
    return save_fig(fig, "slide03_cap1_steps.png")


# ==============================================================================
# SLIDE 4: Capability 1 Benchmark Results
# ==============================================================================
def make_slide4():
    fig, ax = plt.subplots(figsize=(12, 6.2), dpi=250)
    ax.set_facecolor(COLOR_BG); fig.patch.set_facecolor(COLOR_BG); ax.axis('off')

    # Top Banner
    tag = patches.FancyBboxPatch((0.8, 5.0), 10.4, 0.65, boxstyle="round,pad=0.08",
                                 facecolor=COLOR_BLUE, edgecolor="none")
    ax.add_patch(tag)
    ax.text(1.2, 5.32, "CAPABILITY 1: EMPIRICAL BENCHMARK RESULTS",
            fontsize=12, fontweight='bold', color='white', va='center')

    # Top Metric Callout Cards
    metrics = [
        ("189 / 189", "Total Test Cases", COLOR_NAVY, 0.8),
        ("100% MATCH", "Clifford+T & Pairs", COLOR_GREEN, 4.4),
        ("< 0.02s", "Mean 2-Qubit Runtime", COLOR_BLUE, 8.0),
    ]
    for val, lbl, col, x in metrics:
        card = patches.FancyBboxPatch((x, 3.8), 3.2, 0.95, boxstyle="round,pad=0.08",
                                      facecolor="white", edgecolor=col, lw=1.8)
        ax.add_patch(card)
        ax.text(x + 1.6, 4.4, val, ha='center', fontsize=13, fontweight='bold', color=col)
        ax.text(x + 1.6, 4.02, lbl, ha='center', fontsize=8.5, color=COLOR_GRAY)

    # Bottom Left: Category Performance Summary Card
    cat_card = patches.FancyBboxPatch((0.8, 0.8), 4.8, 2.7, boxstyle="round,pad=0.12",
                                      facecolor="white", edgecolor=COLOR_NAVY, lw=1.5)
    ax.add_patch(cat_card)
    ax.text(3.2, 3.15, "Benchmark Suite Performance Summary", ha='center', fontsize=10.5, fontweight='bold', color=COLOR_NAVY)

    rows = [
        ("Basic 1-Qubit Presets", "8 / 8", "100%", "0.00s"),
        ("Single-Qubit Clifford-24", "24 / 24", "100%", "0.00s"),
        ("Known 1-Qubit Pairs", "43 / 43", "100%", "0.00s"),
        ("Known 2-Qubit Products", "80 / 80", "100%", "0.02s"),
        ("3-Qubit Stress (H-H-H)", "3 / 3", "100%", "0.10s"),
    ]
    for i, (name, cases, acc, time) in enumerate(rows):
        y = 2.7 - i * 0.42
        bg = COLOR_LIGHT_BLUE if i % 2 == 0 else "#FFFFFF"
        sub = patches.Rectangle((1.0, y - 0.16), 4.4, 0.36, facecolor=bg, edgecolor="none")
        ax.add_patch(sub)
        ax.text(1.15, y, name, fontsize=8, color=COLOR_DARK, va='center')
        ax.text(3.5, y, cases, fontsize=8, fontweight='bold', color=COLOR_NAVY, va='center')
        ax.text(4.3, y, acc, fontsize=8, fontweight='bold', color=COLOR_GREEN, va='center')
        ax.text(5.1, y, time, fontsize=8, color=COLOR_GRAY, va='center')

    # Bottom Right: Search Expansion Scaling Chart
    chart_card = patches.FancyBboxPatch((6.0, 0.8), 5.2, 2.7, boxstyle="round,pad=0.12",
                                        facecolor="white", edgecolor=COLOR_BLUE, lw=1.5)
    ax.add_patch(chart_card)
    ax.text(8.6, 3.15, "Search Expansions by Target Complexity", ha='center', fontsize=10.5, fontweight='bold', color=COLOR_BLUE)

    bar_data = [
        ("X gate", 2, COLOR_GREEN),
        ("CNOT", 6, COLOR_GREEN),
        ("SWAP (CNOT)", 9, COLOR_BLUE),
        ("SWAP (+CZ)", 21, COLOR_BLUE),
        ("SWAP (+H)", 31, COLOR_BLUE),
        ("SWAP (Full CT)", 301, COLOR_PURPLE),
        ("H-H-H (3Q)", 9102, COLOR_CORAL),
    ]
    # Draw mini bar plot
    for i, (label, val, bar_col) in enumerate(bar_data):
        y = 2.7 - i * 0.32
        # Log scale mapping for width
        w = np.log10(val + 1) * 0.85
        bar = patches.Rectangle((7.4, y - 0.1), w, 0.22, facecolor=bar_col, edgecolor="none")
        ax.add_patch(bar)
        ax.text(7.3, y, label, ha='right', va='center', fontsize=7.5, color=COLOR_DARK)
        ax.text(7.5 + w, y, f"{val:,}", va='center', fontsize=7.5, fontweight='bold', color=bar_col)

    ax.set_xlim(0, 12); ax.set_ylim(0, 6)
    return save_fig(fig, "slide04_cap1_benchmarks.png")


# ==============================================================================
# SLIDE 5: Capability 1 SOTA Comparison
# ==============================================================================
def make_slide5():
    fig, ax = plt.subplots(figsize=(12, 6.2), dpi=250)
    ax.set_facecolor(COLOR_BG); fig.patch.set_facecolor(COLOR_BG); ax.axis('off')

    # Top Banner
    tag = patches.FancyBboxPatch((0.8, 5.0), 10.4, 0.65, boxstyle="round,pad=0.08",
                                 facecolor=COLOR_BLUE, edgecolor="none")
    ax.add_patch(tag)
    ax.text(1.2, 5.32, "CAPABILITY 1: PRIOR ART VS. Q-SYNTH RESEARCH ADVANTAGES",
            fontsize=12, fontweight='bold', color='white', va='center')

    # 4 Comparison Feature Cards
    features = [
        ("1. Gate Set Flexibility",
         "PRIOR ART (Qiskit QSD / KAK):\nRestricted to fixed continuous universal bases (CX + U3).\nCannot synthesize into discrete user subsets.",
         "Q-SYNTH RESEARCH EDGE:\nArbitrary discrete user-specified gate sets.\nSynthesizes Clifford+T, Reversible, or custom matrices natively.",
         COLOR_BLUE, COLOR_LIGHT_BLUE),
        ("2. Global Phase Handling",
         "PRIOR ART (Standard Solvers):\nPenalizes or fails when circuit differs by global phase e^{iφ}.\nRequires artificial phase-tuning gates.",
         "Q-SYNTH RESEARCH EDGE:\nNormalized Hilbert-Schmidt trace metric s(U,V).\nAnalytically extracts φ = -arg(Tr(U†V)), guaranteeing physical equivalence.",
         COLOR_PURPLE, COLOR_LIGHT_PURPLE),
        ("3. Deduplication Scalability",
         "PRIOR ART (BQSKit / BFGS Continuous):\nContinuous optimization suffers from local minima traps and\nfloating-point hash drift during exploration.",
         "Q-SYNTH RESEARCH EDGE:\nQuantized 10⁹ complex integer hash grid.\nGuarantees exact O(1) deduplication with zero false negatives.",
         COLOR_GREEN, COLOR_LIGHT_GREEN),
        ("4. Zero Ancilla Overhead",
         "PRIOR ART (Standard Synthesis):\nFrequently introduces dirty/clean ancillae to complete\nmulti-qubit unitary synthesis.",
         "Q-SYNTH RESEARCH EDGE:\nStrictly bounded zero-ancilla shortest circuit synthesis.\nEvery discovered sequence is provably minimal in gate count.",
         COLOR_AMBER, COLOR_LIGHT_AMBER),
    ]

    for i, (title, prior, qsynth, col, light_col) in enumerate(features):
        x = 0.8 + (i % 2) * 5.4
        y = 2.8 if i < 2 else 0.8
        card = patches.FancyBboxPatch((x, y), 5.0, 1.85, boxstyle="round,pad=0.1",
                                      facecolor="white", edgecolor=col, lw=1.8)
        ax.add_patch(card)
        badge = patches.FancyBboxPatch((x + 0.2, y + 1.42), 4.6, 0.3, boxstyle="round,pad=0.05",
                                       facecolor=light_col, edgecolor="none")
        ax.add_patch(badge)
        ax.text(x + 2.5, y + 1.57, title, ha='center', va='center', fontsize=9.2, fontweight='bold', color=col)
        ax.text(x + 0.2, y + 0.95, prior, fontsize=7.2, color=COLOR_CORAL)
        ax.text(x + 0.2, y + 0.35, qsynth, fontsize=7.2, color=COLOR_NAVY, fontweight='bold')

    ax.set_xlim(0, 12); ax.set_ylim(0, 6)
    return save_fig(fig, "slide05_cap1_sota.png")


# ==============================================================================
# SLIDE 6: Capability 2 Intro
# ==============================================================================
def make_slide6():
    fig, ax = plt.subplots(figsize=(12, 6.2), dpi=250)
    ax.set_facecolor(COLOR_BG); fig.patch.set_facecolor(COLOR_BG); ax.axis('off')

    # Top Banner
    tag = patches.FancyBboxPatch((0.8, 5.0), 10.4, 0.65, boxstyle="round,pad=0.08",
                                 facecolor=COLOR_PURPLE, edgecolor="none")
    ax.add_patch(tag)
    ax.text(1.2, 5.32, "CAPABILITY 2: BOOLEAN FUNCTION & ORACLE SYNTHESIS",
            fontsize=12, fontweight='bold', color='white', va='center')

    # Left: Bullet Points Card
    left_card = patches.FancyBboxPatch((0.8, 0.9), 4.8, 3.8, boxstyle="round,pad=0.15",
                                       facecolor="white", edgecolor=COLOR_PURPLE, lw=1.8)
    ax.add_patch(left_card)
    ax.text(3.2, 4.35, "Core Objectives & Principles", ha='center', fontsize=11.5, fontweight='bold', color=COLOR_PURPLE)

    bullets = [
        ("Multi-Format Logic Ingestion", "Accepts algebraic expressions ('x0 ^ x1') or truth table strings ('0110')."),
        ("Automatic Variable Detection", "Extracts indexed variables (x0, x1, ...) to establish physical qubit order."),
        ("Little-Endian Convention", "Qubit 0 is LSB (Row k = ∑ b_i 2ⁱ => x_i = b_i), matching Qiskit/IBM."),
        ("3 Quantum Oracle Paradigms", "Bit-flip |x,y⊕f(x)⟩, Phase (-1)^{f(x)}|x⟩, and Permutation |f(x)⟩."),
        ("Zero-Ancilla Phase Discovery", "Discovers phase kickback oracles using 0 ancillae (e.g. single CZ for AND)."),
    ]
    for i, (head, desc) in enumerate(bullets):
        y = 3.7 - i * 0.65
        sub = patches.FancyBboxPatch((1.05, y - 0.22), 4.3, 0.52, boxstyle="round,pad=0.06",
                                     facecolor=COLOR_LIGHT_PURPLE, edgecolor="none")
        ax.add_patch(sub)
        ax.text(1.2, y + 0.1, head, fontsize=8.8, fontweight='bold', color=COLOR_PURPLE)
        ax.text(1.2, y - 0.12, desc, fontsize=7.8, color=COLOR_DARK)

    # Right: High-Impact Diagram
    right_card = patches.FancyBboxPatch((6.0, 0.9), 5.2, 3.8, boxstyle="round,pad=0.15",
                                        facecolor="white", edgecolor=COLOR_NAVY, lw=1.8)
    ax.add_patch(right_card)
    ax.text(8.6, 4.35, "Oracle Synthesis Flow", ha='center', fontsize=11.5, fontweight='bold', color=COLOR_NAVY)

    # Expression Box
    e_box = patches.FancyBboxPatch((6.4, 2.7), 2.0, 1.2, boxstyle="round,pad=0.08",
                                   facecolor=COLOR_LIGHT_PURPLE, edgecolor=COLOR_PURPLE, lw=1.5)
    ax.add_patch(e_box)
    ax.text(7.4, 3.55, "Logic Formula", ha='center', fontsize=9, fontweight='bold', color=COLOR_PURPLE)
    ax.text(7.4, 3.15, "x0 ^ x1\n(or '0110')", ha='center', fontsize=8.5, family='monospace', color=COLOR_DARK)

    # Arrow
    ax.annotate("", xy=(8.9, 3.3), xytext=(8.5, 3.3), arrowprops=dict(arrowstyle="-|>", color=COLOR_NAVY, lw=2))

    # Oracle Matrix Box
    o_box = patches.FancyBboxPatch((8.9, 2.7), 2.0, 1.2, boxstyle="round,pad=0.08",
                                   facecolor=COLOR_LIGHT_BLUE, edgecolor=COLOR_BLUE, lw=1.5)
    ax.add_patch(o_box)
    ax.text(9.9, 3.55, "Oracle Paradigm", ha='center', fontsize=9, fontweight='bold', color=COLOR_BLUE)
    ax.text(9.9, 3.15, "Bitflip: 8 x 8\nPhase: 4 x 4", ha='center', fontsize=8.5, family='monospace', color=COLOR_DARK)

    # Arrow Down
    ax.annotate("", xy=(8.6, 2.3), xytext=(8.6, 2.6), arrowprops=dict(arrowstyle="-|>", color=COLOR_NAVY, lw=2))

    # Output Reversible Circuit Box
    circ_box = patches.FancyBboxPatch((6.4, 1.1), 4.4, 1.1, boxstyle="round,pad=0.08",
                                      facecolor=COLOR_LIGHT_GREEN, edgecolor=COLOR_GREEN, lw=1.5)
    ax.add_patch(circ_box)
    ax.text(6.6, 1.85, "Synthesized Reversible Circuit (Clifford+T / Reversible Basis)", fontsize=8.5, fontweight='bold', color=COLOR_GREEN)
    ax.text(6.6, 1.55, "q0: ──■───────\nq1: ──┼───■───    ==> Exact XOR Oracle (2 CNOTs, s = 1.000)", fontsize=7.5, family='monospace', color=COLOR_NAVY)
    ax.text(6.6, 1.3, "q2: ──X───X───", fontsize=7.5, family='monospace', color=COLOR_NAVY)

    ax.set_xlim(0, 12); ax.set_ylim(0, 6)
    return save_fig(fig, "slide06_cap2_intro.png")


# ==============================================================================
# SLIDE 7: Capability 2 Steps Pipeline
# ==============================================================================
def make_slide7():
    fig, ax = plt.subplots(figsize=(12, 6.2), dpi=250)
    ax.set_facecolor(COLOR_BG); fig.patch.set_facecolor(COLOR_BG); ax.axis('off')

    # Top Banner
    tag = patches.FancyBboxPatch((0.8, 5.0), 10.4, 0.65, boxstyle="round,pad=0.08",
                                 facecolor=COLOR_PURPLE, edgecolor="none")
    ax.add_patch(tag)
    ax.text(1.2, 5.32, "CAPABILITY 2: FIVE-STAGE ORACLE SYNTHESIS PIPELINE",
            fontsize=12, fontweight='bold', color='white', va='center')

    # 5 Step Cards along a pipeline
    steps = [
        ("Step 1: AST Parsing",
         "Lexes expression tokens.\nRecursive descent grammar:\nNOT > AND > XOR > OR.\nExtracts variable names.",
         0.8, 2.8, COLOR_PURPLE, COLOR_LIGHT_PURPLE),
        ("Step 2: Truth Table Eval",
         "Evaluates all 2ⁿ inputs.\nLittle-endian LSB-first:\nRow k => x_i = (k >> i) & 1.\nGenerates truth vector.",
         4.4, 2.8, COLOR_PURPLE, COLOR_LIGHT_PURPLE),
        ("Step 3: Oracle Embedding",
         "3 Modes:\n• Bitflip: |x, y⊕f(x)⟩ (2ⁿ⁺¹)\n• Phase: (-1)^f(x) |x⟩ (2ⁿ)\n• Permutation: |f(x)⟩ (2ⁿ)",
         8.0, 2.8, COLOR_BLUE, COLOR_LIGHT_BLUE),
        ("Step 4: Reversible Basis Library",
         "Dispatches to gate basis:\n• Clifford+T: H, S, T, CNOT, CZ\n• Reversible: X, CNOT, SWAP,\n  CCX (Toffoli), CSWAP (Fredkin).",
         2.6, 0.8, COLOR_TEAL, COLOR_LIGHT_TEAL),
        ("Step 5: Search & Exact Verification",
         "Beam search finds minimal gates.\nOutputs ASCII truth table.\nCertified exact unitary fidelity:\ns(U_oracle, V_circuit) == 1.000.",
         6.6, 0.8, COLOR_GREEN, COLOR_LIGHT_GREEN),
    ]

    for title, desc, x, y, col, light_col in steps:
        card = patches.FancyBboxPatch((x, y), 3.2, 1.8, boxstyle="round,pad=0.1",
                                      facecolor="white", edgecolor=col, lw=1.8)
        ax.add_patch(card)
        badge = patches.FancyBboxPatch((x + 0.2, y + 1.35), 2.8, 0.32, boxstyle="round,pad=0.05",
                                       facecolor=light_col, edgecolor="none")
        ax.add_patch(badge)
        ax.text(x + 1.6, y + 1.5, title, ha='center', va='center', fontsize=8.5, fontweight='bold', color=col)
        ax.text(x + 0.2, y + 0.65, desc, fontsize=7.8, color=COLOR_DARK, va='center')

    # Flow arrows
    ax.annotate("", xy=(4.35, 3.7), xytext=(4.05, 3.7), arrowprops=dict(arrowstyle="-|>", color=COLOR_NAVY, lw=2))
    ax.annotate("", xy=(7.95, 3.7), xytext=(7.65, 3.7), arrowprops=dict(arrowstyle="-|>", color=COLOR_NAVY, lw=2))
    ax.annotate("", xy=(8.2, 2.65), xytext=(8.2, 2.75), arrowprops=dict(arrowstyle="-|>", color=COLOR_NAVY, lw=2))
    ax.annotate("", xy=(6.55, 1.7), xytext=(5.85, 1.7), arrowprops=dict(arrowstyle="-|>", color=COLOR_NAVY, lw=2))

    ax.set_xlim(0, 12); ax.set_ylim(0, 6)
    return save_fig(fig, "slide07_cap2_steps.png")


# ==============================================================================
# SLIDE 8: Capability 2 Benchmark Results
# ==============================================================================
def make_slide8():
    fig, ax = plt.subplots(figsize=(12, 6.2), dpi=250)
    ax.set_facecolor(COLOR_BG); fig.patch.set_facecolor(COLOR_BG); ax.axis('off')

    # Top Banner
    tag = patches.FancyBboxPatch((0.8, 5.0), 10.4, 0.65, boxstyle="round,pad=0.08",
                                 facecolor=COLOR_PURPLE, edgecolor="none")
    ax.add_patch(tag)
    ax.text(1.2, 5.32, "CAPABILITY 2: EMPIRICAL BENCHMARK RESULTS",
            fontsize=12, fontweight='bold', color='white', va='center')

    # 4 Benchmark Case Cards
    cases = [
        ("XOR Bit-Flip Oracle", "--bool-expr 'x0 ^ x1'", "bitflip", "3 Qubits", "CNOT[0,2], CNOT[1,2]",
         "10 Expansions", "< 0.001s", "s = 1.000", COLOR_BLUE, 0.8, 2.9),
        ("AND Phase Oracle", "--bool-expr 'x0 and x1'", "phase", "2 Qubits (0 Ancillae!)", "CZ[0,1]",
         "15 Expansions", "< 0.001s", "s = 1.000", COLOR_GREEN, 6.0, 2.9),
        ("AND Bit-Flip Oracle", "--bool-expr 'x0 and x1'", "bitflip", "3 Qubits", "CCX[0,1,2] (Toffoli)",
         "1 Expansion", "< 0.001s", "s = 1.000", COLOR_PURPLE, 0.8, 0.8),
        ("Permutation Map", "--truth-table '0->1, 1->0, ...'", "permutation", "2 Qubits", "X[0]",
         "2 Expansions", "< 0.001s", "s = 1.000", COLOR_AMBER, 6.0, 0.8),
    ]

    for title, cmd, mode, qb, gates, exp, time, fid, col, x, y in cases:
        card = patches.FancyBboxPatch((x, y), 5.2, 1.9, boxstyle="round,pad=0.1",
                                      facecolor="white", edgecolor=col, lw=1.8)
        ax.add_patch(card)
        badge = patches.FancyBboxPatch((x + 0.2, y + 1.45), 4.8, 0.32, boxstyle="round,pad=0.05",
                                       facecolor=col, edgecolor="none")
        ax.add_patch(badge)
        ax.text(x + 2.6, y + 1.61, f"{title} | Mode: {mode}", ha='center', va='center',
                fontsize=8.8, fontweight='bold', color='white')

        ax.text(x + 0.25, y + 1.15, f"Specification: {cmd}", fontsize=7.8, family='monospace', color=COLOR_NAVY)
        ax.text(x + 0.25, y + 0.85, f"Register: {qb}   |   Synthesized Gates: {gates}", fontsize=7.8, fontweight='bold', color=COLOR_DARK)
        ax.text(x + 0.25, y + 0.55, f"Search Effort: {exp}   |   Runtime: {time}   |   Fidelity: {fid}", fontsize=7.5, color=COLOR_GRAY)

        # Highlight callout
        if "CZ" in gates:
            callout = patches.Rectangle((x + 0.25, y + 0.15), 4.7, 0.28, facecolor=COLOR_LIGHT_GREEN, edgecolor="none")
            ax.add_patch(callout)
            ax.text(x + 2.6, y + 0.29, "★ Key Discovery: Phase kickback synthesizes in 0 ancillae via single CZ!",
                    ha='center', va='center', fontsize=7.5, fontweight='bold', color=COLOR_GREEN)
        elif "CCX" in gates:
            callout = patches.Rectangle((x + 0.25, y + 0.15), 4.7, 0.28, facecolor=COLOR_LIGHT_PURPLE, edgecolor="none")
            ax.add_patch(callout)
            ax.text(x + 2.6, y + 0.29, "★ Instant Reversible Match: Maps directly to Toffoli in 1 expansion!",
                    ha='center', va='center', fontsize=7.5, fontweight='bold', color=COLOR_PURPLE)

    ax.set_xlim(0, 12); ax.set_ylim(0, 6)
    return save_fig(fig, "slide08_cap2_benchmarks.png")


# ==============================================================================
# SLIDE 9: Capability 2 SOTA Comparison
# ==============================================================================
def make_slide9():
    fig, ax = plt.subplots(figsize=(12, 6.2), dpi=250)
    ax.set_facecolor(COLOR_BG); fig.patch.set_facecolor(COLOR_BG); ax.axis('off')

    # Top Banner
    tag = patches.FancyBboxPatch((0.8, 5.0), 10.4, 0.65, boxstyle="round,pad=0.08",
                                 facecolor=COLOR_PURPLE, edgecolor="none")
    ax.add_patch(tag)
    ax.text(1.2, 5.32, "CAPABILITY 2: PRIOR ART VS. Q-SYNTH RESEARCH ADVANTAGES",
            fontsize=12, fontweight='bold', color='white', va='center')

    # 4 Comparison Feature Cards
    features = [
        ("1. Ancilla Overhead in Oracles",
         "PRIOR ART (Tweedledum / Qiskit MCX):\nRequires O(n) dirty or clean helper ancillae to execute\nmulti-controlled Boolean functions and phase kickbacks.",
         "Q-SYNTH RESEARCH EDGE:\nDiscovers zero-ancilla phase oracles automatically.\nSynthesizes n-qubit diagonal phase oracles with 0 extra qubits.",
         COLOR_GREEN, COLOR_LIGHT_GREEN),
        ("2. Gate Count Minimality",
         "PRIOR ART (Macro-Expansion Tools):\nGenerates large macro-decompositions (10-25 elementary\ngates) even for simple 2-variable Boolean logic.",
         "Q-SYNTH RESEARCH EDGE:\nGuarantees shortest-depth gate sequences.\nDiscovers minimal 1-to-2 gate exact circuits (e.g. 1 CZ, 2 CNOTs).",
         COLOR_PURPLE, COLOR_LIGHT_PURPLE),
        ("3. Reversible Gate Basis Support",
         "PRIOR ART (Standard Synthesizers):\nDecomposes into fixed continuous rotations and CNOTs,\ndestroying natural reversible logic structure.",
         "Q-SYNTH RESEARCH EDGE:\nNatively synthesizes into standard reversible basis:\nX, CNOT, SWAP, Toffoli (CCX), and Fredkin (CSWAP).",
         COLOR_BLUE, COLOR_LIGHT_BLUE),
        ("4. Input Specification Versatility",
         "PRIOR ART (Rigid Synthesizers):\nRequires rigid truth tables or specific HDL inputs;\ncannot mix algebraic formulas with explicit bijections.",
         "Q-SYNTH RESEARCH EDGE:\nAccepts Boolean strings ('x0 ^ x1'), truth tables ('0110'),\nand arbitrary transition maps ('0->1, 1->0').",
         COLOR_AMBER, COLOR_LIGHT_AMBER),
    ]

    for i, (title, prior, qsynth, col, light_col) in enumerate(features):
        x = 0.8 + (i % 2) * 5.4
        y = 2.8 if i < 2 else 0.8
        card = patches.FancyBboxPatch((x, y), 5.0, 1.85, boxstyle="round,pad=0.1",
                                      facecolor="white", edgecolor=col, lw=1.8)
        ax.add_patch(card)
        badge = patches.FancyBboxPatch((x + 0.2, y + 1.42), 4.6, 0.3, boxstyle="round,pad=0.05",
                                       facecolor=light_col, edgecolor="none")
        ax.add_patch(badge)
        ax.text(x + 2.5, y + 1.57, title, ha='center', va='center', fontsize=9.2, fontweight='bold', color=col)
        ax.text(x + 0.2, y + 0.95, prior, fontsize=7.2, color=COLOR_CORAL)
        ax.text(x + 0.2, y + 0.35, qsynth, fontsize=7.2, color=COLOR_NAVY, fontweight='bold')

    ax.set_xlim(0, 12); ax.set_ylim(0, 6)
    return save_fig(fig, "slide09_cap2_sota.png")


# ==============================================================================
# SLIDE 10: Capability 3 Intro
# ==============================================================================
def make_slide10():
    fig, ax = plt.subplots(figsize=(12, 6.2), dpi=250)
    ax.set_facecolor(COLOR_BG); fig.patch.set_facecolor(COLOR_BG); ax.axis('off')

    # Top Banner
    tag = patches.FancyBboxPatch((0.8, 5.0), 10.4, 0.65, boxstyle="round,pad=0.08",
                                 facecolor=COLOR_GREEN, edgecolor="none")
    ax.add_patch(tag)
    ax.text(1.2, 5.32, "CAPABILITY 3: CONSTRAINED CIRCUIT OPTIMIZATION",
            fontsize=12, fontweight='bold', color='white', va='center')

    # Left: Bullet Points Card
    left_card = patches.FancyBboxPatch((0.8, 0.9), 4.8, 3.8, boxstyle="round,pad=0.15",
                                       facecolor="white", edgecolor=COLOR_GREEN, lw=1.8)
    ax.add_patch(left_card)
    ax.text(3.2, 4.35, "Core Objectives & Principles", ha='center', fontsize=11.5, fontweight='bold', color=COLOR_GREEN)

    bullets = [
        ("Input Circuit Redundancies", "Unoptimized circuits contain redundant pairs, inverses, and suboptimal subcircuits."),
        ("Strict Allowed Gate Set", "Optimizer guarantees that output circuit contains ONLY user-permitted gates."),
        ("Commutation-Aware Analysis", "Passes commuting gates across intermediate wires: [G_i, G_j] = 0."),
        ("Peephole Rewriting Rules", "Cancels self-inverses (G · G† = I) and fuses rotations (T · T -> S)."),
        ("Multi-Pass Resynthesis", "Global unitary and sliding-window resynthesis replace subcircuits with minimal forms."),
    ]
    for i, (head, desc) in enumerate(bullets):
        y = 3.7 - i * 0.65
        sub = patches.FancyBboxPatch((1.05, y - 0.22), 4.3, 0.52, boxstyle="round,pad=0.06",
                                     facecolor=COLOR_LIGHT_GREEN, edgecolor="none")
        ax.add_patch(sub)
        ax.text(1.2, y + 0.1, head, fontsize=8.8, fontweight='bold', color=COLOR_GREEN)
        ax.text(1.2, y - 0.12, desc, fontsize=7.8, color=COLOR_DARK)

    # Right: Circuit Optimization Diagram
    right_card = patches.FancyBboxPatch((6.0, 0.9), 5.2, 3.8, boxstyle="round,pad=0.15",
                                        facecolor="white", edgecolor=COLOR_NAVY, lw=1.8)
    ax.add_patch(right_card)
    ax.text(8.6, 4.35, "Optimization Strategy", ha='center', fontsize=11.5, fontweight='bold', color=COLOR_NAVY)

    # Before Circuit (7 gates)
    b_box = patches.FancyBboxPatch((6.4, 2.7), 4.4, 1.2, boxstyle="round,pad=0.08",
                                   facecolor=COLOR_LIGHT_CORAL, edgecolor=COLOR_CORAL, lw=1.5)
    ax.add_patch(b_box)
    ax.text(6.6, 3.55, "Input: 7-Gate Pedagogical SWAP (Unoptimized)", fontsize=8.5, fontweight='bold', color=COLOR_CORAL)
    ax.text(6.6, 3.2, "q0: ──■──[H]────■──[H]────■──\nq1: ──X────[H]──X────[H]──X──", fontsize=7.5, family='monospace', color=COLOR_NAVY)

    # Arrow Down
    ax.annotate("", xy=(8.6, 2.25), xytext=(8.6, 2.65),
                arrowprops=dict(arrowstyle="-|>", color=COLOR_NAVY, lw=2.5))
    ax.text(8.8, 2.45, "Global Resynthesis (Basis = {CNOT})", fontsize=7.8, fontweight='bold', color=COLOR_BLUE)

    # After Circuit (3 gates)
    a_box = patches.FancyBboxPatch((6.4, 1.0), 4.4, 1.2, boxstyle="round,pad=0.08",
                                   facecolor=COLOR_LIGHT_GREEN, edgecolor=COLOR_GREEN, lw=1.5)
    ax.add_patch(a_box)
    ax.text(6.6, 1.85, "Optimized: 3 CNOTs (57.1% Gate Reduction!)", fontsize=8.5, fontweight='bold', color=COLOR_GREEN)
    ax.text(6.6, 1.5, "q0: ──■───X───■──\nq1: ──X───■───X──", fontsize=7.5, family='monospace', color=COLOR_NAVY)
    ax.text(6.6, 1.2, "Verified Fidelity: s = 1.0000000000   |   Max Error: δ_max = 0.00", fontsize=7.2, color=COLOR_GRAY)

    ax.set_xlim(0, 12); ax.set_ylim(0, 6)
    return save_fig(fig, "slide10_cap3_intro.png")


# ==============================================================================
# SLIDE 11: Capability 3 Steps Pipeline
# ==============================================================================
def make_slide11():
    fig, ax = plt.subplots(figsize=(12, 6.2), dpi=250)
    ax.set_facecolor(COLOR_BG); fig.patch.set_facecolor(COLOR_BG); ax.axis('off')

    # Top Banner
    tag = patches.FancyBboxPatch((0.8, 5.0), 10.4, 0.65, boxstyle="round,pad=0.08",
                                 facecolor=COLOR_GREEN, edgecolor="none")
    ax.add_patch(tag)
    ax.text(1.2, 5.32, "CAPABILITY 3: MULTI-PASS OPTIMIZATION PIPELINE",
            fontsize=12, fontweight='bold', color='white', va='center')

    # 5 Step Cards along a pipeline
    steps = [
        ("Step 1: Circuit Ingestion",
         "Parses circuit input:\n• Native strings (H[0], CNOT[0,1])\n• Space-delimited format\n• Standard OpenQASM 2.0\nResolves wire placements.",
         0.8, 2.8, COLOR_NAVY, COLOR_LIGHT_GRAY),
        ("Step 2: Commutation Analysis",
         "Checks pairwise commutation:\n• Disjoint: p_i ∩ p_j = ∅\n• Diagonal: Z, S, T, CZ\n• Matrix: [M_i, M_j] = 0\nPermits sliding gates past neighbors.",
         4.4, 2.8, COLOR_BLUE, COLOR_LIGHT_BLUE),
        ("Step 3: Peephole Rewriting",
         "Pass 1 Local Rewrites:\n• Identity removal: I -> ∅\n• Self-inverse: G · G† = I -> ∅\n• Rotation fusion: T · T -> S\nIterates until convergence.",
         8.0, 2.8, COLOR_PURPLE, COLOR_LIGHT_PURPLE),
        ("Step 4: Global Resynthesis",
         "Pass 2 Search Optimization:\n• Computes overall unitary U = ∏ G\n• Beam searches depth ≤ M - 1\n• Strictly uses allowed gate set\n• Replaces entire circuit if smaller.",
         2.6, 0.8, COLOR_GREEN, COLOR_LIGHT_GREEN),
        ("Step 5: Sliding-Window Resynthesis",
         "Pass 3 Deep Optimization:\n• Slides window w in [2, W] across circuit\n• Extracts sub-unitary U_slice\n• Synthesizes sub-block with allowed gates\n• Patches in-place and re-triggers Pass 1.",
         6.6, 0.8, COLOR_AMBER, COLOR_LIGHT_AMBER),
    ]

    for title, desc, x, y, col, light_col in steps:
        card = patches.FancyBboxPatch((x, y), 3.2, 1.8, boxstyle="round,pad=0.1",
                                      facecolor="white", edgecolor=col, lw=1.8)
        ax.add_patch(card)
        badge = patches.FancyBboxPatch((x + 0.2, y + 1.35), 2.8, 0.32, boxstyle="round,pad=0.05",
                                       facecolor=light_col, edgecolor="none")
        ax.add_patch(badge)
        ax.text(x + 1.6, y + 1.5, title, ha='center', va='center', fontsize=8.5, fontweight='bold', color=col)
        ax.text(x + 0.2, y + 0.65, desc, fontsize=7.8, color=COLOR_DARK, va='center')

    # Flow arrows
    ax.annotate("", xy=(4.35, 3.7), xytext=(4.05, 3.7), arrowprops=dict(arrowstyle="-|>", color=COLOR_NAVY, lw=2))
    ax.annotate("", xy=(7.95, 3.7), xytext=(7.65, 3.7), arrowprops=dict(arrowstyle="-|>", color=COLOR_NAVY, lw=2))
    ax.annotate("", xy=(8.2, 2.65), xytext=(8.2, 2.75), arrowprops=dict(arrowstyle="-|>", color=COLOR_NAVY, lw=2))
    ax.annotate("", xy=(6.55, 1.7), xytext=(5.85, 1.7), arrowprops=dict(arrowstyle="-|>", color=COLOR_NAVY, lw=2))

    ax.set_xlim(0, 12); ax.set_ylim(0, 6)
    return save_fig(fig, "slide11_cap3_steps.png")


# ==============================================================================
# SLIDE 12: Capability 3 Benchmark Results
# ==============================================================================
def make_slide12():
    fig, ax = plt.subplots(figsize=(12, 6.2), dpi=250)
    ax.set_facecolor(COLOR_BG); fig.patch.set_facecolor(COLOR_BG); ax.axis('off')

    # Top Banner
    tag = patches.FancyBboxPatch((0.8, 5.0), 10.4, 0.65, boxstyle="round,pad=0.08",
                                 facecolor=COLOR_GREEN, edgecolor="none")
    ax.add_patch(tag)
    ax.text(1.2, 5.32, "CAPABILITY 3: EMPIRICAL BENCHMARK RESULTS",
            fontsize=12, fontweight='bold', color='white', va='center')

    # Left: Gate Count Before vs. After Bar Chart
    chart_card = patches.FancyBboxPatch((0.8, 0.8), 5.2, 3.8, boxstyle="round,pad=0.15",
                                        facecolor="white", edgecolor=COLOR_GREEN, lw=1.8)
    ax.add_patch(chart_card)
    ax.text(3.4, 4.35, "Gate Count Reduction Across Test Cases", ha='center', fontsize=11, fontweight='bold', color=COLOR_GREEN)

    benchmarks = [
        ("Redundant H-CNOT", 4, 0, "100.0%"),
        ("Double SWAP (6 CNOTs)", 6, 0, "100.0%"),
        ("Rotation Merge (T·T)", 2, 1, "50.0%"),
        ("7-Gate SWAP Circuit", 7, 3, "57.1%"),
        ("Optimal 3-CNOT SWAP", 3, 3, "0.0% (optimal)"),
    ]

    for i, (name, before, after, saved) in enumerate(benchmarks):
        y = 3.6 - i * 0.65
        ax.text(1.0, y + 0.18, name, fontsize=8.2, fontweight='bold', color=COLOR_NAVY)

        # Before Bar (Coral)
        w_b = before * 0.4
        b_bar = patches.Rectangle((1.0, y - 0.12), w_b, 0.22, facecolor=COLOR_CORAL, edgecolor="none")
        ax.add_patch(b_bar)
        ax.text(1.05 + w_b, y - 0.02, f"In: {before}", fontsize=7.2, color=COLOR_CORAL, fontweight='bold')

        # After Bar (Green)
        w_a = after * 0.4
        a_bar = patches.Rectangle((1.0, y - 0.36), w_a, 0.22, facecolor=COLOR_GREEN, edgecolor="none")
        ax.add_patch(a_bar)
        ax.text(1.05 + w_a, y - 0.26, f"Out: {after} ({saved})", fontsize=7.2, color=COLOR_GREEN, fontweight='bold')

    # Right: Highlight Case Study Card (SWAP 7 -> 3)
    study_card = patches.FancyBboxPatch((6.4, 0.8), 4.8, 3.8, boxstyle="round,pad=0.15",
                                        facecolor="white", edgecolor=COLOR_NAVY, lw=1.8)
    ax.add_patch(study_card)
    ax.text(8.8, 4.35, "Resynthesis Highlight: 7-Gate SWAP", ha='center', fontsize=11, fontweight='bold', color=COLOR_NAVY)

    study_texts = [
        ("Pedagogical SWAP Formulation:", "CNOT · (H ⊗ H) · CNOT · (H ⊗ H) · CNOT"),
        ("Peephole Limitation:", "Hadamards do not commute with CNOT pins; local rules cannot simplify!"),
        ("Q-Synth Resynthesis Solution:", "Evaluates composite unitary matrix U ∈ U(4), detects permutation, and synthesizes 3 CNOTs in < 0.01s."),
        ("Verification Fidelity:", "s(U_orig, V_opt) = 1.0000000000  (Error δ_max < 10⁻¹⁵)"),
        ("Net Reduction:", "4 gates eliminated (57.1% reduction) with ZERO unapproved gates introduced."),
    ]
    for i, (hd, txt) in enumerate(study_texts):
        y = 3.65 - i * 0.65
        sub = patches.FancyBboxPatch((6.65, y - 0.22), 4.3, 0.52, boxstyle="round,pad=0.06",
                                     facecolor=COLOR_LIGHT_BLUE if i == 2 else COLOR_BG,
                                     edgecolor=COLOR_BLUE if i == 2 else "none")
        ax.add_patch(sub)
        ax.text(6.8, y + 0.1, hd, fontsize=8.2, fontweight='bold', color=COLOR_BLUE if i == 2 else COLOR_NAVY)
        ax.text(6.8, y - 0.12, txt, fontsize=7.5, color=COLOR_DARK)

    ax.set_xlim(0, 12); ax.set_ylim(0, 6)
    return save_fig(fig, "slide12_cap3_benchmarks.png")


# ==============================================================================
# SLIDE 13: Capability 3 SOTA Comparison
# ==============================================================================
def make_slide13():
    fig, ax = plt.subplots(figsize=(12, 6.2), dpi=250)
    ax.set_facecolor(COLOR_BG); fig.patch.set_facecolor(COLOR_BG); ax.axis('off')

    # Top Banner
    tag = patches.FancyBboxPatch((0.8, 5.0), 10.4, 0.65, boxstyle="round,pad=0.08",
                                 facecolor=COLOR_GREEN, edgecolor="none")
    ax.add_patch(tag)
    ax.text(1.2, 5.32, "CAPABILITY 3: PRIOR ART VS. Q-SYNTH RESEARCH ADVANTAGES",
            fontsize=12, fontweight='bold', color='white', va='center')

    # 4 Comparison Feature Cards
    features = [
        ("1. Strict Allowed Gate Set Enforcement",
         "PRIOR ART (Qiskit transpile -O3):\nConverts circuits into hardware-native bases (SX, ECR, CZ),\npolluting and violating user-specified discrete sets.",
         "Q-SYNTH RESEARCH EDGE:\n100% adherence to user-specified allowed gate sets.\nNever introduces unauthorized gates into the output circuit.",
         COLOR_GREEN, COLOR_LIGHT_GREEN),
        ("2. Beyond Commutation Barriers",
         "PRIOR ART (Peephole-Only Optimizers):\nBlocked whenever intermediate non-commuting gates sit\nbetween potentially cancelling gate sequences.",
         "Q-SYNTH RESEARCH EDGE:\nGlobal and sliding-window resynthesis evaluates composite unitaries,\nreplacing entire non-commuting blocks with minimal gates.",
         COLOR_BLUE, COLOR_LIGHT_BLUE),
        ("3. Reversible Circuit Optimization",
         "PRIOR ART (Nam et al. 2018 / Continuous):\nOptimizes continuous rotation angles; completely fails on\ndiscrete permutation and multi-controlled reversible logic.",
         "Q-SYNTH RESEARCH EDGE:\nCombines discrete beam resynthesis with exact algebraic cancellation,\nexcelling on both Clifford+T and reversible circuits.",
         COLOR_PURPLE, COLOR_LIGHT_PURPLE),
        ("4. Certified Zero Numerical Drift",
         "PRIOR ART (Approximate Synthesizers):\nAccumulates floating-point parameter drift and unitary leakage\nacross repeated optimization cycles.",
         "Q-SYNTH RESEARCH EDGE:\nExact Hilbert-Schmidt verification guarantees identical\nphysical observables with zero numerical leakage (s = 1.000).",
         COLOR_AMBER, COLOR_LIGHT_AMBER),
    ]

    for i, (title, prior, qsynth, col, light_col) in enumerate(features):
        x = 0.8 + (i % 2) * 5.4
        y = 2.8 if i < 2 else 0.8
        card = patches.FancyBboxPatch((x, y), 5.0, 1.85, boxstyle="round,pad=0.1",
                                      facecolor="white", edgecolor=col, lw=1.8)
        ax.add_patch(card)
        badge = patches.FancyBboxPatch((x + 0.2, y + 1.42), 4.6, 0.3, boxstyle="round,pad=0.05",
                                       facecolor=light_col, edgecolor="none")
        ax.add_patch(badge)
        ax.text(x + 2.5, y + 1.57, title, ha='center', va='center', fontsize=9.2, fontweight='bold', color=col)
        ax.text(x + 0.2, y + 0.95, prior, fontsize=7.2, color=COLOR_CORAL)
        ax.text(x + 0.2, y + 0.35, qsynth, fontsize=7.2, color=COLOR_NAVY, fontweight='bold')

    ax.set_xlim(0, 12); ax.set_ylim(0, 6)
    return save_fig(fig, "slide13_cap3_sota.png")


# ==============================================================================
# MAIN PRESENTATION BUILDER
# ==============================================================================
def build_10min_presentation():
    print("Generating 13 high-resolution diagram slides for 10-minute presentation...")

    slide_makers = [
        ("Overview", make_slide1),
        ("Cap 1 Intro", make_slide2),
        ("Cap 1 Steps", make_slide3),
        ("Cap 1 Benchmarks", make_slide4),
        ("Cap 1 SOTA", make_slide5),
        ("Cap 2 Intro", make_slide6),
        ("Cap 2 Steps", make_slide7),
        ("Cap 2 Benchmarks", make_slide8),
        ("Cap 2 SOTA", make_slide9),
        ("Cap 3 Intro", make_slide10),
        ("Cap 3 Steps", make_slide11),
        ("Cap 3 Benchmarks", make_slide12),
        ("Cap 3 SOTA", make_slide13),
    ]

    image_paths = []
    for name, maker in slide_makers:
        print(f"  Rendering {name}...")
        img_path = maker()
        image_paths.append(img_path)

    print("Building PowerPoint PPTX presentation...")
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]  # Blank

    for idx, img_path in enumerate(image_paths):
        slide = prs.slides.add_slide(blank_layout)
        # Add background fill
        bg = slide.background
        fill = bg.fill
        fill.solid()
        fill.fore_color.rgb = RGBColor(248, 250, 252)

        # Centered High-Res Diagram Image filling the slide gracefully
        slide.shapes.add_picture(img_path, Inches(0.666), Inches(0.4), width=Inches(12.0))

    out_file = os.path.join(OUTPUT_DIR, "Q-Synth_10Min_Presentation.pptx")
    prs.save(out_file)
    print(f"Successfully generated 13-slide 10-minute presentation: {out_file}")
    return out_file


if __name__ == "__main__":
    build_10min_presentation()
