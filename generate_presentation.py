"""Script to generate all diagrams and assemble the PowerPoint presentation for Q-Synth."""

import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor

OUTPUT_DIR = "presentation"
FIG_DIR = os.path.join(OUTPUT_DIR, "figures")
os.makedirs(FIG_DIR, exist_ok=True)

# Use DejaVu Sans for complete Unicode mathematical symbol coverage
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


def fig1_title_overview():
    fig, ax = plt.subplots(figsize=(12, 6.2), dpi=250)
    ax.set_facecolor(COLOR_BG)
    fig.patch.set_facecolor(COLOR_BG)
    ax.axis('off')

    # Central Core Box
    core = patches.FancyBboxPatch((4.2, 1.8), 3.6, 2.6, boxstyle="round,pad=0.2",
                                  facecolor=COLOR_BLUE, edgecolor=COLOR_NAVY, linewidth=2)
    ax.add_patch(core)
    ax.text(6.0, 3.4, "Q-SYNTH CORE", ha='center', va='center',
            fontsize=18, fontweight='bold', color='white')
    ax.text(6.0, 2.8, "Automated Beam-Search Synthesis\n& Circuit Optimizer Engine",
            ha='center', va='center', fontsize=11, color='#EFF6FF')
    ax.text(6.0, 2.2, r"Phase-Insensitive Metric: $s(U, V) = |\mathrm{Tr}(U^\dagger V)| / 2^n$",
            ha='center', va='center', fontsize=10, style='italic', color='#BFDBFE')

    # Input Cards (Left)
    inputs = [
        ("Unitary Matrix U", "Built-in, JSON, .npy, CSV", 4.2),
        ("Boolean Function", "f(x) logic formula (AST)", 3.0),
        ("Truth Table", "Bitstrings, lists, mappings", 1.8),
        ("User Circuit", "OpenQASM or native gate list", 0.6),
    ]
    for title, desc, y in inputs:
        box = patches.FancyBboxPatch((0.4, y), 2.8, 0.85, boxstyle="round,pad=0.1",
                                     facecolor="white", edgecolor=COLOR_PURPLE, linewidth=1.5)
        ax.add_patch(box)
        ax.text(1.8, y + 0.52, title, ha='center', va='center',
                fontsize=11, fontweight='bold', color=COLOR_NAVY)
        ax.text(1.8, y + 0.22, desc, ha='center', va='center',
                fontsize=8.5, color=COLOR_GRAY)
        # Arrow to core
        ax.annotate("", xy=(4.1, 3.1), xytext=(3.3, y + 0.42),
                    arrowprops=dict(arrowstyle="-|>", color=COLOR_PURPLE, lw=1.8,
                                    connectionstyle="arc3,rad=-0.05"))

    # Output Cards (Right)
    outputs = [
        ("Optimal Gate Sequence", "Minimal depth & gate count", 4.2),
        ("Reversible Oracles", "Bit-flip, Phase, Permutation", 3.0),
        ("Reduced Circuits", "Up to 100% redundancy eliminated", 1.8),
        ("Export & Visualization", "OpenQASM 2.0 & ASCII wire diagrams", 0.6),
    ]
    for title, desc, y in outputs:
        box = patches.FancyBboxPatch((8.8, y), 2.8, 0.85, boxstyle="round,pad=0.1",
                                     facecolor="white", edgecolor=COLOR_TEAL, linewidth=1.5)
        ax.add_patch(box)
        ax.text(10.2, y + 0.52, title, ha='center', va='center',
                fontsize=11, fontweight='bold', color=COLOR_NAVY)
        ax.text(10.2, y + 0.22, desc, ha='center', va='center',
                fontsize=8.5, color=COLOR_GRAY)
        # Arrow from core
        ax.annotate("", xy=(8.7, y + 0.42), xytext=(7.9, 3.1),
                    arrowprops=dict(arrowstyle="-|>", color=COLOR_TEAL, lw=1.8,
                                    connectionstyle="arc3,rad=-0.05"))

    # Gate Library Badge (Top)
    gate_box = patches.FancyBboxPatch((4.5, 4.9), 3.0, 0.8, boxstyle="round,pad=0.1",
                                      facecolor=COLOR_LIGHT_TEAL, edgecolor=COLOR_TEAL, lw=1.5)
    ax.add_patch(gate_box)
    ax.text(6.0, 5.4, "User-Allowed Gate Library", ha='center', va='center',
            fontsize=10.5, fontweight='bold', color=COLOR_TEAL)
    ax.text(6.0, 5.1, "Clifford+T, Reversible (Toffoli/Fredkin), Rotations",
            ha='center', va='center', fontsize=8, color=COLOR_NAVY)
    ax.annotate("", xy=(6.0, 4.5), xytext=(6.0, 4.85),
                arrowprops=dict(arrowstyle="-|>", color=COLOR_TEAL, lw=1.8))

    ax.set_xlim(0, 12)
    ax.set_ylim(0, 6)
    plt.tight_layout()
    path = os.path.join(FIG_DIR, "slide1_overview.png")
    plt.savefig(path, facecolor=fig.get_facecolor(), bbox_inches='tight')
    plt.close()
    return path


def fig2_compilation_challenge():
    fig, ax = plt.subplots(figsize=(12, 6.2), dpi=250)
    ax.set_facecolor(COLOR_BG)
    fig.patch.set_facecolor(COLOR_BG)
    ax.axis('off')

    # Left: High Level Algorithm Domain
    left_box = patches.FancyBboxPatch((0.8, 1.0), 4.2, 4.4, boxstyle="round,pad=0.2",
                                      facecolor="white", edgecolor=COLOR_BLUE, linewidth=2)
    ax.add_patch(left_box)
    ax.text(2.9, 5.0, "Algorithm & Logic Domain", ha='center', va='center',
            fontsize=14, fontweight='bold', color=COLOR_NAVY)

    items_left = [
        ("Target Unitaries", r"Continuous $2^n \times 2^n$ matrices ($4^n - 1$ DOFs)"),
        ("Classical Logic", r"Boolean functions $f(x): \{0,1\}^n \to \{0,1\}$"),
        ("Truth Tables", r"Permutations & oracles: $|x,y\rangle \to |x, y \oplus f(x)\rangle$"),
        ("Theoretical circuits", "Arbitrary multi-controlled & non-native gates"),
    ]
    for i, (head, body) in enumerate(items_left):
        y = 4.2 - i * 0.95
        sub = patches.FancyBboxPatch((1.1, y - 0.3), 3.6, 0.75, boxstyle="round,pad=0.08",
                                     facecolor=COLOR_LIGHT_BLUE, edgecolor="none")
        ax.add_patch(sub)
        ax.text(1.3, y + 0.15, head, fontsize=10, fontweight='bold', color=COLOR_BLUE)
        ax.text(1.3, y - 0.12, body, fontsize=8, color=COLOR_DARK)

    # Right: Physical Hardware Domain
    right_box = patches.FancyBboxPatch((7.0, 1.0), 4.2, 4.4, boxstyle="round,pad=0.2",
                                       facecolor="white", edgecolor=COLOR_CORAL, linewidth=2)
    ax.add_patch(right_box)
    ax.text(9.1, 5.0, "Physical Hardware Execution", ha='center', va='center',
            fontsize=14, fontweight='bold', color=COLOR_NAVY)

    items_right = [
        ("Discrete Native Basis", r"Fixed physical gates: {CX, Rz, $\sqrt{X}$} or Clifford+T"),
        ("Two-Qubit Noise Barrier", "Entangling errors ~10x higher than single-qubit gates"),
        ("Coherence Time Horizon", r"Circuit depth limited by $T_1$ / $T_2$ relaxation"),
        ("Coupling Constraints", "Restricted wire connectivity graphs (heavy-hex, linear)"),
    ]
    for i, (head, body) in enumerate(items_right):
        y = 4.2 - i * 0.95
        sub = patches.FancyBboxPatch((7.3, y - 0.3), 3.6, 0.75, boxstyle="round,pad=0.08",
                                     facecolor=COLOR_LIGHT_CORAL, edgecolor="none")
        ax.add_patch(sub)
        ax.text(7.5, y + 0.15, head, fontsize=10, fontweight='bold', color=COLOR_CORAL)
        ax.text(7.5, y - 0.12, body, fontsize=8, color=COLOR_DARK)

    # Middle Bridge / Barrier
    bridge = patches.FancyBboxPatch((5.3, 2.0), 1.4, 2.4, boxstyle="round,pad=0.1",
                                    facecolor=COLOR_NAVY, edgecolor="none")
    ax.add_patch(bridge)
    ax.text(6.0, 3.7, "COMPILATION\nGAP", ha='center', va='center',
            fontsize=11, fontweight='bold', color='white')
    ax.text(6.0, 2.9, "Q-Synth\nBridge", ha='center', va='center',
            fontsize=10, fontweight='bold', color="#38BDF8")
    ax.text(6.0, 2.3, "Minimal Gates\n& Exact Match", ha='center', va='center',
            fontsize=8, color="#94A3B8")

    # Arrows crossing
    ax.annotate("", xy=(5.2, 3.2), xytext=(4.8, 3.2),
                arrowprops=dict(arrowstyle="-|>", color=COLOR_BLUE, lw=2.5))
    ax.annotate("", xy=(7.2, 3.2), xytext=(6.8, 3.2),
                arrowprops=dict(arrowstyle="-|>", color=COLOR_CORAL, lw=2.5))

    ax.set_xlim(0, 12)
    ax.set_ylim(0, 6)
    plt.tight_layout()
    path = os.path.join(FIG_DIR, "slide2_challenge.png")
    plt.savefig(path, facecolor=fig.get_facecolor(), bbox_inches='tight')
    plt.close()
    return path


def fig3_system_architecture():
    fig, ax = plt.subplots(figsize=(12, 6.2), dpi=250)
    ax.set_facecolor(COLOR_BG)
    fig.patch.set_facecolor(COLOR_BG)
    ax.axis('off')

    stages = [
        ("STAGE 1", "Input & Validation",
         ["• Unitary matrix check", "• AST syntax safety", "• Truth table parsing", "• Inferred qubit count n"],
         COLOR_BLUE, 0.8),
        ("STAGE 2", "Move Engine",
         ["• Permutation generation", "  P(n, k) gate placements", "• Kronecker embeddings", "• Precomputed matrices"],
         COLOR_PURPLE, 3.6),
        ("STAGE 3", "Synthesis & Optimizer",
         ["• Beam-search engine", "• Quantized hash deduplication", "• Commutation peephole pass", "• Sliding-window resynthesis"],
         COLOR_TEAL, 6.4),
        ("STAGE 4", "Verification & Export",
         ["• Hilbert-Schmidt trace check", "• Global phase extraction", "• OpenQASM 2.0 export", "• Terminal ASCII diagram"],
         COLOR_CORAL, 9.2),
    ]

    for stage_num, title, bullets, col, x in stages:
        # Header banner
        hdr = patches.FancyBboxPatch((x, 4.7), 2.4, 0.5, boxstyle="round,pad=0.08",
                                     facecolor=col, edgecolor=COLOR_NAVY, lw=1.2)
        ax.add_patch(hdr)
        ax.text(x + 1.2, 4.95, stage_num, ha='center', va='center',
                fontsize=9.5, fontweight='bold', color='white')

        # Main box
        box = patches.FancyBboxPatch((x, 1.2), 2.4, 3.4, boxstyle="round,pad=0.1",
                                     facecolor="white", edgecolor=col, linewidth=2)
        ax.add_patch(box)
        ax.text(x + 1.2, 4.25, title, ha='center', va='center',
                fontsize=11, fontweight='bold', color=COLOR_NAVY)

        for j, b in enumerate(bullets):
            ax.text(x + 0.15, 3.65 - j * 0.65, b, fontsize=8.5, color=COLOR_DARK)

        # Connecting Arrow to next stage
        if x < 9.0:
            ax.annotate("", xy=(x + 2.65, 2.9), xytext=(x + 2.35, 2.9),
                        arrowprops=dict(arrowstyle="-|>", color=COLOR_NAVY, lw=2.5))

    ax.set_xlim(0, 12.4)
    ax.set_ylim(0, 6)
    plt.tight_layout()
    path = os.path.join(FIG_DIR, "slide3_pipeline.png")
    plt.savefig(path, facecolor=fig.get_facecolor(), bbox_inches='tight')
    plt.close()
    return path


def fig4_move_enumeration_embedding():
    fig, ax = plt.subplots(figsize=(12, 6.2), dpi=250)
    ax.set_facecolor(COLOR_BG)
    fig.patch.set_facecolor(COLOR_BG)
    ax.axis('off')

    # Title Banner inside diagram
    ax.text(6.0, 5.5, "Embedding a 2-Qubit Gate into an n-Qubit Register (e.g. n=3)",
            ha='center', va='center', fontsize=13, fontweight='bold', color=COLOR_NAVY)

    # Left: Wire placement schematic
    box_left = patches.FancyBboxPatch((0.8, 1.2), 4.5, 3.8, boxstyle="round,pad=0.15",
                                      facecolor="white", edgecolor=COLOR_BLUE, lw=1.8)
    ax.add_patch(box_left)
    ax.text(3.05, 4.6, "1. Wire Placement: CNOT[0, 2]", ha='center', va='center',
            fontsize=11.5, fontweight='bold', color=COLOR_BLUE)

    wires = [
        ("q0 (LSB)", "Control Wire (wire 0)", 3.8, True, "ctrl"),
        ("q1", "Untouched Wire (Identity: I)", 2.8, False, "id"),
        ("q2 (MSB)", "Target Wire (wire 1)", 1.8, True, "tgt"),
    ]
    for lbl, desc, y, active, role in wires:
        # Wire line
        ax.plot([1.2, 4.8], [y, y], color=COLOR_GRAY, lw=2)
        ax.text(0.95, y, lbl, ha='right', va='center', fontsize=9.5, fontweight='bold', color=COLOR_NAVY)
        if role == "ctrl":
            circle = plt.Circle((3.0, y), 0.14, color=COLOR_BLUE, zorder=5)
            ax.add_patch(circle)
            ax.text(3.3, y + 0.22, "control (wire 0)", fontsize=8, color=COLOR_BLUE, fontweight='bold')
        elif role == "tgt":
            circle = plt.Circle((3.0, y), 0.16, facecolor="white", edgecolor=COLOR_BLUE, lw=2, zorder=5)
            ax.add_patch(circle)
            ax.plot([2.88, 3.12], [y, y], color=COLOR_BLUE, lw=2, zorder=6)
            ax.plot([3.0, 3.0], [y - 0.12, y + 0.12], color=COLOR_BLUE, lw=2, zorder=6)
            ax.text(3.3, y - 0.22, "target (wire 1)", fontsize=8, color=COLOR_BLUE, fontweight='bold')
        elif role == "id":
            rect = patches.Rectangle((2.7, y - 0.2), 0.6, 0.4, facecolor=COLOR_LIGHT_TEAL,
                                     edgecolor=COLOR_TEAL, lw=1.2, zorder=5)
            ax.add_patch(rect)
            ax.text(3.0, y, "I", ha='center', va='center', fontsize=9, fontweight='bold', color=COLOR_TEAL)
            ax.text(3.4, y, "acts as identity", fontsize=8, color=COLOR_TEAL)

    # Vertical control-target connection
    ax.plot([3.0, 3.0], [1.8, 3.8], color=COLOR_BLUE, lw=2, zorder=4)

    # Right: Kronecker / Sub-word projection math
    box_right = patches.FancyBboxPatch((6.0, 1.2), 5.2, 3.8, boxstyle="round,pad=0.15",
                                       facecolor="white", edgecolor=COLOR_PURPLE, lw=1.8)
    ax.add_patch(box_right)
    ax.text(8.6, 4.6, "2. Matrix Embedding Expansion", ha='center', va='center',
            fontsize=11.5, fontweight='bold', color=COLOR_PURPLE)

    math_lines = [
        r"Full dimension: $2^n \times 2^n = 8 \times 8$ matrix",
        "Kronecker bit-level embedding rule:",
        "Embed(G, n, p)[row, col] = ",
        "  • G[grow, gcol]  if untouched bits agree",
        "  • 0              if untouched bits differ",
        "grow = sum(((row >> p[w]) & 1) << w)",
        "gcol = sum(((col >> p[w]) & 1) << w)",
        "Permutation Placements for n=3, 2-qubit gate:",
        "  P(3, 2) = 3! / 1! = 6 placements: [0,1], [1,0],",
        "  [0,2], [2,0], [1,2], [2,1]"
    ]
    for i, line in enumerate(math_lines):
        col = COLOR_PURPLE if i in (0, 1, 7) else COLOR_DARK
        wt = 'bold' if i in (0, 7) else 'normal'
        ax.text(6.3, 4.15 - i * 0.35, line, fontsize=8.5, color=col, fontweight=wt)

    # Arrow between boxes
    ax.annotate("", xy=(5.8, 3.1), xytext=(5.3, 3.1),
                arrowprops=dict(arrowstyle="-|>", color=COLOR_NAVY, lw=2.5))

    ax.set_xlim(0, 12)
    ax.set_ylim(0, 6)
    plt.tight_layout()
    path = os.path.join(FIG_DIR, "slide4_embedding.png")
    plt.savefig(path, facecolor=fig.get_facecolor(), bbox_inches='tight')
    plt.close()
    return path


def fig5_beam_search_dedup():
    fig, ax = plt.subplots(figsize=(12, 6.2), dpi=250)
    ax.set_facecolor(COLOR_BG)
    fig.patch.set_facecolor(COLOR_BG)
    ax.axis('off')

    # Tree root (Depth 0: Identity)
    root = patches.Circle((1.5, 3.0), 0.5, facecolor=COLOR_NAVY, edgecolor=COLOR_BLUE, lw=2)
    ax.add_patch(root)
    ax.text(1.5, 3.0, "Depth 0\nV₀ = I", ha='center', va='center',
            fontsize=9.5, fontweight='bold', color='white')

    # Depth 1 level
    d1_y = [4.5, 3.5, 2.5, 1.5]
    for i, y in enumerate(d1_y):
        col = COLOR_BLUE if i < 3 else COLOR_GRAY
        c = patches.Circle((4.2, y), 0.4, facecolor="white", edgecolor=col, lw=1.8)
        ax.add_patch(c)
        ax.text(4.2, y, f"V_{i+1}", ha='center', va='center', fontsize=9, fontweight='bold', color=col)
        ax.annotate("", xy=(3.8, y), xytext=(2.0, 3.0),
                    arrowprops=dict(arrowstyle="-|>", color=col, lw=1.5))

    # Deduplication Filter Banner (Between Depth 1 and 2)
    filter_box = patches.FancyBboxPatch((5.4, 1.0), 2.2, 4.2, boxstyle="round,pad=0.1",
                                         facecolor=COLOR_LIGHT_PURPLE, edgecolor=COLOR_PURPLE, lw=1.8)
    ax.add_patch(filter_box)
    ax.text(6.5, 4.8, "Quantized Hash\nDeduplication", ha='center', va='center',
            fontsize=10.5, fontweight='bold', color=COLOR_PURPLE)
    ax.text(6.5, 3.8, r"Hash Grid: $10^9$" + "\nkey = bytes(\n  round(Re·10⁹),\n  round(Im·10⁹)\n)",
            ha='center', va='center', fontsize=8, color=COLOR_DARK)
    ax.text(6.5, 2.4, "Duplicates\nDropped (seen)\nUnique Kept",
            ha='center', va='center', fontsize=8.5, fontweight='bold', color=COLOR_CORAL)
    ax.text(6.5, 1.5, "Keep Top-K\n(Beam Width)", ha='center', va='center',
            fontsize=9, fontweight='bold', color=COLOR_BLUE)

    # Depth 2 level
    d2_y = [4.2, 3.0, 1.8]
    for i, y in enumerate(d2_y):
        c = patches.Circle((8.6, y), 0.4, facecolor="white", edgecolor=COLOR_TEAL, lw=1.8)
        ax.add_patch(c)
        ax.text(8.6, y, f"K_{i+1}", ha='center', va='center', fontsize=9, fontweight='bold', color=COLOR_TEAL)
        ax.annotate("", xy=(8.2, y), xytext=(7.6, 3.0),
                    arrowprops=dict(arrowstyle="-|>", color=COLOR_TEAL, lw=1.5))

    # Goal / Match Node
    goal = patches.FancyBboxPatch((10.0, 2.5), 1.8, 1.2, boxstyle="round,pad=0.1",
                                  facecolor=COLOR_TEAL, edgecolor=COLOR_NAVY, lw=2)
    ax.add_patch(goal)
    ax.text(10.9, 3.3, "SOLUTION FOUND", ha='center', va='center',
            fontsize=9.5, fontweight='bold', color='white')
    ax.text(10.9, 2.8, r"$s(U, V) \geq 1 - \epsilon$" + "\nExact match!", ha='center', va='center',
            fontsize=8.5, color='#F0FDFA')
    ax.annotate("", xy=(10.0, 3.0), xytext=(9.0, 3.0),
                arrowprops=dict(arrowstyle="-|>", color=COLOR_TEAL, lw=2.5))

    ax.set_xlim(0.5, 12.2)
    ax.set_ylim(0.5, 5.5)
    plt.tight_layout()
    path = os.path.join(FIG_DIR, "slide5_beam_search.png")
    plt.savefig(path, facecolor=fig.get_facecolor(), bbox_inches='tight')
    plt.close()
    return path


def fig6_target_pathways():
    fig, ax = plt.subplots(figsize=(12, 6.2), dpi=250)
    ax.set_facecolor(COLOR_BG)
    fig.patch.set_facecolor(COLOR_BG)
    ax.axis('off')

    # Central Target Unitary
    target = patches.FancyBboxPatch((8.5, 1.5), 3.0, 3.2, boxstyle="round,pad=0.15",
                                    facecolor=COLOR_BLUE, edgecolor=COLOR_NAVY, lw=2)
    ax.add_patch(target)
    ax.text(10.0, 4.2, "UNIFIED TARGET", ha='center', va='center',
            fontsize=13, fontweight='bold', color='white')
    ax.text(10.0, 3.6, "Unitary Matrix U", ha='center', va='center',
            fontsize=11, fontweight='bold', color='#BFDBFE')
    ax.text(10.0, 2.8, r"Dimension: $2^n \times 2^n$" + "\n" + r"$U^\dagger U = I$" + "\n(Validated within 10⁻⁸)",
            ha='center', va='center', fontsize=9.5, color='white')
    ax.text(10.0, 1.9, "Ready for Beam Search", ha='center', va='center',
            fontsize=9, style='italic', color='#E0E7FF')

    # Pathway 1: Direct Unitary
    p1 = patches.FancyBboxPatch((0.8, 4.0), 5.5, 1.4, boxstyle="round,pad=0.1",
                                facecolor="white", edgecolor=COLOR_TEAL, lw=1.8)
    ax.add_patch(p1)
    ax.text(1.1, 5.0, "Pathway 1: Direct Unitary Matrix", fontsize=11, fontweight='bold', color=COLOR_TEAL)
    ax.text(1.1, 4.5, "• Built-in presets: SWAP, CNOT, CZ, CCX (Toffoli), CSWAP (Fredkin), H, S, T\n• Inline JSON: '[[\"sqrt2/2\",\"sqrt2/2\"],[\"sqrt2/2\",\"-sqrt2/2\"]]'\n• Files: .npy or CSV text matrices", fontsize=8.5, color=COLOR_DARK)
    ax.annotate("", xy=(8.4, 3.5), xytext=(6.3, 4.7),
                arrowprops=dict(arrowstyle="-|>", color=COLOR_TEAL, lw=2))

    # Pathway 2: Boolean Formulas
    p2 = patches.FancyBboxPatch((0.8, 2.4), 5.5, 1.4, boxstyle="round,pad=0.1",
                                facecolor="white", edgecolor=COLOR_PURPLE, lw=1.8)
    ax.add_patch(p2)
    ax.text(1.1, 3.4, "Pathway 2: Boolean Logic Expressions", fontsize=11, fontweight='bold', color=COLOR_PURPLE)
    ax.text(1.1, 2.9, "• Syntax: '(x0 and x1) ^ x2' or 'a & b | ~c'\n• AST safe inspection with automatic variable ordering (x0 → wire 0)\n• Oracle construction: Bit-flip (n+1 wires) or Phase (n wires)", fontsize=8.5, color=COLOR_DARK)
    ax.annotate("", xy=(8.4, 3.1), xytext=(6.3, 3.1),
                arrowprops=dict(arrowstyle="-|>", color=COLOR_PURPLE, lw=2))

    # Pathway 3: Truth Tables
    p3 = patches.FancyBboxPatch((0.8, 0.8), 5.5, 1.4, boxstyle="round,pad=0.1",
                                facecolor="white", edgecolor=COLOR_CORAL, lw=1.8)
    ax.add_patch(p3)
    ax.text(1.1, 1.8, "Pathway 3: Truth Tables", fontsize=11, fontweight='bold', color=COLOR_CORAL)
    ax.text(1.1, 1.3, "• Bitstrings: '0110' (XOR) or delimited '0, 1, 1, 0'\n• Input-output mappings: {'00':0, '01':1, '10':1, '11':0}\n• Reversible permutations: '0->1, 1->0, 2->3, 3->2'", fontsize=8.5, color=COLOR_DARK)
    ax.annotate("", xy=(8.4, 2.7), xytext=(6.3, 1.5),
                arrowprops=dict(arrowstyle="-|>", color=COLOR_CORAL, lw=2))

    ax.set_xlim(0, 12)
    ax.set_ylim(0.2, 5.8)
    plt.tight_layout()
    path = os.path.join(FIG_DIR, "slide6_pathways.png")
    plt.savefig(path, facecolor=fig.get_facecolor(), bbox_inches='tight')
    plt.close()
    return path


def fig7_oracle_architectures():
    fig, ax = plt.subplots(figsize=(12, 6.2), dpi=250)
    ax.set_facecolor(COLOR_BG)
    fig.patch.set_facecolor(COLOR_BG)
    ax.axis('off')

    modes = [
        ("1. Bit-Flip Oracle (--oracle-mode bitflip)",
         r"$|x, y\rangle \mapsto |x, y \oplus f(x)\rangle$",
         "Requires n + 1 qubits (inputs x on q0..qn-1, target y on qn)",
         COLOR_BLUE, 0.8, "bitflip"),
        ("2. Phase Oracle (--oracle-mode phase)",
         r"$|x\rangle \mapsto (-1)^{f(x)} |x\rangle$",
         "Requires exactly n qubits (0 ancilla overhead; diagonal matrix)",
         COLOR_PURPLE, 4.4, "phase"),
        ("3. Permutation Oracle (--oracle-mode permutation)",
         r"$|x\rangle \mapsto |f(x)\rangle$",
         "Requires n qubits (reversible bijection permutation matrix)",
         COLOR_TEAL, 8.0, "perm"),
    ]

    for title, formula, note, col, x, kind in modes:
        box = patches.FancyBboxPatch((x, 0.8), 3.4, 4.6, boxstyle="round,pad=0.15",
                                     facecolor="white", edgecolor=col, lw=2)
        ax.add_patch(box)
        ax.text(x + 1.7, 5.0, title, ha='center', va='center',
                fontsize=10.5, fontweight='bold', color=col)
        ax.text(x + 1.7, 4.5, formula, ha='center', va='center',
                fontsize=11.5, fontweight='bold', color=COLOR_NAVY)
        ax.text(x + 1.7, 4.0, note, ha='center', va='center',
                fontsize=8, color=COLOR_GRAY, multialignment='center')

        # Draw mini-circuit schematic inside each box
        # Wires
        for w in range(3):
            yw = 3.2 - w * 0.8
            ax.plot([x + 0.4, x + 3.0], [yw, yw], color=COLOR_LIGHT_GRAY, lw=2)
            lbl = f"x{w}" if w < 2 else ("y (ancilla)" if kind == "bitflip" else f"x{w}")
            ax.text(x + 0.35, yw, lbl, ha='right', va='center', fontsize=8, color=COLOR_NAVY)

        if kind == "bitflip":
            # Multi-control or gate box
            gate = patches.Rectangle((x + 1.2, 1.4), 1.0, 2.0, facecolor=COLOR_LIGHT_BLUE,
                                     edgecolor=COLOR_BLUE, lw=1.5)
            ax.add_patch(gate)
            ax.text(x + 1.7, 2.4, "U_f", ha='center', va='center',
                    fontsize=12, fontweight='bold', color=COLOR_BLUE)
            ax.text(x + 3.05, 1.6, r"$|y \oplus f(x)\rangle$", ha='left', va='center', fontsize=8, color=COLOR_BLUE)
        elif kind == "phase":
            gate = patches.Rectangle((x + 1.2, 2.2), 1.0, 1.2, facecolor=COLOR_LIGHT_PURPLE,
                                     edgecolor=COLOR_PURPLE, lw=1.5)
            ax.add_patch(gate)
            ax.text(x + 1.7, 2.8, r"$(-1)^f$", ha='center', va='center',
                    fontsize=11, fontweight='bold', color=COLOR_PURPLE)
            ax.text(x + 1.7, 1.4, "[No ancilla needed]", ha='center', va='center',
                    fontsize=8.5, style='italic', color=COLOR_GRAY)
        elif kind == "perm":
            gate = patches.Rectangle((x + 1.2, 1.4), 1.0, 2.0, facecolor=COLOR_LIGHT_TEAL,
                                     edgecolor=COLOR_TEAL, lw=1.5)
            ax.add_patch(gate)
            ax.text(x + 1.7, 2.4, "P_f", ha='center', va='center',
                    fontsize=12, fontweight='bold', color=COLOR_TEAL)
            ax.text(x + 3.05, 2.4, r"$|f(x)\rangle$", ha='left', va='center', fontsize=8, color=COLOR_TEAL)

    ax.set_xlim(0, 12.2)
    ax.set_ylim(0.4, 5.6)
    plt.tight_layout()
    path = os.path.join(FIG_DIR, "slide7_oracles.png")
    plt.savefig(path, facecolor=fig.get_facecolor(), bbox_inches='tight')
    plt.close()
    return path


def fig8_boolean_synthesis_results():
    fig, ax = plt.subplots(figsize=(12, 6.2), dpi=250)
    ax.set_facecolor(COLOR_BG)
    fig.patch.set_facecolor(COLOR_BG)
    ax.axis('off')

    cases = [
        ("Case A: XOR (Bit-Flip)", r"$f(x_0, x_1) = x_0 \oplus x_1$", "Allowed: CNOT | Target: 3 Qubits",
         "2 CNOT gates", 0.6, COLOR_BLUE),
        ("Case B: AND (Phase Oracle)", r"$f(x_0, x_1) = x_0 \wedge x_1$", "Allowed: Clifford+T | Target: 2 Qubits",
         "1 CZ gate (0 ancilla)", 4.5, COLOR_PURPLE),
        ("Case C: AND (Reversible CCX)", r"$f(x_0, x_1) = x_0 \wedge x_1$", "Allowed: Reversible | Target: 3 Qubits",
         "1 Toffoli (CCX) gate", 8.4, COLOR_TEAL),
    ]

    for title, formula, config, res, x, col in cases:
        box = patches.FancyBboxPatch((x, 0.8), 3.3, 4.6, boxstyle="round,pad=0.15",
                                     facecolor="white", edgecolor=col, lw=2)
        ax.add_patch(box)
        ax.text(x + 1.65, 5.0, title, ha='center', va='center', fontsize=11, fontweight='bold', color=col)
        ax.text(x + 1.65, 4.5, formula, ha='center', va='center', fontsize=11, fontweight='bold', color=COLOR_NAVY)
        ax.text(x + 1.65, 4.1, config, ha='center', va='center', fontsize=8, color=COLOR_GRAY)

        # Synthesized Outcome Badge
        badge = patches.FancyBboxPatch((x + 0.3, 3.4), 2.7, 0.45, boxstyle="round,pad=0.08",
                                       facecolor=col, edgecolor="none")
        ax.add_patch(badge)
        ax.text(x + 1.65, 3.62, f"Synthesized: {res}", ha='center', va='center',
                fontsize=9, fontweight='bold', color="white")

        # Quantum Circuit Drawing inside card
        if x < 2.0:  # Case A: XOR -> CNOT[0,2], CNOT[1,2]
            # 3 wires
            for w in range(3):
                yw = 2.7 - w * 0.7
                ax.plot([x + 0.4, x + 2.9], [yw, yw], color=COLOR_GRAY, lw=1.8)
                ax.text(x + 0.3, yw, f"q{w}", ha='right', va='center', fontsize=8, color=COLOR_NAVY)
            # CNOT 0->2
            ax.plot([x + 1.1, x + 1.1], [1.3, 2.7], color=col, lw=1.8)
            ax.plot(x + 1.1, 2.7, 'o', color=col, ms=6)
            circle = plt.Circle((x + 1.1, 1.3), 0.12, facecolor="white", edgecolor=col, lw=1.5, zorder=5)
            ax.add_patch(circle)
            # CNOT 1->2
            ax.plot([x + 2.1, x + 2.1], [1.3, 2.0], color=col, lw=1.8)
            ax.plot(x + 2.1, 2.0, 'o', color=col, ms=6)
            circle2 = plt.Circle((x + 2.1, 1.3), 0.12, facecolor="white", edgecolor=col, lw=1.5, zorder=5)
            ax.add_patch(circle2)
        elif x < 6.0:  # Case B: AND -> CZ[0,1]
            for w in range(2):
                yw = 2.4 - w * 0.9
                ax.plot([x + 0.4, x + 2.9], [yw, yw], color=COLOR_GRAY, lw=1.8)
                ax.text(x + 0.3, yw, f"q{w}", ha='right', va='center', fontsize=8, color=COLOR_NAVY)
            ax.plot([x + 1.65, x + 1.65], [1.5, 2.4], color=col, lw=2)
            ax.plot(x + 1.65, 2.4, 'o', color=col, ms=7)
            ax.plot(x + 1.65, 1.5, 'o', color=col, ms=7)
            ax.text(x + 1.65, 1.0, "CZ[0,1] Phase Flip", ha='center', fontsize=8.5, color=col, fontweight='bold')
        else:  # Case C: Toffoli (CCX[0,1,2])
            for w in range(3):
                yw = 2.7 - w * 0.7
                ax.plot([x + 0.4, x + 2.9], [yw, yw], color=COLOR_GRAY, lw=1.8)
                ax.text(x + 0.3, yw, f"q{w}", ha='right', va='center', fontsize=8, color=COLOR_NAVY)
            ax.plot([x + 1.65, x + 1.65], [1.3, 2.7], color=col, lw=2)
            ax.plot(x + 1.65, 2.7, 'o', color=col, ms=6)
            ax.plot(x + 1.65, 2.0, 'o', color=col, ms=6)
            circle = plt.Circle((x + 1.65, 1.3), 0.12, facecolor="white", edgecolor=col, lw=1.5, zorder=5)
            ax.add_patch(circle)

    ax.set_xlim(0, 12.3)
    ax.set_ylim(0.4, 5.6)
    plt.tight_layout()
    path = os.path.join(FIG_DIR, "slide8_bool_cases.png")
    plt.savefig(path, facecolor=fig.get_facecolor(), bbox_inches='tight')
    plt.close()
    return path


def fig9_optimizer_pipeline():
    fig, ax = plt.subplots(figsize=(12, 6.2), dpi=250)
    ax.set_facecolor(COLOR_BG)
    fig.patch.set_facecolor(COLOR_BG)
    ax.axis('off')

    # Flowchart Blocks
    nodes = [
        ("User Input Circuit", "OpenQASM or native gate list", 1.2, COLOR_BLUE),
        ("Pass 1: Commutation Peephole", "Disjoint commutations, inverse\ncancellations, and gate merging", 3.8, COLOR_PURPLE),
        ("Pass 2: Global Resynthesis", "Beam search on total unitary\nfor short circuits (depth < L)", 6.4, COLOR_TEAL),
        ("Pass 3: Sliding Window", r"Block resynthesis across" + "\n" + r"sub-windows $w \in [2, W]$", 9.0, COLOR_CORAL),
        ("Verified Minimal Circuit", r"Fidelity $s \geq 1 - \epsilon$ verified" + "\nOpenQASM & ASCII exported", 11.2, COLOR_NAVY),
    ]

    for title, desc, x, col in nodes:
        box = patches.FancyBboxPatch((x - 1.0, 1.8), 2.0, 2.4, boxstyle="round,pad=0.1",
                                     facecolor="white", edgecolor=col, lw=2)
        ax.add_patch(box)
        hdr = patches.FancyBboxPatch((x - 1.0, 3.6), 2.0, 0.6, boxstyle="round,pad=0.05",
                                     facecolor=col, edgecolor="none")
        ax.add_patch(hdr)
        ax.text(x, 3.9, title, ha='center', va='center', fontsize=9, fontweight='bold', color='white')
        ax.text(x, 2.7, desc, ha='center', va='center', fontsize=8, color=COLOR_DARK)

        if x < 11.0:
            ax.annotate("", xy=(x + 1.15, 3.0), xytext=(x + 0.95, 3.0),
                        arrowprops=dict(arrowstyle="-|>", color=COLOR_NAVY, lw=2.2))

    # Feedback Loop arrow from Sliding Window back to Peephole
    ax.annotate("Local reduction triggers\npeephole re-pass", xy=(3.8, 1.7), xytext=(9.0, 1.0),
                ha='center', fontsize=8.5, fontweight='bold', color=COLOR_CORAL,
                arrowprops=dict(arrowstyle="-|>", color=COLOR_CORAL, lw=1.8,
                                connectionstyle="arc3,rad=0.25"))

    ax.set_xlim(0, 12.5)
    ax.set_ylim(0.5, 5.2)
    plt.tight_layout()
    path = os.path.join(FIG_DIR, "slide9_optimizer_pipeline.png")
    plt.savefig(path, facecolor=fig.get_facecolor(), bbox_inches='tight')
    plt.close()
    return path


def fig10_peephole_rules():
    fig, ax = plt.subplots(figsize=(12, 6.2), dpi=250)
    ax.set_facecolor(COLOR_BG)
    fig.patch.set_facecolor(COLOR_BG)
    ax.axis('off')

    rules = [
        ("Rule 1: Commutation Past Disjoint Wires",
         "If gates act on disjoint wires, [A, B] = 0. They commute across intermediate steps.",
         COLOR_BLUE, 4.0),
        ("Rule 2: Self-Inverse Cancellation",
         "Adjacent inverse pairs cancel directly to identity: H·H = I, CNOT·CNOT = I.",
         COLOR_CORAL, 2.4),
        ("Rule 3: Gate Merging into Allowed Basis",
         "Sequential rotations merge into single gates: T·T → S, S·S → Z.",
         COLOR_TEAL, 0.8),
    ]

    for title, desc, col, y in rules:
        box = patches.FancyBboxPatch((0.8, y), 10.4, 1.35, boxstyle="round,pad=0.1",
                                     facecolor="white", edgecolor=col, lw=2)
        ax.add_patch(box)
        ax.text(1.2, y + 1.0, title, fontsize=11, fontweight='bold', color=col)
        ax.text(1.2, y + 0.65, desc, fontsize=8.5, color=COLOR_DARK)

        # Mini visual transformation diagram on the right side of card
        if y > 3.0:  # Commutation
            ax.text(8.5, y + 0.8, "CNOT[0,1] · H[2]   =   H[2] · CNOT[0,1]",
                    fontsize=9, fontweight='bold', color=COLOR_NAVY)
            ax.text(8.5, y + 0.4, "Commute freely to unlock cancellations",
                    fontsize=8, style='italic', color=COLOR_BLUE)
        elif y > 2.0:  # Cancellation
            ax.text(8.5, y + 0.8, r"H[0]  ──  H[0]   $\Longrightarrow$   [Identity Wire]",
                    fontsize=9, fontweight='bold', color=COLOR_CORAL)
            ax.text(8.5, y + 0.4, "2 gates eliminated (-100%)",
                    fontsize=8, style='italic', color=COLOR_CORAL)
        else:  # Merging
            ax.text(8.5, y + 0.8, r"T[0]  ──  T[0]   $\Longrightarrow$   S[0]",
                    fontsize=9, fontweight='bold', color=COLOR_TEAL)
            ax.text(8.5, y + 0.4, "2 gates collapsed into 1 gate (-50%)",
                    fontsize=8, style='italic', color=COLOR_TEAL)

    ax.set_xlim(0, 12)
    ax.set_ylim(0.5, 5.8)
    plt.tight_layout()
    path = os.path.join(FIG_DIR, "slide10_peephole_rules.png")
    plt.savefig(path, facecolor=fig.get_facecolor(), bbox_inches='tight')
    plt.close()
    return path


def fig11_case_study_swap():
    fig, ax = plt.subplots(figsize=(12, 6.2), dpi=250)
    ax.set_facecolor(COLOR_BG)
    fig.patch.set_facecolor(COLOR_BG)
    ax.axis('off')

    # Top: Original 7-Gate Circuit
    box_top = patches.FancyBboxPatch((0.8, 3.2), 10.4, 2.3, boxstyle="round,pad=0.15",
                                     facecolor="white", edgecolor=COLOR_CORAL, lw=2)
    ax.add_patch(box_top)
    ax.text(1.2, 5.1, "Original Circuit: 7 Gates (CNOT + 4 Hadamards)",
            fontsize=12, fontweight='bold', color=COLOR_CORAL)
    ax.text(9.5, 5.1, "Gate Count: 7", fontsize=11, fontweight='bold', color=COLOR_CORAL)

    # 7-gate wire diagram
    for q, y in enumerate([4.3, 3.6]):
        ax.plot([1.5, 10.5], [y, y], color=COLOR_GRAY, lw=2)
        ax.text(1.3, y, f"q{q}", ha='right', va='center', fontsize=9, fontweight='bold', color=COLOR_NAVY)

    # CNOT 1
    ax.plot([2.5, 2.5], [3.6, 4.3], color=COLOR_CORAL, lw=2)
    ax.plot(2.5, 4.3, 'o', color=COLOR_CORAL, ms=7)
    c1 = plt.Circle((2.5, 3.6), 0.14, facecolor="white", edgecolor=COLOR_CORAL, lw=1.8, zorder=5)
    ax.add_patch(c1)
    # H gates on q0 and q1
    for y in [4.3, 3.6]:
        h = patches.Rectangle((3.6, y - 0.2), 0.6, 0.4, facecolor=COLOR_LIGHT_CORAL, edgecolor=COLOR_CORAL, lw=1.2)
        ax.add_patch(h)
        ax.text(3.9, y, "H", ha='center', va='center', fontsize=9, fontweight='bold', color=COLOR_CORAL)
    # CNOT 2
    ax.plot([5.5, 5.5], [3.6, 4.3], color=COLOR_CORAL, lw=2)
    ax.plot(5.5, 4.3, 'o', color=COLOR_CORAL, ms=7)
    c2 = plt.Circle((5.5, 3.6), 0.14, facecolor="white", edgecolor=COLOR_CORAL, lw=1.8, zorder=5)
    ax.add_patch(c2)
    # H gates on q0 and q1
    for y in [4.3, 3.6]:
        h = patches.Rectangle((6.8, y - 0.2), 0.6, 0.4, facecolor=COLOR_LIGHT_CORAL, edgecolor=COLOR_CORAL, lw=1.2)
        ax.add_patch(h)
        ax.text(7.1, y, "H", ha='center', va='center', fontsize=9, fontweight='bold', color=COLOR_CORAL)
    # CNOT 3
    ax.plot([8.8, 8.8], [3.6, 4.3], color=COLOR_CORAL, lw=2)
    ax.plot(8.8, 4.3, 'o', color=COLOR_CORAL, ms=7)
    c3 = plt.Circle((8.8, 3.6), 0.14, facecolor="white", edgecolor=COLOR_CORAL, lw=1.8, zorder=5)
    ax.add_patch(c3)

    # Downward Transformation Arrow
    ax.annotate("Q-Synth Global Resynthesis (Allowed: CNOT only)\nFidelity: s = 1.0000000000 | Max Error: 0.00",
                xy=(6.0, 2.7), xytext=(6.0, 3.1),
                ha='center', va='center', fontsize=10, fontweight='bold', color=COLOR_NAVY,
                arrowprops=dict(arrowstyle="-|>", color=COLOR_BLUE, lw=3))

    # Bottom: Optimized 3-CNOT Circuit
    box_bot = patches.FancyBboxPatch((0.8, 0.5), 10.4, 1.9, boxstyle="round,pad=0.15",
                                     facecolor="white", edgecolor=COLOR_TEAL, lw=2)
    ax.add_patch(box_bot)
    ax.text(1.2, 2.1, "Optimized Circuit: Minimal 3 CNOT SWAP",
            fontsize=12, fontweight='bold', color=COLOR_TEAL)
    ax.text(9.5, 2.1, "Gate Count: 3 (-57.1%)", fontsize=11, fontweight='bold', color=COLOR_TEAL)

    for q, y in enumerate([1.5, 0.9]):
        ax.plot([1.5, 10.5], [y, y], color=COLOR_GRAY, lw=2)
        ax.text(1.3, y, f"q{q}", ha='right', va='center', fontsize=9, fontweight='bold', color=COLOR_NAVY)

    # 3 CNOTs
    cnots = [(3.2, 1.5, 0.9), (6.0, 0.9, 1.5), (8.8, 1.5, 0.9)]
    for xc, ctrl_y, tgt_y in cnots:
        ax.plot([xc, xc], [0.9, 1.5], color=COLOR_TEAL, lw=2)
        ax.plot(xc, ctrl_y, 'o', color=COLOR_TEAL, ms=7)
        cc = plt.Circle((xc, tgt_y), 0.14, facecolor="white", edgecolor=COLOR_TEAL, lw=1.8, zorder=5)
        ax.add_patch(cc)

    ax.set_xlim(0, 12)
    ax.set_ylim(0.2, 5.8)
    plt.tight_layout()
    path = os.path.join(FIG_DIR, "slide11_swap_case.png")
    plt.savefig(path, facecolor=fig.get_facecolor(), bbox_inches='tight')
    plt.close()
    return path


def fig12_benchmark_summary():
    fig, ax = plt.subplots(figsize=(12, 6.2), dpi=250)
    ax.set_facecolor(COLOR_BG)
    fig.patch.set_facecolor(COLOR_BG)

    cases = [
        "H-CNOT-CNOT-H\nCancellation",
        "Double SWAP\n(6 CNOTs)",
        "Gate Merging\n(T + T → S)",
        "7-Gate SWAP\nResynthesis",
    ]
    orig_gates = [4, 6, 2, 7]
    opt_gates = [0, 0, 1, 3]
    reductions = ["-100%", "-100%", "-50%", "-57.1%"]

    x = np.arange(len(cases))
    width = 0.32

    rects1 = ax.bar(x - width/2, orig_gates, width, label='Original Gate Count',
                    color=COLOR_CORAL, edgecolor=COLOR_NAVY, lw=1.2)
    rects2 = ax.bar(x + width/2, opt_gates, width, label='Q-Synth Optimized Count',
                    color=COLOR_TEAL, edgecolor=COLOR_NAVY, lw=1.2)

    # Value labels on bars
    for rect in rects1:
        h = rect.get_height()
        ax.annotate(f'{h}',
                    xy=(rect.get_x() + rect.get_width() / 2, h),
                    xytext=(0, 4), textcoords="offset points",
                    ha='center', va='bottom', fontsize=11, fontweight='bold', color=COLOR_CORAL)

    for i, rect in enumerate(rects2):
        h = rect.get_height()
        ax.annotate(f'{h}',
                    xy=(rect.get_x() + rect.get_width() / 2, h),
                    xytext=(0, 4), textcoords="offset points",
                    ha='center', va='bottom', fontsize=11, fontweight='bold', color=COLOR_TEAL)
        # Reduction badge above
        ax.annotate(reductions[i],
                    xy=(x[i], max(orig_gates[i], opt_gates[i]) + 0.9),
                    ha='center', va='bottom', fontsize=10.5, fontweight='bold',
                    color=COLOR_BLUE,
                    bbox=dict(boxstyle="round,pad=0.2", facecolor=COLOR_LIGHT_BLUE, edgecolor=COLOR_BLUE, lw=1))

    ax.set_ylabel('Gate Count', fontsize=12, fontweight='bold', color=COLOR_NAVY)
    ax.set_title(r'Q-Synth Circuit Optimization Benchmarks (All Verified $s = 1.0000000000$)',
                 fontsize=13, fontweight='bold', color=COLOR_NAVY, pad=15)
    ax.set_xticks(x)
    ax.set_xticklabels(cases, fontsize=10.5, fontweight='bold', color=COLOR_NAVY)
    ax.set_ylim(0, 9.2)
    ax.grid(axis='y', linestyle='--', alpha=0.5)
    ax.legend(fontsize=10.5, loc='upper right', framealpha=0.95)

    plt.tight_layout()
    path = os.path.join(FIG_DIR, "slide12_benchmarks.png")
    plt.savefig(path, facecolor=fig.get_facecolor(), bbox_inches='tight')
    plt.close()
    return path


def build_powerpoint():
    prs = Presentation()
    # Set 16:9 widescreen dimensions
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    blank_layout = prs.slide_layouts[6]  # completely blank slide

    slides_data = [
        ("Q-Synth: Quantum Circuit Synthesizer & Optimizer",
         "A modular framework for synthesizing unitaries and Boolean functions into minimal quantum circuits",
         fig1_title_overview()),

        ("The Quantum Compilation Challenge",
         "Bridging high-level mathematical algorithms and noise-constrained physical quantum hardware",
         fig2_compilation_challenge()),

        ("End-to-End System Pipeline Architecture",
         "Four-stage modular flow from specification and move enumeration to verification and export",
         fig3_system_architecture()),

        ("Move Enumeration & Kronecker Matrix Embedding",
         "Kronecker bit-subword projection across all ordered wire placements P(n, k)",
         fig4_move_enumeration_embedding()),

        ("Beam Search with Quantized Hash Deduplication",
         "Breadth-first exploration with 10⁹ complex-grid deduplication to prevent exponential explosion",
         fig5_beam_search_dedup()),

        ("Unified Target Specification Spectrum",
         "Three seamless input pathways: direct unitary matrices, Boolean logic, and truth tables",
         fig6_target_pathways()),

        ("Quantum Oracle Compilation Paradigms",
         "Bit-flip oracles (n+1 wires), phase oracles (0 ancilla overhead), and reversible permutations",
         fig7_oracle_architectures()),

        ("Synthesized Boolean Oracles in Action",
         "Empirical synthesis results: XOR into 2 CNOTs, AND into CZ phase gate and Toffoli CCX",
         fig8_boolean_synthesis_results()),

        ("Circuit Optimization: Multi-Pass Architecture",
         "Cascading passes combining algebraic commutation peepholes with global and sliding-window resynthesis",
         fig9_optimizer_pipeline()),

        ("Commutation-Aware Peephole Rewriting Rules",
         "Disjoint wire commutations, self-inverse cancellations, and single-gate collapsing",
         fig10_peephole_rules()),

        ("Case Study: Resynthesizing 7-Gate SWAP to 3 CNOTs",
         "Achieving 57.1% gate count reduction using strictly permitted CNOT basis gates",
         fig11_case_study_swap()),

        ("Empirical Benchmark Results & Gate Reduction",
         "Exact numerical verification across synthesis cases with up to 100% gate reduction",
         fig12_benchmark_summary()),
    ]

    for title, subtitle, img_path in slides_data:
        slide = prs.slides.add_slide(blank_layout)

        # Header Title text box
        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(0.9))
        tf = title_box.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        p_title = tf.paragraphs[0]
        p_title.text = title
        p_title.font.size = Pt(22)
        p_title.font.bold = True
        p_title.font.color.rgb = RGBColor(15, 23, 42)  # Navy

        p_sub = tf.add_paragraph()
        p_sub.text = subtitle
        p_sub.font.size = Pt(11)
        p_sub.font.color.rgb = RGBColor(100, 116, 139)  # Slate Gray

        # Insert Diagram Image centered
        img_left = Inches(0.8)
        img_top = Inches(1.35)
        img_width = Inches(11.733)
        slide.shapes.add_picture(img_path, img_left, img_top, width=img_width)

    output_pptx = os.path.join(OUTPUT_DIR, "Q-Synth_Presentation.pptx")
    prs.save(output_pptx)
    print(f"Successfully generated PowerPoint presentation with {len(slides_data)} slides: {output_pptx}")
    return output_pptx


if __name__ == "__main__":
    build_powerpoint()
