"""Generates the 20-slide research-focused presentation for Q-Synth.

Structure:
- Slide 1: Opening Title & Tri-Pillar Architecture
- Slides 2-7: Capability 1 Steps (Unitary Synthesis)
- Slide 8: Capability 1 SOTA Comparison ("Where this is beyond everything else")
- Slides 9-13: Capability 2 Steps (Boolean & Truth Table Synthesis)
- Slide 14: Capability 2 SOTA Comparison ("Where this is beyond everything else")
- Slides 15-19: Capability 3 Steps (Circuit Optimization)
- Slide 20: Capability 3 SOTA Comparison ("Where this is beyond everything else")
"""

import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor

OUTPUT_DIR = "presentation"
FIG_DIR = os.path.join(OUTPUT_DIR, "figures_research")
os.makedirs(FIG_DIR, exist_ok=True)

# Font and color setup
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


def save_fig(fig, name):
    path = os.path.join(FIG_DIR, name)
    plt.tight_layout()
    plt.savefig(path, facecolor=fig.get_facecolor(), bbox_inches='tight', dpi=250)
    plt.close()
    return path


# ==============================================================================
# SLIDE 1: OPENING TITLE & TRI-PILLAR ARCHITECTURE
# ==============================================================================
def make_slide1():
    fig, ax = plt.subplots(figsize=(12, 6.2), dpi=250)
    ax.set_facecolor(COLOR_BG); fig.patch.set_facecolor(COLOR_BG); ax.axis('off')

    # Header Card
    hdr = patches.FancyBboxPatch((1.0, 4.6), 10.0, 1.2, boxstyle="round,pad=0.15",
                                 facecolor=COLOR_NAVY, edgecolor=COLOR_BLUE, lw=2)
    ax.add_patch(hdr)
    ax.text(6.0, 5.35, "Q-SYNTH: FIRST-PRINCIPLES QUANTUM SYNTHESIZER & OPTIMIZER",
            ha='center', va='center', fontsize=15, fontweight='bold', color='white')
    ax.text(6.0, 4.9, "An Open-Source Framework for Exact Unitary Decompositions, Oracle Compilation & Circuit Reduction",
            ha='center', va='center', fontsize=10, color='#93C5FD')

    # Three Capability Pillars
    pillars = [
        ("CAPABILITY 1", "Unitary Matrix Synthesis",
         "• Exact & approximate beam search\n• Arbitrary user-defined gate sets\n• Phase-insensitive Hilbert-Schmidt metric\n• Quantized complex hash deduplication",
         COLOR_BLUE, COLOR_LIGHT_BLUE, 0.8),
        ("CAPABILITY 2", "Boolean & Oracle Compilation",
         "• Safe Python AST logic parser\n• Bit-flip (n+1 wires) & Phase (n wires)\n• Zero-ancilla phase kickback discovery\n• Reversible basis: Toffoli, Fredkin, CNOT",
         COLOR_PURPLE, COLOR_LIGHT_PURPLE, 4.4),
        ("CAPABILITY 3", "Constrained Circuit Optimizer",
         "• Commutation matrix analysis [A,B]=0\n• Disjoint wire peephole cancellation\n• Global synthesis-driven resynthesis\n• Sliding-window local block reductions",
         COLOR_TEAL, COLOR_LIGHT_TEAL, 8.0),
    ]

    for cap_tag, title, desc, col, bg_col, x in pillars:
        box = patches.FancyBboxPatch((x, 1.0), 3.2, 3.2, boxstyle="round,pad=0.15",
                                     facecolor="white", edgecolor=col, lw=2)
        ax.add_patch(box)
        badge = patches.FancyBboxPatch((x + 0.3, 3.65), 2.6, 0.45, boxstyle="round,pad=0.08",
                                       facecolor=col, edgecolor="none")
        ax.add_patch(badge)
        ax.text(x + 1.6, 3.87, cap_tag, ha='center', va='center',
                fontsize=9.5, fontweight='bold', color='white')
        ax.text(x + 1.6, 3.25, title, ha='center', va='center',
                fontsize=11, fontweight='bold', color=COLOR_NAVY)
        ax.text(x + 0.25, 2.0, desc, fontsize=8.5, color=COLOR_DARK, va='center')

    # Bottom Foundation Bar
    bar = patches.FancyBboxPatch((0.8, 0.2), 10.4, 0.55, boxstyle="round,pad=0.08",
                                 facecolor=COLOR_LIGHT_GRAY, edgecolor=COLOR_GRAY, lw=1)
    ax.add_patch(bar)
    ax.text(6.0, 0.47, "Foundation: Pure Python 3 + NumPy | Validated 100% Pass Rate across 34 Rigorous Test Suites",
            ha='center', va='center', fontsize=9.5, fontweight='bold', color=COLOR_DARK)

    ax.set_xlim(0, 12); ax.set_ylim(0, 6)
    return save_fig(fig, "slide01_title_overview.png")


# ==============================================================================
# CAPABILITY 1: UNITARY SYNTHESIS (STEPS 1-6 + SOTA)
# ==============================================================================
def make_slide2():  # Cap 1, Step 1: Input & Phase-Insensitive Formulation
    fig, ax = plt.subplots(figsize=(12, 6.2), dpi=250)
    ax.set_facecolor(COLOR_BG); fig.patch.set_facecolor(COLOR_BG); ax.axis('off')

    # Step Banner
    step_tag = patches.FancyBboxPatch((0.8, 5.0), 10.4, 0.65, boxstyle="round,pad=0.08",
                                     facecolor=COLOR_BLUE, edgecolor="none")
    ax.add_patch(step_tag)
    ax.text(1.2, 5.32, "CAPABILITY 1 | STEP 1: TARGET UNITARY INGESTION & PHASE-INSENSITIVE METRIC",
            fontsize=12, fontweight='bold', color='white', va='center')

    # Left: Target Ingestion Modes
    left_box = patches.FancyBboxPatch((0.8, 1.0), 4.8, 3.7, boxstyle="round,pad=0.15",
                                      facecolor="white", edgecolor=COLOR_BLUE, lw=1.8)
    ax.add_patch(left_box)
    ax.text(3.2, 4.3, "1. Target Input Pathways", ha='center', fontsize=12, fontweight='bold', color=COLOR_BLUE)

    inputs = [
        ("Built-in Presets", "--matrix swap, cnot, cz, ccx, h, s, t"),
        ("Inline JSON", "--matrix '[[\"sqrt2/2\",\"sqrt2/2\"],[\"sqrt2/2\",\"-sqrt2/2\"]]'"),
        ("Matrix File", "--matrix-file unitary.npy or text/CSV"),
        ("Unitarity Validation", r"Enforces $\|U^\dagger U - I\| < 10^{-8}$ and dim $= 2^n$"),
    ]
    for i, (title, desc) in enumerate(inputs):
        y = 3.6 - i * 0.75
        sub = patches.FancyBboxPatch((1.1, y - 0.25), 4.2, 0.6, boxstyle="round,pad=0.08",
                                     facecolor=COLOR_LIGHT_BLUE, edgecolor="none")
        ax.add_patch(sub)
        ax.text(1.3, y + 0.12, title, fontsize=9.5, fontweight='bold', color=COLOR_NAVY)
        ax.text(1.3, y - 0.12, desc, fontsize=8, color=COLOR_DARK)

    # Right: Phase-Insensitive Hilbert-Schmidt Metric
    right_box = patches.FancyBboxPatch((6.0, 1.0), 5.2, 3.7, boxstyle="round,pad=0.15",
                                       facecolor="white", edgecolor=COLOR_PURPLE, lw=1.8)
    ax.add_patch(right_box)
    ax.text(8.6, 4.3, "2. Phase-Insensitive Trace Metric", ha='center', fontsize=12, fontweight='bold', color=COLOR_PURPLE)

    math_notes = [
        ("Normalized Hilbert-Schmidt Similarity:", r"$s(U, V) = \frac{|\mathrm{Tr}(U^\dagger V)|}{2^n} \in [0, 1]$"),
        ("Physical Equivalence Condition:", r"$s(U, V) = 1 \Leftrightarrow U = e^{i\phi} V$ (identical observables)"),
        ("Global Phase Extraction:", r"$\phi = -\arg(\mathrm{Tr}(U^\dagger V))$"),
        ("Phase-Corrected Maximum Residual Error:", r"$\delta_{\max} = \max_{j,k} |U_{jk} - e^{i\phi} V_{jk}|$"),
    ]
    for i, (head, eq) in enumerate(math_notes):
        y = 3.6 - i * 0.75
        sub = patches.FancyBboxPatch((6.3, y - 0.25), 4.6, 0.6, boxstyle="round,pad=0.08",
                                     facecolor=COLOR_LIGHT_PURPLE, edgecolor="none")
        ax.add_patch(sub)
        ax.text(6.5, y + 0.12, head, fontsize=9, fontweight='bold', color=COLOR_PURPLE)
        ax.text(6.5, y - 0.14, eq, fontsize=9.5, color=COLOR_NAVY)

    # Arrow from left to right
    ax.annotate("", xy=(5.8, 2.8), xytext=(5.3, 2.8),
                arrowprops=dict(arrowstyle="-|>", color=COLOR_NAVY, lw=2.5))

    ax.set_xlim(0, 12); ax.set_ylim(0, 6)
    return save_fig(fig, "slide02_cap1_step1_formulation.png")


def make_slide3():  # Cap 1, Step 2: Ordered Permutation Move Enumeration
    fig, ax = plt.subplots(figsize=(12, 6.2), dpi=250)
    ax.set_facecolor(COLOR_BG); fig.patch.set_facecolor(COLOR_BG); ax.axis('off')

    # Step Banner
    step_tag = patches.FancyBboxPatch((0.8, 5.0), 10.4, 0.65, boxstyle="round,pad=0.08",
                                     facecolor=COLOR_BLUE, edgecolor="none")
    ax.add_patch(step_tag)
    ax.text(1.2, 5.32, "CAPABILITY 1 | STEP 2: ORDERED PERMUTATION MOVE ENUMERATION",
            fontsize=12, fontweight='bold', color='white', va='center')

    # Formula Box
    formula_box = patches.FancyBboxPatch((0.8, 3.8), 10.4, 0.95, boxstyle="round,pad=0.1",
                                         facecolor="white", edgecolor=COLOR_NAVY, lw=1.5)
    ax.add_patch(formula_box)
    ax.text(1.2, 4.4, r"Combinatorial Move Placements: $P(n, k_g) = \frac{n!}{(n - k_g)!}$ directed placements per gate $g$",
            fontsize=11.5, fontweight='bold', color=COLOR_NAVY)
    ax.text(1.2, 4.05, "Every gate wire maps to a distinct physical wire: e.g. for CNOT, [0,1] flips q1 on q0=1; [1,0] flips q0 on q1=1.",
            fontsize=9, color=COLOR_GRAY)

    # Concrete Example Cards for n = 3 Qubits
    examples = [
        ("1-Qubit Gate (e.g. H, T)", r"$P(3, 1) = \frac{3!}{2!} = 3$ Placements",
         ["Placement [0]: Acts on q0", "Placement [1]: Acts on q1", "Placement [2]: Acts on q2"],
         COLOR_TEAL, 0.8),
        ("2-Qubit Gate (e.g. CNOT, CZ)", r"$P(3, 2) = \frac{3!}{1!} = 6$ Placements",
         ["Placements: [0,1], [1,0]", "Placements: [0,2], [2,0]", "Placements: [1,2], [2,1]"],
         COLOR_BLUE, 4.4),
        ("3-Qubit Gate (e.g. Toffoli)", r"$P(3, 3) = \frac{3!}{0!} = 6$ Placements",
         ["Placements: [0,1,2], [1,0,2]", "Placements: [0,2,1], [2,0,1]", "Placements: [1,2,0], [2,1,0]"],
         COLOR_PURPLE, 8.0),
    ]

    for title, math_hd, items, col, x in examples:
        card = patches.FancyBboxPatch((x, 1.0), 3.2, 2.5, boxstyle="round,pad=0.12",
                                      facecolor="white", edgecolor=col, lw=2)
        ax.add_patch(card)
        ax.text(x + 1.6, 3.2, title, ha='center', fontsize=11, fontweight='bold', color=col)
        ax.text(x + 1.6, 2.75, math_hd, ha='center', fontsize=9.5, color=COLOR_NAVY)
        for j, it in enumerate(items):
            ax.text(x + 0.3, 2.2 - j * 0.45, it, fontsize=8.5, color=COLOR_DARK)

    ax.set_xlim(0, 12); ax.set_ylim(0, 6)
    return save_fig(fig, "slide03_cap1_step2_moves.png")


def make_slide4():  # Cap 1, Step 3: Kronecker Matrix Embedding
    fig, ax = plt.subplots(figsize=(12, 6.2), dpi=250)
    ax.set_facecolor(COLOR_BG); fig.patch.set_facecolor(COLOR_BG); ax.axis('off')

    # Step Banner
    step_tag = patches.FancyBboxPatch((0.8, 5.0), 10.4, 0.65, boxstyle="round,pad=0.08",
                                     facecolor=COLOR_BLUE, edgecolor="none")
    ax.add_patch(step_tag)
    ax.text(1.2, 5.32, "CAPABILITY 1 | STEP 3: KRONECKER SUB-WORD EMBEDDING INTO 2ⁿ SPACE",
            fontsize=12, fontweight='bold', color='white', va='center')

    # Left: Wire Diagram Embedding
    wire_box = patches.FancyBboxPatch((0.8, 1.0), 5.0, 3.7, boxstyle="round,pad=0.15",
                                      facecolor="white", edgecolor=COLOR_BLUE, lw=1.8)
    ax.add_patch(wire_box)
    ax.text(3.3, 4.35, "Placement Mapping: CNOT on [q0, q2]", ha='center', fontsize=11.5, fontweight='bold', color=COLOR_BLUE)

    wires = [
        ("q0 (wire 0)", "Control Wire", 3.7, "ctrl"),
        ("q1 (wire 1)", "Untouched: Acts as Identity I₂", 2.7, "id"),
        ("q2 (wire 2)", "Target Wire", 1.7, "tgt"),
    ]
    for lbl, desc, y, role in wires:
        ax.plot([1.2, 5.4], [y, y], color=COLOR_GRAY, lw=2)
        ax.text(1.1, y, lbl, ha='right', va='center', fontsize=9.5, fontweight='bold', color=COLOR_NAVY)
        if role == "ctrl":
            c = plt.Circle((3.3, y), 0.15, color=COLOR_BLUE, zorder=5)
            ax.add_patch(c)
            ax.text(3.6, y + 0.18, desc, fontsize=8, color=COLOR_BLUE, fontweight='bold')
        elif role == "tgt":
            c = plt.Circle((3.3, y), 0.18, facecolor="white", edgecolor=COLOR_BLUE, lw=2, zorder=5)
            ax.add_patch(c)
            ax.plot([3.18, 3.42], [y, y], color=COLOR_BLUE, lw=2, zorder=6)
            ax.plot([3.3, 3.3], [y-0.12, y+0.12], color=COLOR_BLUE, lw=2, zorder=6)
            ax.text(3.6, y - 0.18, desc, fontsize=8, color=COLOR_BLUE, fontweight='bold')
        elif role == "id":
            rect = patches.Rectangle((3.0, y - 0.22), 0.6, 0.44, facecolor=COLOR_LIGHT_TEAL,
                                     edgecolor=COLOR_TEAL, lw=1.5, zorder=5)
            ax.add_patch(rect)
            ax.text(3.3, y, "I₂", ha='center', va='center', fontsize=9, fontweight='bold', color=COLOR_TEAL)
            ax.text(3.7, y, desc, fontsize=8, color=COLOR_TEAL)

    ax.plot([3.3, 3.3], [1.7, 3.7], color=COLOR_BLUE, lw=2, zorder=4)

    # Right: Mathematical Projection Rule
    math_box = patches.FancyBboxPatch((6.2, 1.0), 5.0, 3.7, boxstyle="round,pad=0.15",
                                      facecolor="white", edgecolor=COLOR_PURPLE, lw=1.8)
    ax.add_patch(math_box)
    ax.text(8.7, 4.35, "Mathematical Projection Rule", ha='center', fontsize=11.5, fontweight='bold', color=COLOR_PURPLE)

    rules = [
        r"$\mathrm{Embed}(G, n, p)_{r, c}$ Definition:",
        r"  $\bullet$ $G[g_{\mathrm{row}}, g_{\mathrm{col}}]$ if untouched bits agree",
        r"  $\bullet$ $0$ otherwise (untouched bits differ)",
        r"Sub-word extraction: $g_{\mathrm{row}} = \sum_{w=0}^{k-1} ((r \gg p_w) \ \mathrm{AND} \ 1) \cdot 2^w$",
        r"Identity on free wires: $(r \oplus c) \ \mathrm{AND} \ \mathrm{free\_mask} = 0$",
        "Precomputed once per gate set & register size",
        "Result: exact 8 x 8 sparse matrix multiplication",
    ]
    for i, r in enumerate(rules):
        ax.text(6.5, 3.7 - i * 0.48, r, fontsize=8.8, color=COLOR_DARK)

    ax.set_xlim(0, 12); ax.set_ylim(0, 6)
    return save_fig(fig, "slide04_cap1_step3_embedding.png")


def make_slide5():  # Cap 1, Step 4: Quantized Complex Hash Grid Deduplication
    fig, ax = plt.subplots(figsize=(12, 6.2), dpi=250)
    ax.set_facecolor(COLOR_BG); fig.patch.set_facecolor(COLOR_BG); ax.axis('off')

    # Step Banner
    step_tag = patches.FancyBboxPatch((0.8, 5.0), 10.4, 0.65, boxstyle="round,pad=0.08",
                                     facecolor=COLOR_BLUE, edgecolor="none")
    ax.add_patch(step_tag)
    ax.text(1.2, 5.32, "CAPABILITY 1 | STEP 4: QUANTIZED COMPLEX HASH GRID DEDUPLICATION",
            fontsize=12, fontweight='bold', color='white', va='center')

    # Left: The State Space Explosion Problem
    left = patches.FancyBboxPatch((0.8, 1.0), 4.8, 3.7, boxstyle="round,pad=0.15",
                                 facecolor="white", edgecolor=COLOR_CORAL, lw=1.8)
    ax.add_patch(left)
    ax.text(3.2, 4.35, "The Combinatorial Explosion Challenge", ha='center',
            fontsize=11.5, fontweight='bold', color=COLOR_CORAL)

    notes_left = [
        ("Branching Factor:", r"$N_{\mathrm{moves}}^d$ candidates explode exponentially"),
        ("Commutative Redundancy:", "X[0] X[1] produces identical matrix to X[1] X[0]"),
        ("Self-Inverse Cycles:", "H[0] followed by H[0] loops back to Identity"),
        ("Floating-Point Hazard:", "Standard float hashing fails due to rounding drift"),
    ]
    for i, (head, body) in enumerate(notes_left):
        y = 3.6 - i * 0.75
        sub = patches.FancyBboxPatch((1.1, y - 0.25), 4.2, 0.6, boxstyle="round,pad=0.08",
                                     facecolor=COLOR_LIGHT_CORAL, edgecolor="none")
        ax.add_patch(sub)
        ax.text(1.3, y + 0.12, head, fontsize=9, fontweight='bold', color=COLOR_CORAL)
        ax.text(1.3, y - 0.14, body, fontsize=8, color=COLOR_DARK)

    # Right: Q-Synth Fixed-Grid Hashing Solution
    right = patches.FancyBboxPatch((6.0, 1.0), 5.2, 3.7, boxstyle="round,pad=0.15",
                                  facecolor="white", edgecolor=COLOR_TEAL, lw=1.8)
    ax.add_patch(right)
    ax.text(8.6, 4.35, "Q-Synth 10⁹ Quantized Hash Grid", ha='center',
            fontsize=11.5, fontweight='bold', color=COLOR_TEAL)

    notes_right = [
        ("Quantization Formula:", r"$\mathrm{key} = \mathrm{bytes}(\lfloor \mathrm{Re}(V) \cdot 10^9 \rceil, \lfloor \mathrm{Im}(V) \cdot 10^9 \rceil)$"),
        ("Exact Integer Hashing:", "Converts complex matrix to immutable 64-bit int buffer"),
        ("Duplicate Elimination:", "Maintains visited set; skips already discovered states"),
        ("Impact on Scaling:", "Keeps unique states bounded; prevents redundant beam slots"),
    ]
    for i, (head, body) in enumerate(notes_right):
        y = 3.6 - i * 0.75
        sub = patches.FancyBboxPatch((6.3, y - 0.25), 4.6, 0.6, boxstyle="round,pad=0.08",
                                     facecolor=COLOR_LIGHT_TEAL, edgecolor="none")
        ax.add_patch(sub)
        ax.text(6.5, y + 0.12, head, fontsize=9, fontweight='bold', color=COLOR_TEAL)
        ax.text(6.5, y - 0.14, body, fontsize=8.5, color=COLOR_NAVY)

    # Middle Arrow
    ax.annotate("", xy=(5.8, 2.8), xytext=(5.3, 2.8),
                arrowprops=dict(arrowstyle="-|>", color=COLOR_NAVY, lw=2.5))

    ax.set_xlim(0, 12); ax.set_ylim(0, 6)
    return save_fig(fig, "slide05_cap1_step4_hash_grid.png")


def make_slide6():  # Cap 1, Step 5: Guided Beam Search Exploration
    fig, ax = plt.subplots(figsize=(12, 6.2), dpi=250)
    ax.set_facecolor(COLOR_BG); fig.patch.set_facecolor(COLOR_BG); ax.axis('off')

    # Step Banner
    step_tag = patches.FancyBboxPatch((0.8, 5.0), 10.4, 0.65, boxstyle="round,pad=0.08",
                                     facecolor=COLOR_BLUE, edgecolor="none")
    ax.add_patch(step_tag)
    ax.text(1.2, 5.32, "CAPABILITY 1 | STEP 5: GUIDED BEAM-SEARCH EXPLORATION & PRUNING",
            fontsize=12, fontweight='bold', color='white', va='center')

    # Visual Tree Diagram
    # Level 0
    c0 = patches.Circle((1.5, 2.8), 0.5, facecolor=COLOR_NAVY, edgecolor=COLOR_BLUE, lw=2)
    ax.add_patch(c0)
    ax.text(1.5, 2.8, "Depth 0\nV = I", ha='center', va='center', fontsize=9.5, fontweight='bold', color='white')

    # Level 1 Candidates
    l1_y = [4.2, 3.3, 2.3, 1.4]
    for i, y in enumerate(l1_y):
        col = COLOR_BLUE if i < 3 else COLOR_GRAY
        c = patches.Circle((4.5, y), 0.38, facecolor="white", edgecolor=col, lw=1.8)
        ax.add_patch(c)
        ax.text(4.5, y, f"V_{i+1}", ha='center', va='center', fontsize=8.5, fontweight='bold', color=col)
        ax.annotate("", xy=(4.1, y), xytext=(2.0, 2.8),
                    arrowprops=dict(arrowstyle="-|>", color=col, lw=1.4))

    # Scoring & Pruning Filter Box
    prune = patches.FancyBboxPatch((5.8, 1.0), 2.2, 3.6, boxstyle="round,pad=0.1",
                                   facecolor=COLOR_LIGHT_BLUE, edgecolor=COLOR_BLUE, lw=1.8)
    ax.add_patch(prune)
    ax.text(6.9, 4.2, "Beam Filter", ha='center', fontsize=11, fontweight='bold', color=COLOR_BLUE)
    ax.text(6.9, 3.6, "1. Evaluate Fidelity:\ns(U, V) = |Tr(U†V)|/2ⁿ", ha='center', fontsize=8, color=COLOR_DARK)
    ax.text(6.9, 2.7, "2. Early Match Check:\ns ≥ 1 - ε? -> EXIT", ha='center', fontsize=8, fontweight='bold', color=COLOR_CORAL)
    ax.text(6.9, 1.8, "3. Sort Descending & Keep Top-K (Beam Width)", ha='center', fontsize=8, color=COLOR_BLUE)

    # Level 2 Candidates
    l2_y = [3.8, 2.8, 1.8]
    for i, y in enumerate(l2_y):
        c = patches.Circle((9.0, y), 0.38, facecolor="white", edgecolor=COLOR_TEAL, lw=1.8)
        ax.add_patch(c)
        ax.text(9.0, y, f"K_{i+1}", ha='center', va='center', fontsize=8.5, fontweight='bold', color=COLOR_TEAL)
        ax.annotate("", xy=(8.6, y), xytext=(7.8, 2.8),
                    arrowprops=dict(arrowstyle="-|>", color=COLOR_TEAL, lw=1.4))

    # Solution Found Box
    sol = patches.FancyBboxPatch((10.0, 2.2), 1.6, 1.2, boxstyle="round,pad=0.1",
                                 facecolor=COLOR_TEAL, edgecolor=COLOR_NAVY, lw=2)
    ax.add_patch(sol)
    ax.text(10.8, 3.0, "MATCH!", ha='center', fontsize=11, fontweight='bold', color='white')
    ax.text(10.8, 2.5, "s ≥ 1 - 10⁻⁹\nExact Circuit", ha='center', fontsize=8, color='#ECFDF5')
    ax.annotate("", xy=(10.0, 2.8), xytext=(9.4, 2.8),
                arrowprops=dict(arrowstyle="-|>", color=COLOR_TEAL, lw=2.5))

    ax.set_xlim(0.5, 12); ax.set_ylim(0.5, 5.8)
    return save_fig(fig, "slide06_cap1_step5_beam_search.png")


def make_slide7():  # Cap 1, Step 6: Post-Search Verification
    fig, ax = plt.subplots(figsize=(12, 6.2), dpi=250)
    ax.set_facecolor(COLOR_BG); fig.patch.set_facecolor(COLOR_BG); ax.axis('off')

    # Step Banner
    step_tag = patches.FancyBboxPatch((0.8, 5.0), 10.4, 0.65, boxstyle="round,pad=0.08",
                                     facecolor=COLOR_BLUE, edgecolor="none")
    ax.add_patch(step_tag)
    ax.text(1.2, 5.32, "CAPABILITY 1 | STEP 6: POST-SEARCH VERIFICATION & RESIDUAL ERROR ANALYSIS",
            fontsize=12, fontweight='bold', color='white', va='center')

    # Flowchart: Reconstructed Circuit -> Global Phase -> Max Error
    steps = [
        ("1. Multiplied Circuit V", r"$V = G_L G_{L-1} \cdots G_1$",
         "Multiplies full embedded matrices in forward execution order", COLOR_BLUE, 0.8),
        ("2. Hilbert-Schmidt Trace", r"$\tau = \mathrm{Tr}(U^\dagger V)$",
         "Measures complex overlap scalar; similarity s = |τ| / 2ⁿ", COLOR_PURPLE, 4.4),
        ("3. Global Phase & Residual Error", r"$\phi = -\arg(\tau), \quad \delta = \max |U - e^{i\phi} V|$",
         "Guarantees physical equivalence with zero observable discrepancy", COLOR_TEAL, 8.0),
    ]
    for title, eq, desc, col, x in steps:
        card = patches.FancyBboxPatch((x, 2.0), 3.2, 2.6, boxstyle="round,pad=0.15",
                                      facecolor="white", edgecolor=col, lw=2)
        ax.add_patch(card)
        ax.text(x + 1.6, 4.2, title, ha='center', fontsize=10.5, fontweight='bold', color=col)
        ax.text(x + 1.6, 3.4, eq, ha='center', fontsize=10, color=COLOR_NAVY)
        ax.text(x + 1.6, 2.5, desc, ha='center', fontsize=8, color=COLOR_DARK, multialignment='center')

        if x < 7.0:
            ax.annotate("", xy=(x + 3.45, 3.3), xytext=(x + 3.15, 3.3),
                        arrowprops=dict(arrowstyle="-|>", color=COLOR_NAVY, lw=2.2))

    # Real Empirical Stats Banner
    res_box = patches.FancyBboxPatch((0.8, 0.6), 10.4, 1.0, boxstyle="round,pad=0.1",
                                     facecolor=COLOR_LIGHT_TEAL, edgecolor=COLOR_TEAL, lw=1.5)
    ax.add_patch(res_box)
    ax.text(1.1, 1.25, "Actual Q-Synth Verification Output (Hadamard from discrete RX/RY/RZ rotations):",
            fontsize=9.5, fontweight='bold', color=COLOR_TEAL)
    ax.text(1.1, 0.85, "SUCCESS at depth 2 (35 expansions, 0.00s): V = RY(-pi/2) @ RX(-pi) | similarity: 1.0000000000 | phase: -1.570796 rad | max error: 1.41e-16",
            fontsize=8.5, color=COLOR_NAVY)

    ax.set_xlim(0, 12); ax.set_ylim(0.2, 5.8)
    return save_fig(fig, "slide07_cap1_step6_verification.png")


def make_slide8():  # Cap 1, SOTA Comparison
    fig, ax = plt.subplots(figsize=(12, 6.2), dpi=250)
    ax.set_facecolor(COLOR_BG); fig.patch.set_facecolor(COLOR_BG); ax.axis('off')

    # SOTA Banner
    banner = patches.FancyBboxPatch((0.8, 5.0), 10.4, 0.65, boxstyle="round,pad=0.08",
                                   facecolor=COLOR_NAVY, edgecolor=COLOR_BLUE, lw=1.8)
    ax.add_patch(banner)
    ax.text(1.2, 5.32, "CAPABILITY 1 | RESEARCH FRONTIER: WHERE Q-SYNTH GOES BEYOND PRIOR WORK",
            fontsize=12, fontweight='bold', color='white', va='center')

    # Left: Prior Art Limitations
    left = patches.FancyBboxPatch((0.8, 0.8), 4.8, 3.9, boxstyle="round,pad=0.15",
                                 facecolor="white", edgecolor=COLOR_CORAL, lw=1.8)
    ax.add_patch(left)
    ax.text(3.2, 4.4, "Conventional Prior Work (Qiskit, KAK, Solovay-Kitaev)", ha='center',
            fontsize=11, fontweight='bold', color=COLOR_CORAL)

    prior_points = [
        ("Locked to Fixed Hardware Bases", "Compilers are hard-coded to standard sets (e.g. {CX, U3}); unable to explore arbitrary experimental gate sets."),
        ("Continuous Analytical Overhead", "KAK & QSD require continuous Euler angles, necessitating heavy subsequent discretization passes."),
        ("Sub-Optimal Depth for Subsets", "Restricting to a subset (e.g. CNOT only) breaks analytical transpilers or blows up gate depth."),
        ("Black-Box Opaque Search", "Users cannot inspect intermediate state expansions or enforce custom gate costs."),
    ]
    for i, (head, body) in enumerate(prior_points):
        y = 3.7 - i * 0.75
        ax.text(1.1, y + 0.12, "✕ " + head, fontsize=9.5, fontweight='bold', color=COLOR_CORAL)
        ax.text(1.3, y - 0.15, body, fontsize=8, color=COLOR_DARK)

    # Right: Q-Synth Research Edge
    right = patches.FancyBboxPatch((6.0, 0.8), 5.2, 3.9, boxstyle="round,pad=0.15",
                                  facecolor="white", edgecolor=COLOR_TEAL, lw=1.8)
    ax.add_patch(right)
    ax.text(8.6, 4.4, "Q-Synth Breakthrough & Advantages", ha='center',
            fontsize=11, fontweight='bold', color=COLOR_TEAL)

    qsynth_points = [
        ("Arbitrary User-Configured Gate Libraries", "Loads any gate definitions via simple JSON. Seamlessly synthesizes Clifford+T, discrete rotations, or reversible sets."),
        ("Provably Minimal Depth for Small Registers", "Exact beam search discovers true minimal gate counts (e.g., SWAP in 3 CNOTs in 9 expansions in <0.001s)."),
        ("10⁹ Quantized Grid Deduplication", "Eliminates state-space explosion without floating-point hash instability."),
        ("Phase-Insensitive Observable Equivalence", "Guarantees exact physical fidelity while decoupling unobservable global phase."),
    ]
    for i, (head, body) in enumerate(qsynth_points):
        y = 3.7 - i * 0.75
        ax.text(6.3, y + 0.12, "✓ " + head, fontsize=9.5, fontweight='bold', color=COLOR_TEAL)
        ax.text(6.5, y - 0.15, body, fontsize=8, color=COLOR_DARK)

    ax.set_xlim(0, 12); ax.set_ylim(0.4, 5.8)
    return save_fig(fig, "slide08_cap1_sota_comparison.png")


# ==============================================================================
# CAPABILITY 2: BOOLEAN & TRUTH TABLE SYNTHESIS (STEPS 1-5 + SOTA)
# ==============================================================================
def make_slide9():  # Cap 2, Step 1: AST Logic Parsing
    fig, ax = plt.subplots(figsize=(12, 6.2), dpi=250)
    ax.set_facecolor(COLOR_BG); fig.patch.set_facecolor(COLOR_BG); ax.axis('off')

    # Step Banner
    step_tag = patches.FancyBboxPatch((0.8, 5.0), 10.4, 0.65, boxstyle="round,pad=0.08",
                                     facecolor=COLOR_PURPLE, edgecolor="none")
    ax.add_patch(step_tag)
    ax.text(1.2, 5.32, "CAPABILITY 2 | STEP 1: SAFE AST LOGIC PARSING & VARIABLE INTROSPECTION",
            fontsize=12, fontweight='bold', color='white', va='center')

    # Left: AST Decomposition Diagram
    left = patches.FancyBboxPatch((0.8, 1.0), 5.0, 3.7, boxstyle="round,pad=0.15",
                                 facecolor="white", edgecolor=COLOR_PURPLE, lw=1.8)
    ax.add_patch(left)
    ax.text(3.3, 4.35, "AST Tree Breakdown: '(x0 and x1) ^ x2'", ha='center',
            fontsize=11, fontweight='bold', color=COLOR_PURPLE)

    # Mini AST tree
    ax.text(3.3, 3.7, "BinOp: BitXor (^)", ha='center', fontsize=9.5, fontweight='bold',
            bbox=dict(boxstyle="round,pad=0.2", facecolor=COLOR_LIGHT_PURPLE, edgecolor=COLOR_PURPLE))
    ax.plot([3.3, 2.2], [3.45, 2.7], color=COLOR_PURPLE, lw=1.5)
    ax.plot([3.3, 4.4], [3.45, 2.7], color=COLOR_PURPLE, lw=1.5)

    ax.text(2.2, 2.5, "BoolOp: And", ha='center', fontsize=8.5, fontweight='bold',
            bbox=dict(boxstyle="round,pad=0.2", facecolor=COLOR_LIGHT_BLUE, edgecolor=COLOR_BLUE))
    ax.text(4.4, 2.5, "Var: x2", ha='center', fontsize=8.5, fontweight='bold',
            bbox=dict(boxstyle="round,pad=0.2", facecolor=COLOR_LIGHT_TEAL, edgecolor=COLOR_TEAL))

    ax.plot([2.2, 1.6], [2.25, 1.7], color=COLOR_BLUE, lw=1.5)
    ax.plot([2.2, 2.8], [2.25, 1.7], color=COLOR_BLUE, lw=1.5)
    ax.text(1.6, 1.5, "Var: x0", ha='center', fontsize=8,
            bbox=dict(boxstyle="round,pad=0.15", facecolor=COLOR_LIGHT_BLUE, edgecolor=COLOR_BLUE))
    ax.text(2.8, 1.5, "Var: x1", ha='center', fontsize=8,
            bbox=dict(boxstyle="round,pad=0.15", facecolor=COLOR_LIGHT_BLUE, edgecolor=COLOR_BLUE))

    # Right: Security & Automated Introspection
    right = patches.FancyBboxPatch((6.2, 1.0), 5.0, 3.7, boxstyle="round,pad=0.15",
                                  facecolor="white", edgecolor=COLOR_NAVY, lw=1.8)
    ax.add_patch(right)
    ax.text(8.7, 4.35, "Security Constraints & Variable Ordering", ha='center',
            fontsize=11, fontweight='bold', color=COLOR_NAVY)

    features = [
        ("Strict Syntax Sanitization:", "Only BitOp, BoolOp, UnaryOp, and Constants allowed; arbitrary functions & imports rejected."),
        ("Supported Operators:", "Python syntax: and, or, not, &, |, ^, ~, ==, !="),
        ("Automated Wire Ordering:", "Variables (x0, x1, x2...) sorted by index; x0 maps to least significant qubit (LSB)."),
        ("Safe Isolated Evaluation:", "Compiled code runs with empty __builtins__ namespace."),
    ]
    for i, (hd, desc) in enumerate(features):
        y = 3.6 - i * 0.75
        sub = patches.FancyBboxPatch((6.5, y - 0.25), 4.4, 0.6, boxstyle="round,pad=0.08",
                                     facecolor=COLOR_LIGHT_GRAY, edgecolor="none")
        ax.add_patch(sub)
        ax.text(6.7, y + 0.12, hd, fontsize=9, fontweight='bold', color=COLOR_NAVY)
        ax.text(6.7, y - 0.14, desc, fontsize=8, color=COLOR_DARK)

    ax.set_xlim(0, 12); ax.set_ylim(0.4, 5.8)
    return save_fig(fig, "slide09_cap2_step1_ast.png")


def make_slide10():  # Cap 2, Step 2: Truth Table Formulation
    fig, ax = plt.subplots(figsize=(12, 6.2), dpi=250)
    ax.set_facecolor(COLOR_BG); fig.patch.set_facecolor(COLOR_BG); ax.axis('off')

    # Step Banner
    step_tag = patches.FancyBboxPatch((0.8, 5.0), 10.4, 0.65, boxstyle="round,pad=0.08",
                                     facecolor=COLOR_PURPLE, edgecolor="none")
    ax.add_patch(step_tag)
    ax.text(1.2, 5.32, "CAPABILITY 2 | STEP 2: TRUTH TABLE EVALUATION & LITTLE-ENDIAN CONVENTION",
            fontsize=12, fontweight='bold', color='white', va='center')

    # Left: Little-Endian Assignment
    left = patches.FancyBboxPatch((0.8, 1.0), 5.0, 3.7, boxstyle="round,pad=0.15",
                                 facecolor="white", edgecolor=COLOR_PURPLE, lw=1.8)
    ax.add_patch(left)
    ax.text(3.3, 4.35, "Little-Endian State Mapping", ha='center', fontsize=11.5, fontweight='bold', color=COLOR_PURPLE)

    points = [
        ("LSB-First Standard:", "Qubit 0 is the Least Significant Bit (matches Qiskit / IBM)."),
        ("Row Index Mapping:", r"Row $k = \sum_{i=0}^{n-1} b_i 2^i \Rightarrow x_i = b_i$"),
        ("Vector Size:", r"$2^n$ outputs for $n$ input variables"),
        ("Permutation Validations:", "Checks that bijections contain 0..2ⁿ-1 without duplicate outputs"),
    ]
    for i, (hd, body) in enumerate(points):
        y = 3.6 - i * 0.75
        sub = patches.FancyBboxPatch((1.1, y - 0.25), 4.4, 0.6, boxstyle="round,pad=0.08",
                                     facecolor=COLOR_LIGHT_PURPLE, edgecolor="none")
        ax.add_patch(sub)
        ax.text(1.3, y + 0.12, hd, fontsize=9, fontweight='bold', color=COLOR_PURPLE)
        ax.text(1.3, y - 0.14, body, fontsize=8, color=COLOR_DARK)

    # Right: Rendered Truth Table Example (XOR: x0 ^ x1)
    right = patches.FancyBboxPatch((6.2, 1.0), 5.0, 3.7, boxstyle="round,pad=0.15",
                                  facecolor="white", edgecolor=COLOR_NAVY, lw=1.8)
    ax.add_patch(right)
    ax.text(8.7, 4.35, "Terminal Truth Table Output (e.g. x0 ^ x1)", ha='center',
            fontsize=11.5, fontweight='bold', color=COLOR_NAVY)

    tt_code = (
        "  x1  x0  |  f(x0, x1)\n"
        " ----------------------\n"
        "   0   0  |     0\n"
        "   0   1  |     1\n"
        "   1   0  |     1\n"
        "   1   1  |     0\n\n"
        "• Little-Endian Row Index k:\n"
        "  k=0 (00₂) -> f=0 | k=1 (01₂) -> f=1\n"
        "  k=2 (10₂) -> f=1 | k=3 (11₂) -> f=0\n"
        "• Equivalent bitstring spec: \"0110\""
    )
    ax.text(6.6, 2.5, tt_code, fontsize=9, family='monospace', color=COLOR_NAVY, va='center')

    ax.set_xlim(0, 12); ax.set_ylim(0.4, 5.8)
    return save_fig(fig, "slide10_cap2_step2_truth_table.png")


def make_slide11():  # Cap 2, Step 3: Three Oracle Paradigms
    fig, ax = plt.subplots(figsize=(12, 6.2), dpi=250)
    ax.set_facecolor(COLOR_BG); fig.patch.set_facecolor(COLOR_BG); ax.axis('off')

    # Step Banner
    step_tag = patches.FancyBboxPatch((0.8, 5.0), 10.4, 0.65, boxstyle="round,pad=0.08",
                                     facecolor=COLOR_PURPLE, edgecolor="none")
    ax.add_patch(step_tag)
    ax.text(1.2, 5.32, "CAPABILITY 2 | STEP 3: QUANTUM ORACLE EMBEDDING PARADIGMS",
            fontsize=12, fontweight='bold', color='white', va='center')

    oracles = [
        ("1. Bit-Flip Oracle", "--oracle-mode bitflip",
         r"$|x, y\rangle \mapsto |x, y \oplus f(x)\rangle$",
         "• Operates on n + 1 qubits\n• Wires 0..n-1: input |x⟩\n• Wire n: ancilla |y⟩\n• Constructs 2ⁿ⁺¹ permutation matrix",
         COLOR_BLUE, 0.8),
        ("2. Phase Oracle", "--oracle-mode phase",
         r"$|x\rangle \mapsto (-1)^{f(x)} |x\rangle$",
         "• Operates strictly on n qubits\n• Zero ancilla qubit overhead!\n• Diagonal matrix: diag((-1)^f(x))\n• Ideal for Grover / phase kickback",
         COLOR_PURPLE, 4.4),
        ("3. Permutation Oracle", "--oracle-mode permutation",
         r"$|x\rangle \mapsto |f(x)\rangle$",
         "• Operates on n qubits\n• Requires bijection truth table\n• Maps basis states directly\n• Perfect for reversible arithmetic",
         COLOR_TEAL, 8.0),
    ]

    for title, flag, math_eq, desc, col, x in oracles:
        card = patches.FancyBboxPatch((x, 1.0), 3.2, 3.7, boxstyle="round,pad=0.12",
                                      facecolor="white", edgecolor=col, lw=2)
        ax.add_patch(card)
        ax.text(x + 1.6, 4.3, title, ha='center', fontsize=11, fontweight='bold', color=col)
        ax.text(x + 1.6, 3.9, flag, ha='center', fontsize=8, color=COLOR_GRAY)
        sub = patches.FancyBboxPatch((x + 0.2, 3.2), 2.8, 0.5, boxstyle="round,pad=0.06",
                                     facecolor=COLOR_LIGHT_GRAY, edgecolor="none")
        ax.add_patch(sub)
        ax.text(x + 1.6, 3.45, math_eq, ha='center', fontsize=9.5, color=COLOR_NAVY)
        ax.text(x + 0.3, 2.0, desc, fontsize=8.5, color=COLOR_DARK)

    ax.set_xlim(0, 12); ax.set_ylim(0.4, 5.8)
    return save_fig(fig, "slide11_cap2_step3_oracle_modes.png")


def make_slide12():  # Cap 2, Step 4: Reversible Logic Basis
    fig, ax = plt.subplots(figsize=(12, 6.2), dpi=250)
    ax.set_facecolor(COLOR_BG); fig.patch.set_facecolor(COLOR_BG); ax.axis('off')

    # Step Banner
    step_tag = patches.FancyBboxPatch((0.8, 5.0), 10.4, 0.65, boxstyle="round,pad=0.08",
                                     facecolor=COLOR_PURPLE, edgecolor="none")
    ax.add_patch(step_tag)
    ax.text(1.2, 5.32, "CAPABILITY 2 | STEP 4: REVERSIBLE LOGIC BASIS INTEGRATION (gates/reversible.json)",
            fontsize=12, fontweight='bold', color='white', va='center')

    gates = [
        ("X (NOT)", "1 Qubit", "|x⟩ ↦ |x ⊕ 1⟩", "Single bit inversion", COLOR_BLUE, 0.8),
        ("CNOT (Feynman)", "2 Qubits", "|x, y⟩ ↦ |x, y ⊕ x⟩", "Controlled bit inversion", COLOR_TEAL, 3.0),
        ("SWAP", "2 Qubits", "|x, y⟩ ↦ |y, x⟩", "Wire state exchange", COLOR_GRAY, 5.2),
        ("CCX (Toffoli)", "3 Qubits", "|x, y, z⟩ ↦ |x, y, z ⊕ (x∧y)⟩", "Universal reversible logic gate", COLOR_PURPLE, 7.4),
        ("CSWAP (Fredkin)", "3 Qubits", "Controlled swap of y and z", "Conservative logic gate", COLOR_CORAL, 9.6),
    ]

    for name, qubits, math_eq, desc, col, x in gates:
        card = patches.FancyBboxPatch((x, 1.2), 2.0, 3.5, boxstyle="round,pad=0.1",
                                      facecolor="white", edgecolor=col, lw=2)
        ax.add_patch(card)
        ax.text(x + 1.0, 4.3, name, ha='center', fontsize=10.5, fontweight='bold', color=col)
        ax.text(x + 1.0, 3.9, qubits, ha='center', fontsize=8.5, color=COLOR_GRAY)
        ax.text(x + 1.0, 3.2, math_eq, ha='center', fontsize=8.5, color=COLOR_NAVY)
        ax.text(x + 1.0, 2.0, desc, ha='center', fontsize=8, color=COLOR_DARK, multialignment='center')

    # Bottom Callout
    callout = patches.FancyBboxPatch((0.8, 0.3), 10.4, 0.65, boxstyle="round,pad=0.08",
                                     facecolor=COLOR_LIGHT_PURPLE, edgecolor=COLOR_PURPLE, lw=1)
    ax.add_patch(callout)
    ax.text(6.0, 0.62, "Supplied via gates/reversible.json | Enables direct synthesis of classical functions into reversible circuits",
            ha='center', va='center', fontsize=9.5, fontweight='bold', color=COLOR_PURPLE)

    ax.set_xlim(0, 12); ax.set_ylim(0.1, 5.8)
    return save_fig(fig, "slide12_cap2_step4_reversible_gates.png")


def make_slide13():  # Cap 2, Step 5: Automated Oracle Synthesis Cases
    fig, ax = plt.subplots(figsize=(12, 6.2), dpi=250)
    ax.set_facecolor(COLOR_BG); fig.patch.set_facecolor(COLOR_BG); ax.axis('off')

    # Step Banner
    step_tag = patches.FancyBboxPatch((0.8, 5.0), 10.4, 0.65, boxstyle="round,pad=0.08",
                                     facecolor=COLOR_PURPLE, edgecolor="none")
    ax.add_patch(step_tag)
    ax.text(1.2, 5.32, "CAPABILITY 2 | STEP 5: AUTOMATED ORACLE SYNTHESIS CASE STUDIES",
            fontsize=12, fontweight='bold', color='white', va='center')

    cases = [
        ("Case A: XOR Bit-Flip Oracle", "--bool-expr \"x0 ^ x1\"\nAllowed: Clifford+T (CNOT only)",
         "Synthesized: 2 CNOTs in 10 expansions (<0.001s)", COLOR_BLUE, 0.8),
        ("Case B: AND Phase Oracle", "--bool-expr \"x0 and x1\"\n--oracle-mode phase",
         "Synthesized: 1 CZ gate (0 ancilla overhead!)", COLOR_PURPLE, 4.4),
        ("Case C: AND Reversible Bit-Flip", "--bool-expr \"x0 and x1\"\nAllowed: Reversible (CCX)",
         "Synthesized: 1 Toffoli (CCX) gate in 1 expansion", COLOR_TEAL, 8.0),
    ]

    for title, cmd, result, col, x in cases:
        card = patches.FancyBboxPatch((x, 1.0), 3.2, 3.7, boxstyle="round,pad=0.12",
                                      facecolor="white", edgecolor=col, lw=2)
        ax.add_patch(card)
        ax.text(x + 1.6, 4.3, title, ha='center', fontsize=10.5, fontweight='bold', color=col)
        ax.text(x + 1.6, 3.7, cmd, ha='center', fontsize=8, color=COLOR_GRAY, multialignment='center')

        badge = patches.FancyBboxPatch((x + 0.2, 3.0), 2.8, 0.45, boxstyle="round,pad=0.06",
                                       facecolor=col, edgecolor="none")
        ax.add_patch(badge)
        ax.text(x + 1.6, 3.22, result, ha='center', fontsize=8.5, fontweight='bold', color='white')

        # Circuit diagrams
        if x < 2.0:  # Case A: 2 CNOTs
            for w in range(3):
                yw = 2.4 - w * 0.6
                ax.plot([x + 0.5, x + 2.7], [yw, yw], color=COLOR_GRAY, lw=1.5)
                ax.text(x + 0.4, yw, f"q{w}", ha='right', va='center', fontsize=7.5, color=COLOR_NAVY)
            ax.plot([x + 1.2, x + 1.2], [1.2, 2.4], color=col, lw=1.8)
            ax.plot(x + 1.2, 2.4, 'o', color=col, ms=6)
            c1 = plt.Circle((x + 1.2, 1.2), 0.12, facecolor="white", edgecolor=col, lw=1.5, zorder=5)
            ax.add_patch(c1)
            ax.plot([x + 2.0, x + 2.0], [1.2, 1.8], color=col, lw=1.8)
            ax.plot(x + 2.0, 1.8, 'o', color=col, ms=6)
            c2 = plt.Circle((x + 2.0, 1.2), 0.12, facecolor="white", edgecolor=col, lw=1.5, zorder=5)
            ax.add_patch(c2)
        elif x < 6.0:  # Case B: CZ
            for w in range(2):
                yw = 2.2 - w * 0.8
                ax.plot([x + 0.5, x + 2.7], [yw, yw], color=COLOR_GRAY, lw=1.5)
                ax.text(x + 0.4, yw, f"q{w}", ha='right', va='center', fontsize=7.5, color=COLOR_NAVY)
            ax.plot([x + 1.6, x + 1.6], [1.4, 2.2], color=col, lw=2)
            ax.plot(x + 1.6, 2.2, 'o', color=col, ms=7)
            ax.plot(x + 1.6, 1.4, 'o', color=col, ms=7)
            ax.text(x + 1.6, 0.9, "Phase Kickback: (-1)^(x0 x1)", ha='center', fontsize=7.5, color=col)
        else:  # Case C: Toffoli
            for w in range(3):
                yw = 2.4 - w * 0.6
                ax.plot([x + 0.5, x + 2.7], [yw, yw], color=COLOR_GRAY, lw=1.5)
                ax.text(x + 0.4, yw, f"q{w}", ha='right', va='center', fontsize=7.5, color=COLOR_NAVY)
            ax.plot([x + 1.6, x + 1.6], [1.2, 2.4], color=col, lw=2)
            ax.plot(x + 1.6, 2.4, 'o', color=col, ms=6)
            ax.plot(x + 1.6, 1.8, 'o', color=col, ms=6)
            c3 = plt.Circle((x + 1.6, 1.2), 0.12, facecolor="white", edgecolor=col, lw=1.5, zorder=5)
            ax.add_patch(c3)

    ax.set_xlim(0, 12); ax.set_ylim(0.4, 5.8)
    return save_fig(fig, "slide13_cap2_step5_oracle_cases.png")


def make_slide14():  # Cap 2, SOTA Comparison
    fig, ax = plt.subplots(figsize=(12, 6.2), dpi=250)
    ax.set_facecolor(COLOR_BG); fig.patch.set_facecolor(COLOR_BG); ax.axis('off')

    # SOTA Banner
    banner = patches.FancyBboxPatch((0.8, 5.0), 10.4, 0.65, boxstyle="round,pad=0.08",
                                   facecolor=COLOR_NAVY, edgecolor=COLOR_PURPLE, lw=1.8)
    ax.add_patch(banner)
    ax.text(1.2, 5.32, "CAPABILITY 2 | RESEARCH FRONTIER: WHERE Q-SYNTH GOES BEYOND PRIOR WORK",
            fontsize=12, fontweight='bold', color='white', va='center')

    # Left: Prior Art Limitations
    left = patches.FancyBboxPatch((0.8, 0.8), 4.8, 3.9, boxstyle="round,pad=0.15",
                                 facecolor="white", edgecolor=COLOR_CORAL, lw=1.8)
    ax.add_patch(left)
    ax.text(3.2, 4.4, "Conventional Logic Synthesis (RevLib, Bennett Uncomputation)", ha='center',
            fontsize=10.5, fontweight='bold', color=COLOR_CORAL)

    prior_points = [
        ("Mandatory Ancilla Allocation", "Classical synthesis pipelines always allocate extra ancillae even when phase kickback could eliminate them entirely."),
        ("Symmetric Uncomputation Overhead", "Requires doubling circuit depth (U_f followed by U_f†) to reset scratch wires to |0⟩."),
        ("No Phase-Oracle Awareness", "Cannot directly compile diagonal phase oracles (-1)^f(x); forces bit-flip oracles with ancilla."),
        ("Disconnected Logic Interfaces", "Requires external tools (e.g. ABC or RevLib) to convert logic before feeding into quantum SDKs."),
    ]
    for i, (head, body) in enumerate(prior_points):
        y = 3.7 - i * 0.75
        ax.text(1.1, y + 0.12, "✕ " + head, fontsize=9.5, fontweight='bold', color=COLOR_CORAL)
        ax.text(1.3, y - 0.15, body, fontsize=8, color=COLOR_DARK)

    # Right: Q-Synth Research Edge
    right = patches.FancyBboxPatch((6.0, 0.8), 5.2, 3.9, boxstyle="round,pad=0.15",
                                  facecolor="white", edgecolor=COLOR_TEAL, lw=1.8)
    ax.add_patch(right)
    ax.text(8.6, 4.4, "Q-Synth Breakthrough & Advantages", ha='center',
            fontsize=11, fontweight='bold', color=COLOR_TEAL)

    qsynth_points = [
        ("Multi-Paradigm Oracle Generation", "Seamlessly supports bit-flip, zero-ancilla phase, and reversible permutation oracles."),
        ("Automatic Ancilla-Free Phase Kickback", "Automatically discovers that AND phase oracle compiles into a single 2-qubit CZ gate."),
        ("Direct Python AST Logic Interface", "Compiles raw Python expressions directly with AST security checks and wire inference."),
        ("Minimal Reversible Sequence Discovery", "Synthesizes minimal Toffoli/Fredkin/CNOT networks without uncomputation bloat."),
    ]
    for i, (head, body) in enumerate(qsynth_points):
        y = 3.7 - i * 0.75
        ax.text(6.3, y + 0.12, "✓ " + head, fontsize=9.5, fontweight='bold', color=COLOR_TEAL)
        ax.text(6.5, y - 0.15, body, fontsize=8, color=COLOR_DARK)

    ax.set_xlim(0, 12); ax.set_ylim(0.4, 5.8)
    return save_fig(fig, "slide14_cap2_sota_comparison.png")


# ==============================================================================
# CAPABILITY 3: CIRCUIT OPTIMIZATION (STEPS 1-5 + SOTA)
# ==============================================================================
def make_slide15():  # Cap 3, Step 1: Ingestion & Move Tokenization
    fig, ax = plt.subplots(figsize=(12, 6.2), dpi=250)
    ax.set_facecolor(COLOR_BG); fig.patch.set_facecolor(COLOR_BG); ax.axis('off')

    # Step Banner
    step_tag = patches.FancyBboxPatch((0.8, 5.0), 10.4, 0.65, boxstyle="round,pad=0.08",
                                     facecolor=COLOR_TEAL, edgecolor="none")
    ax.add_patch(step_tag)
    ax.text(1.2, 5.32, "CAPABILITY 3 | STEP 1: CIRCUIT INGESTION & DIRECTED MOVE TOKENIZATION",
            fontsize=12, fontweight='bold', color='white', va='center')

    # Left: Ingestion Formats
    left = patches.FancyBboxPatch((0.8, 1.0), 4.8, 3.7, boxstyle="round,pad=0.15",
                                 facecolor="white", edgecolor=COLOR_TEAL, lw=1.8)
    ax.add_patch(left)
    ax.text(3.2, 4.35, "Circuit Input Parsing", ha='center', fontsize=11.5, fontweight='bold', color=COLOR_TEAL)

    formats = [
        ("Bracket Notation:", "--circuit 'H[0], CNOT[0,1], H[0]'"),
        ("Space Notation:", "--circuit 'h 0; cx 0 1; h 0'"),
        ("File Loading:", "--circuit-file unoptimized.qasm"),
        ("Qubit Auto-Inference:", "Infers total wire count n from maximum referenced wire index"),
    ]
    for i, (hd, body) in enumerate(formats):
        y = 3.6 - i * 0.75
        sub = patches.FancyBboxPatch((1.1, y - 0.25), 4.2, 0.6, boxstyle="round,pad=0.08",
                                     facecolor=COLOR_LIGHT_TEAL, edgecolor="none")
        ax.add_patch(sub)
        ax.text(1.3, y + 0.12, hd, fontsize=9, fontweight='bold', color=COLOR_TEAL)
        ax.text(1.3, y - 0.14, body, fontsize=8, color=COLOR_DARK)

    # Right: Move Data Structure & Baseline Matrix Computation
    right = patches.FancyBboxPatch((6.0, 1.0), 5.2, 3.7, boxstyle="round,pad=0.15",
                                  facecolor="white", edgecolor=COLOR_NAVY, lw=1.8)
    ax.add_patch(right)
    ax.text(8.6, 4.35, "Internal Move Data Representation", ha='center',
            fontsize=11.5, fontweight='bold', color=COLOR_NAVY)

    notes = [
        ("Structured Move Objects:", "Move(gate=Gate('CNOT'), placement=(0, 1))"),
        ("Immutable Hashability:", "Gates implement custom matrix hash for instant equality tests"),
        ("Baseline Target Unitary:", r"Calculates $U_{\mathrm{target}} = \prod_{\ell=1}^M G_\ell$ to establish verification ground-truth"),
        ("Allowed Basis Binding:", "Loads target gate set; ensures optimizer only emits allowed gates"),
    ]
    for i, (hd, body) in enumerate(notes):
        y = 3.6 - i * 0.75
        sub = patches.FancyBboxPatch((6.3, y - 0.25), 4.6, 0.6, boxstyle="round,pad=0.08",
                                     facecolor=COLOR_LIGHT_GRAY, edgecolor="none")
        ax.add_patch(sub)
        ax.text(6.5, y + 0.12, hd, fontsize=9, fontweight='bold', color=COLOR_NAVY)
        ax.text(6.5, y - 0.14, body, fontsize=8, color=COLOR_DARK)

    ax.set_xlim(0, 12); ax.set_ylim(0.4, 5.8)
    return save_fig(fig, "slide15_cap3_step1_ingestion.png")


def make_slide16():  # Cap 3, Step 2: Commutation Matrix Analysis
    fig, ax = plt.subplots(figsize=(12, 6.2), dpi=250)
    ax.set_facecolor(COLOR_BG); fig.patch.set_facecolor(COLOR_BG); ax.axis('off')

    # Step Banner
    step_tag = patches.FancyBboxPatch((0.8, 5.0), 10.4, 0.65, boxstyle="round,pad=0.08",
                                     facecolor=COLOR_TEAL, edgecolor="none")
    ax.add_patch(step_tag)
    ax.text(1.2, 5.32, "CAPABILITY 3 | STEP 2: COMMUTATION MATRIX ANALYSIS ACROSS DISJOINT WIRES",
            fontsize=12, fontweight='bold', color='white', va='center')

    # Commutation Math Box
    math_box = patches.FancyBboxPatch((0.8, 3.6), 10.4, 1.1, boxstyle="round,pad=0.1",
                                     facecolor="white", edgecolor=COLOR_NAVY, lw=1.5)
    ax.add_patch(math_box)
    ax.text(1.2, 4.35, r"Mathematical Commutation Criterion: $[G_i, G_j] = G_i G_j - G_j G_i = 0$",
            fontsize=12, fontweight='bold', color=COLOR_NAVY)
    ax.text(1.2, 3.9, "When gates commute, their execution order can be exchanged freely without altering the accumulated circuit unitary.",
            fontsize=9, color=COLOR_GRAY)

    # Two Commutation Cases
    cases = [
        ("Case 1: Disjoint Wire Placements", r"$\mathrm{placement}(G_i) \cap \mathrm{placement}(G_j) = \emptyset$",
         "• Example: CNOT[0,1] and H[2]\n• Wires are independent: G_i acts on q0,q1; G_j acts on q2\n• Guaranteed commute: CNOT[0,1] · H[2] = H[2] · CNOT[0,1]\n• Permitted to sweep past all intermediate disjoint gates",
         COLOR_BLUE, 0.8),
        ("Case 2: Commuting Overlapping Matrices", r"$\max |M_i M_j - M_j M_i| < 10^{-9}$",
         "• Example: Diagonal gates (Z, S, T, CZ) on shared wires\n• Numerical matrix check verifies zero commutator\n• Permitted to commute through to unlock cancellations\n• Preserves exact overall unitary operator",
         COLOR_PURPLE, 6.2),
    ]

    for title, eq, desc, col, x in cases:
        card = patches.FancyBboxPatch((x, 1.0), 5.0, 2.3, boxstyle="round,pad=0.12",
                                      facecolor="white", edgecolor=col, lw=2)
        ax.add_patch(card)
        ax.text(x + 2.5, 3.0, title, ha='center', fontsize=11, fontweight='bold', color=col)
        ax.text(x + 2.5, 2.55, eq, ha='center', fontsize=9.5, color=COLOR_NAVY)
        ax.text(x + 0.4, 1.8, desc, fontsize=8, color=COLOR_DARK)

    ax.set_xlim(0, 12); ax.set_ylim(0.4, 5.8)
    return save_fig(fig, "slide16_cap3_step2_commutation.png")


def make_slide17():  # Cap 3, Step 3: Peephole Reduction Rules
    fig, ax = plt.subplots(figsize=(12, 6.2), dpi=250)
    ax.set_facecolor(COLOR_BG); fig.patch.set_facecolor(COLOR_BG); ax.axis('off')

    # Step Banner
    step_tag = patches.FancyBboxPatch((0.8, 5.0), 10.4, 0.65, boxstyle="round,pad=0.08",
                                     facecolor=COLOR_TEAL, edgecolor="none")
    ax.add_patch(step_tag)
    ax.text(1.2, 5.32, "CAPABILITY 3 | STEP 3: COMMUTATION-AWARE ALGEBRAIC PEEPHOLE REDUCTION",
            fontsize=12, fontweight='bold', color='white', va='center')

    rules = [
        ("Rule 1: Commute to Expose Adjacency",
         "Sweep gates forward past commuting gates to bring potential matching pairs into adjacent contact.",
         "CNOT[0,1] · H[2] · CNOT[0,1]  ==>  H[2] · CNOT[0,1] · CNOT[0,1]", COLOR_BLUE, 3.6),
        ("Rule 2: Self-Inverse Cancellation (100% Elimination)",
         "Adjacent self-inverse pairs collapse to Identity and are dropped immediately.",
         r"H[0] · H[0] = I    |    CNOT[0,1] · CNOT[0,1] = I    ==>    $\emptyset$ (0 gates)", COLOR_CORAL, 2.2),
        ("Rule 3: Gate Merging into Allowed Basis (-50% Elimination)",
         "Sequential rotations on identical placement merge into a single allowable gate.",
         r"T[0] · T[0] = S[0]    |    S[0] · S[0] = Z[0]    ==>    1 combined gate", COLOR_TEAL, 0.8),
    ]

    for title, desc, code, col, y in rules:
        card = patches.FancyBboxPatch((0.8, y), 10.4, 1.25, boxstyle="round,pad=0.1",
                                      facecolor="white", edgecolor=col, lw=1.8)
        ax.add_patch(card)
        ax.text(1.1, y + 0.95, title, fontsize=10.5, fontweight='bold', color=col)
        ax.text(1.1, y + 0.65, desc, fontsize=8.5, color=COLOR_DARK)

        sub = patches.FancyBboxPatch((1.1, y + 0.1), 9.8, 0.38, boxstyle="round,pad=0.05",
                                     facecolor=COLOR_LIGHT_GRAY, edgecolor="none")
        ax.add_patch(sub)
        ax.text(6.0, y + 0.28, code, ha='center', va='center', fontsize=8.5, fontweight='bold', color=COLOR_NAVY)

    ax.set_xlim(0, 12); ax.set_ylim(0.4, 5.8)
    return save_fig(fig, "slide17_cap3_step3_peephole.png")


def make_slide18():  # Cap 3, Step 4: Global Resynthesis
    fig, ax = plt.subplots(figsize=(12, 6.2), dpi=250)
    ax.set_facecolor(COLOR_BG); fig.patch.set_facecolor(COLOR_BG); ax.axis('off')

    # Step Banner
    step_tag = patches.FancyBboxPatch((0.8, 5.0), 10.4, 0.65, boxstyle="round,pad=0.08",
                                     facecolor=COLOR_TEAL, edgecolor="none")
    ax.add_patch(step_tag)
    ax.text(1.2, 5.32, "CAPABILITY 3 | STEP 4: GLOBAL SYNTHESIS-DRIVEN RESYNTHESIS",
            fontsize=12, fontweight='bold', color='white', va='center')

    # Left: The Limitation of Pure Peephole Rules
    left = patches.FancyBboxPatch((0.8, 1.0), 4.8, 3.7, boxstyle="round,pad=0.15",
                                 facecolor="white", edgecolor=COLOR_CORAL, lw=1.8)
    ax.add_patch(left)
    ax.text(3.2, 4.35, "Where Peephole Rules Stall", ha='center',
            fontsize=11.5, fontweight='bold', color=COLOR_CORAL)

    notes_left = [
        ("Complex Entangled Blocks:", "e.g. CNOT · (H ⊗ H) · CNOT · (H ⊗ H) · CNOT"),
        ("Non-Commuting Barriers:", "Hadamards on target wires do not commute with CNOT controls"),
        ("Rule-Based Blind Spots:", "No local 2-gate peephole rule can simplify this 7-gate SWAP"),
        ("Result without Resynthesis:", "Peephole reduction makes 0 progress; 7 gates remain"),
    ]
    for i, (hd, body) in enumerate(notes_left):
        y = 3.6 - i * 0.75
        sub = patches.FancyBboxPatch((1.1, y - 0.25), 4.2, 0.6, boxstyle="round,pad=0.08",
                                     facecolor=COLOR_LIGHT_CORAL, edgecolor="none")
        ax.add_patch(sub)
        ax.text(1.3, y + 0.12, hd, fontsize=9, fontweight='bold', color=COLOR_CORAL)
        ax.text(1.3, y - 0.14, body, fontsize=8, color=COLOR_DARK)

    # Right: Global Beam Resynthesis Breakthrough
    right = patches.FancyBboxPatch((6.0, 1.0), 5.2, 3.7, boxstyle="round,pad=0.15",
                                  facecolor="white", edgecolor=COLOR_TEAL, lw=1.8)
    ax.add_patch(right)
    ax.text(8.6, 4.35, "Q-Synth Global Resynthesis Engine", ha='center',
            fontsize=11.5, fontweight='bold', color=COLOR_TEAL)

    notes_right = [
        ("Full Unitary Extraction:", r"Computes overall matrix $U = \prod_{\ell=1}^7 G_\ell$"),
        ("Depth-Constrained Search:", "Launches beam search with max_depth = len(C) - 1 = 6"),
        ("Allowed Basis Enforcement:", "Searches using strictly user-permitted gates (e.g. CNOT only)"),
        ("Radical Gate Reduction:", "Synthesizes minimal 3-CNOT sequence: 7 gates -> 3 gates (-57.1%!)"),
    ]
    for i, (hd, body) in enumerate(notes_right):
        y = 3.6 - i * 0.75
        sub = patches.FancyBboxPatch((6.3, y - 0.25), 4.6, 0.6, boxstyle="round,pad=0.08",
                                     facecolor=COLOR_LIGHT_TEAL, edgecolor="none")
        ax.add_patch(sub)
        ax.text(6.5, y + 0.12, hd, fontsize=9, fontweight='bold', color=COLOR_TEAL)
        ax.text(6.5, y - 0.14, body, fontsize=8, color=COLOR_NAVY)

    # Middle Arrow
    ax.annotate("", xy=(5.8, 2.8), xytext=(5.3, 2.8),
                arrowprops=dict(arrowstyle="-|>", color=COLOR_NAVY, lw=2.5))

    ax.set_xlim(0, 12); ax.set_ylim(0.4, 5.8)
    return save_fig(fig, "slide18_cap3_step4_global_resynth.png")


def make_slide19():  # Cap 3, Step 5: Sliding-Window Resynthesis
    fig, ax = plt.subplots(figsize=(12, 6.2), dpi=250)
    ax.set_facecolor(COLOR_BG); fig.patch.set_facecolor(COLOR_BG); ax.axis('off')

    # Step Banner
    step_tag = patches.FancyBboxPatch((0.8, 5.0), 10.4, 0.65, boxstyle="round,pad=0.08",
                                     facecolor=COLOR_TEAL, edgecolor="none")
    ax.add_patch(step_tag)
    ax.text(1.2, 5.32, "CAPABILITY 3 | STEP 5: SLIDING-WINDOW BLOCK RESYNTHESIS & FEEDBACK LOOPS",
            fontsize=12, fontweight='bold', color='white', va='center')

    # Window Sweep Visual
    sweep_box = patches.FancyBboxPatch((0.8, 3.2), 10.4, 1.5, boxstyle="round,pad=0.1",
                                       facecolor="white", edgecolor=COLOR_NAVY, lw=1.5)
    ax.add_patch(sweep_box)
    ax.text(1.2, 4.4, "Sliding Window Block Sweeping Algorithm", fontsize=11, fontweight='bold', color=COLOR_NAVY)

    # Sequence of gate blocks
    gates = ["G1", "G2", "G3", "G4", "G5", "G6", "G7", "G8"]
    for i, g in enumerate(gates):
        xg = 1.6 + i * 1.15
        is_window = 2 <= i <= 5
        col = COLOR_PURPLE if is_window else COLOR_GRAY
        bg = COLOR_LIGHT_PURPLE if is_window else "white"
        b = patches.Rectangle((xg, 3.5), 0.9, 0.55, facecolor=bg, edgecolor=col, lw=1.5)
        ax.add_patch(b)
        ax.text(xg + 0.45, 3.77, g, ha='center', va='center', fontsize=9, fontweight='bold', color=col)

    # Bracket showing window w=4
    ax.text(5.5, 3.32, "Active Window Slice: C[i : i+w] (width w = 4)", ha='center', fontsize=8.5, fontweight='bold', color=COLOR_PURPLE)

    # Bottom Two Action Cards
    card1 = patches.FancyBboxPatch((0.8, 1.0), 4.8, 1.9, boxstyle="round,pad=0.12",
                                   facecolor="white", edgecolor=COLOR_PURPLE, lw=1.8)
    ax.add_patch(card1)
    ax.text(3.2, 2.6, "1. Local Block Synthesis", ha='center', fontsize=11, fontweight='bold', color=COLOR_PURPLE)
    ax.text(1.1, 2.1, "• Computes sub-unitary U_block = ∏ G_slice", fontsize=8.5, color=COLOR_DARK)
    ax.text(1.1, 1.7, "• Synthesizes U_block to depth <= w - 1", fontsize=8.5, color=COLOR_DARK)
    ax.text(1.1, 1.3, "• If shorter replacement found -> patch in-place", fontsize=8.5, color=COLOR_DARK)

    card2 = patches.FancyBboxPatch((6.0, 1.0), 5.2, 1.9, boxstyle="round,pad=0.12",
                                   facecolor="white", edgecolor=COLOR_CORAL, lw=1.8)
    ax.add_patch(card2)
    ax.text(8.6, 2.6, "2. Cascading Feedback Loops", ha='center', fontsize=11, fontweight='bold', color=COLOR_CORAL)
    ax.text(6.3, 2.1, "• Local replacement alters neighboring boundary gates", fontsize=8.5, color=COLOR_DARK)
    ax.text(6.3, 1.7, "• Triggers immediate re-execution of Pass 1 (Peephole)", fontsize=8.5, color=COLOR_DARK)
    ax.text(6.3, 1.3, "• Cascades further cancellations across the entire circuit", fontsize=8.5, color=COLOR_DARK)

    ax.set_xlim(0, 12); ax.set_ylim(0.4, 5.8)
    return save_fig(fig, "slide19_cap3_step5_sliding_window.png")


def make_slide20():  # Cap 3, SOTA Comparison
    fig, ax = plt.subplots(figsize=(12, 6.2), dpi=250)
    ax.set_facecolor(COLOR_BG); fig.patch.set_facecolor(COLOR_BG); ax.axis('off')

    # SOTA Banner
    banner = patches.FancyBboxPatch((0.8, 5.0), 10.4, 0.65, boxstyle="round,pad=0.08",
                                   facecolor=COLOR_NAVY, edgecolor=COLOR_TEAL, lw=1.8)
    ax.add_patch(banner)
    ax.text(1.2, 5.32, "CAPABILITY 3 | RESEARCH FRONTIER: WHERE Q-SYNTH GOES BEYOND PRIOR WORK",
            fontsize=12, fontweight='bold', color='white', va='center')

    # Left: Prior Art Limitations
    left = patches.FancyBboxPatch((0.8, 0.8), 4.8, 3.9, boxstyle="round,pad=0.15",
                                 facecolor="white", edgecolor=COLOR_CORAL, lw=1.8)
    ax.add_patch(left)
    ax.text(3.2, 4.4, "Conventional Rule-Based Optimizers (Qiskit Transpiler L1-L3)", ha='center',
            fontsize=10.5, fontweight='bold', color=COLOR_CORAL)

    prior_points = [
        ("Rigid Template Libraries", "Optimizers match only predetermined subcircuit patterns; cannot discover novel replacements outside hardcoded templates."),
        ("Fragile to Intermediate Gates", "Any non-commuting gate in a block completely breaks pattern recognition, halting optimization."),
        ("No Resynthesis from Unitary", "Cannot isolate a sub-unitary matrix and synthesize a cleaner replacement from scratch."),
        ("Locked Allowed Bases", "Cannot optimize a circuit while forcing all resulting gates into a strictly user-specified basis subset (e.g. CNOT only)."),
    ]
    for i, (head, body) in enumerate(prior_points):
        y = 3.7 - i * 0.75
        ax.text(1.1, y + 0.12, "✕ " + head, fontsize=9.5, fontweight='bold', color=COLOR_CORAL)
        ax.text(1.3, y - 0.15, body, fontsize=8, color=COLOR_DARK)

    # Right: Q-Synth Research Edge
    right = patches.FancyBboxPatch((6.0, 0.8), 5.2, 3.9, boxstyle="round,pad=0.15",
                                  facecolor="white", edgecolor=COLOR_TEAL, lw=1.8)
    ax.add_patch(right)
    ax.text(8.6, 4.4, "Q-Synth Optimization Breakthroughs", ha='center',
            fontsize=11, fontweight='bold', color=COLOR_TEAL)

    qsynth_points = [
        ("Hybrid Algebraic & Resynthesis Passes", "Marries commutation-aware peephole cancellation with synthesis-driven search to conquer template blind spots."),
        ("User-Constrained Gate Basis", "Guarantees that every optimized gate belongs strictly to the user-permitted library (--gate-names)."),
        ("Sliding-Window Resynthesis Sweep", "Scales beyond shallow depth by optimizing local matrix blocks independently."),
        ("Empirical Reductions (Up to 100%)", "Solves 7-gate SWAP -> 3 CNOTs (-57.1%) and cancels double SWAP 6 CNOTs -> 0 (-100%) in <0.01s."),
    ]
    for i, (head, body) in enumerate(qsynth_points):
        y = 3.7 - i * 0.75
        ax.text(6.3, y + 0.12, "✓ " + head, fontsize=9.5, fontweight='bold', color=COLOR_TEAL)
        ax.text(6.5, y - 0.15, body, fontsize=8, color=COLOR_DARK)

    ax.set_xlim(0, 12); ax.set_ylim(0.4, 5.8)
    return save_fig(fig, "slide20_cap3_sota_comparison.png")


# ==============================================================================
# PRESENTATION BUILDER
# ==============================================================================
def build_research_presentation():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    slides_info = [
        # OPENING SLIDE
        ("Q-Synth: Autonomous Quantum Circuit Synthesis & Optimization",
         "A First-Principles Framework for Unitary Synthesis, Boolean Compilation, and Gate-Constrained Optimization",
         make_slide1()),

        # CAPABILITY 1: UNITARY SYNTHESIS (STEPS 1-6 + SOTA)
        ("Capability 1 | Step 1: Input Ingestion & Phase-Insensitive Metric",
         "Normalized Hilbert-Schmidt similarity metric enabling exact physical equivalence with arbitrary global phase",
         make_slide2()),

        ("Capability 1 | Step 2: Ordered Permutation Move Enumeration",
         "Combinatorial placement generation P(n, k) mapping 1-, 2-, and 3-qubit gates across global wires",
         make_slide3()),

        ("Capability 1 | Step 3: Kronecker Sub-Word Matrix Embedding",
         "Bit-slice projection architecture embedding local gate matrices into full 2ⁿ x 2ⁿ Hilbert space",
         make_slide4()),

        ("Capability 1 | Step 4: Quantized Complex Hash Grid Deduplication",
         "Fixed 10⁹ rounding grid collapsing redundant physical paths to stop combinatorial state explosion",
         make_slide5()),

        ("Capability 1 | Step 5: Guided Beam-Search Exploration & Pruning",
         "Breadth-first expansion ranked by Hilbert-Schmidt trace fidelity with top-K beam pruning",
         make_slide6()),

        ("Capability 1 | Step 6: Post-Search Verification & Residual Error Analysis",
         "Exact numerical verification of fidelity, global phase extraction, and residual element error",
         make_slide7()),

        ("Capability 1 | Research Frontier: Where Q-Synth Goes Beyond Prior Work",
         "Overcoming fixed-basis compiler lock-in with arbitrary user-defined gate library synthesis",
         make_slide8()),

        # CAPABILITY 2: BOOLEAN & TRUTH TABLE SYNTHESIS (STEPS 1-5 + SOTA)
        ("Capability 2 | Step 1: Safe AST Logic Parsing & Introspection",
         "Abstract syntax tree sanitization, boolean operator extraction, and automatic variable wire ordering",
         make_slide9()),

        ("Capability 2 | Step 2: Truth Table Evaluation & Little-Endian Mapping",
         "Evaluating 2ⁿ basis state responses under the industry-standard least significant bit (LSB) convention",
         make_slide10()),

        ("Capability 2 | Step 3: Quantum Oracle Embedding Paradigms",
         "Constructing bit-flip (n+1 wires), zero-ancilla phase (n wires), and reversible permutation matrices",
         make_slide11()),

        ("Capability 2 | Step 4: Reversible Logic Basis Integration",
         "Multi-qubit classical reversible gates: Toffoli (CCX), Fredkin (CSWAP), CNOT, and NOT",
         make_slide12()),

        ("Capability 2 | Step 5: Automated Oracle Synthesis Case Studies",
         "Empirical compilation of XOR into 2 CNOTs, AND into CZ phase gate, and AND into Toffoli CCX",
         make_slide13()),

        ("Capability 2 | Research Frontier: Where Q-Synth Goes Beyond Prior Work",
         "Eliminating uncomputation ancilla overhead and discovering direct phase kickback implementations",
         make_slide14()),

        # CAPABILITY 3: CIRCUIT OPTIMIZATION (STEPS 1-5 + SOTA)
        ("Capability 3 | Step 1: Circuit Ingestion & Directed Move Tokenization",
         "Parsing raw gate sequences and establishing the baseline composite unitary operator ground-truth",
         make_slide15()),

        ("Capability 3 | Step 2: Commutation Matrix Analysis Across Disjoint Wires",
         "Evaluating wire overlaps and matrix commutators [A, B] = 0 to enable long-range gate sweeps",
         make_slide16()),

        ("Capability 3 | Step 3: Commutation-Aware Algebraic Peephole Reduction",
         "Sweeping commuting gates adjacent to trigger self-inverse cancellations and single-gate collapsing",
         make_slide17()),

        ("Capability 3 | Step 4: Global Synthesis-Driven Resynthesis",
         "Conquering template matcher blind spots by synthesizing entire entangled subcircuits from scratch",
         make_slide18()),

        ("Capability 3 | Step 5: Sliding-Window Block Resynthesis & Feedback Loops",
         "Sweeping local sub-windows with depth-constrained beam search to cascade global circuit reductions",
         make_slide19()),

        ("Capability 3 | Research Frontier: Where Q-Synth Goes Beyond Prior Work",
         "Replacing brittle template matching with constrained synthesis-driven optimization (up to 100% reduction)",
         make_slide20()),
    ]

    for title, subtitle, img_path in slides_info:
        slide = prs.slides.add_slide(blank_layout)

        # Header Text Box
        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.35), Inches(11.7), Inches(0.9))
        tf = title_box.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        p_title = tf.paragraphs[0]
        p_title.text = title
        p_title.font.size = Pt(21)
        p_title.font.bold = True
        p_title.font.color.rgb = RGBColor(15, 23, 42)  # Navy

        p_sub = tf.add_paragraph()
        p_sub.text = subtitle
        p_sub.font.size = Pt(10.5)
        p_sub.font.color.rgb = RGBColor(100, 116, 139)  # Gray

        # Centered High-Res Diagram Image
        slide.shapes.add_picture(img_path, Inches(0.8), Inches(1.35), width=Inches(11.733))

    out_file = os.path.join(OUTPUT_DIR, "Q-Synth_Research_Capabilities.pptx")
    prs.save(out_file)
    print(f"Successfully generated 20-slide research presentation: {out_file}")
    return out_file


if __name__ == "__main__":
    build_research_presentation()
