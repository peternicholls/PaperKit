#!/usr/bin/env python3
from pathlib import Path
try:
    import numpy as np
    import matplotlib.pyplot as plt
    from matplotlib.patches import Ellipse, Circle, FancyArrowPatch, Rectangle
except ModuleNotFoundError as e:
    pkg = e.name
    print(f"Missing dependency '{pkg}'. Install with:\n  pip install {pkg}\nor\n  pip install -r requirements.txt")
    raise

import matplotlib as mpl
mpl.rcParams.update({
    "font.family": "serif",
    "font.size": 11,
    "axes.titlesize": 12,
    "axes.labelsize": 11,
    "pdf.fonttype": 42,  # embed TrueType
    "ps.fonttype": 42,
})

OUT_DIR = Path("figures")  # run from your latex/ directory
OUT_DIR.mkdir(parents=True, exist_ok=True)

def save_pdf(fig, name: str):
    path = OUT_DIR / name
    fig.savefig(path, format="pdf", bbox_inches="tight")
    plt.close(fig)
    print("Wrote", path)

def fig_metric_ellipses():
    fig, ax = plt.subplots(figsize=(7.5, 4.8))

    # Coordinate plane for a-b (schematic)
    ax.axhline(0, linewidth=1)
    ax.axvline(0, linewidth=1)
    ax.set_aspect("equal", adjustable="box")
    ax.set_xlim(-1.15, 1.15)
    ax.set_ylim(-0.85, 0.85)
    ax.set_xlabel("a axis (green–red)")
    ax.set_ylabel("b axis (blue–yellow)")
    ax.set_title("Schematic: local discrimination ellipses vary by location and orientation")

    # Place ellipses around the plane and orient their major axis toward the origin
    rng = np.random.default_rng(4)
    points = [
        (-0.9,  0.55), (-0.6, -0.4), (-0.2,  0.65), (0.2, -0.6),
        (0.55, 0.45), (0.9, -0.15), (-0.85, -0.05), (0.1, 0.2)
    ]

    for (x, y) in points:
        # angle pointing from point to origin
        ang = np.degrees(np.arctan2(-y, -x))
        # sizes: make ellipses slightly bigger away from origin
        r = np.hypot(x, y)
        w = 0.25 + 0.15 * r
        h = 0.10 + 0.07 * r
        e = Ellipse((x, y), width=w, height=h, angle=ang, fill=False, linewidth=1.5)
        ax.add_patch(e)

    # A few arrows to show radial tendency
    for (x, y) in [(-0.9, 0.55), (0.55, 0.45), (0.2, -0.6)]:
        arr = FancyArrowPatch((x, y), (0, 0), arrowstyle="->", mutation_scale=12, linewidth=1)
        ax.add_patch(arr)

    ax.text(0.02, 0.02, "achromatic axis", transform=ax.transAxes, fontsize=10)
    save_pdf(fig, "hong-metric-ellipses.pdf")

def fig_hue_720():
    fig, ax = plt.subplots(figsize=(6.8, 4.6))
    ax.set_aspect("equal", adjustable="box")
    ax.axis("off")
    ax.set_title("Conceptual schematic: 720° intuition as effective doubling", pad=16)

    # Two concentric circles with labels
    c1 = Circle((0, 0), 1.0, fill=False, linewidth=2)
    c2 = Circle((0, 0), 1.35, fill=False, linewidth=2)
    ax.add_patch(c1)
    ax.add_patch(c2)

    # Mark a start point and a return point conceptually
    ax.plot([1.0], [0.0], marker="o")
    ax.text(1.05, 0.0, "start", va="center")

    # Arc style arrows (schematic)
    arc1 = FancyArrowPatch((1.0, 0.0), (0.98, 0.05), connectionstyle="arc3,rad=0.35",
                           arrowstyle="->", mutation_scale=14, linewidth=1.5)
    arc2 = FancyArrowPatch((1.35, 0.0), (1.33, 0.06), connectionstyle="arc3,rad=0.35",
                           arrowstyle="->", mutation_scale=14, linewidth=1.5)
    ax.add_patch(arc1)
    ax.add_patch(arc2)

    ax.text(0, -1.15, r"Euclidean reference: $2\pi$ (360°)", ha="center", fontsize=11)
    ax.text(0, -1.55, r"H2SI ratio near $4\pi$ (720°) in angular terms", ha="center", fontsize=11)

    ax.text(0, 1.05, "360°", ha="center", fontsize=11)
    ax.text(0, 1.45, "720°", ha="center", fontsize=11)

    ax.set_xlim(-1.9, 1.9)
    ax.set_ylim(-1.9, 1.9)
    save_pdf(fig, "hue-720-schematic.pdf")

def fig_temporal_weights():
    """
    Clean, refactored figure: Channel weighting for temporal smoothness.
    
    Layout:
      - Top row: Three gradient swatches showing lightness, chroma, hue changes
      - Bottom: Bar chart with temporal sensitivity weights and distinct colors per channel
    
    This version prioritizes clarity, clean code structure, professional appearance,
    and perceptual consistency with publication standards.
    """
    import matplotlib.colors as mcolors

    fig = plt.figure(figsize=(11, 5.9), constrained_layout=True)
    gs = fig.add_gridspec(2, 1, height_ratios=[0.44, 1.56], hspace=0.36)
    
    # ======================== TOP ROW: GRADIENT SWATCHES ========================
    ax_swatches = fig.add_subplot(gs[0, 0])
    ax_swatches.axis('off')
    ax_swatches.set_xlim(0, 21)
    ax_swatches.set_ylim(0, 2)
    
    # Define swatches: (x_start, label, caption, gradient_colors)
    swatches_config = [
        (0, 'Lightness change', r'$\Delta L = 0.1 \to$ very noticeable',
         [np.array([c, c, c]) for c in np.linspace(0.2, 0.95, 100)]),
        (7, 'Chroma change', r'$\Delta C = 0.1 \to$ subtle',
         [mcolors.hsv_to_rgb((0.58, s, 0.85)) for s in np.linspace(0.05, 0.95, 100)]),
        (14, 'Hue change', r'$\Delta H = 10° \to$ moderate',
         [mcolors.hsv_to_rgb((0.05 + dh, 0.85, 0.95)) for dh in np.linspace(-0.03, 0.03, 100)]),
    ]
    
    for x_start, label, caption, colors in swatches_config:
        # Draw gradient bar (0.5 height)
        for i, color in enumerate(colors):
            rect = Rectangle((x_start + i*0.06, 0.5), 0.06, 0.8, 
                            facecolor=color, edgecolor='none')
            ax_swatches.add_patch(rect)
        
        # Label above
        ax_swatches.text(x_start + 3, 1.5, label, fontsize=11, ha='center', fontweight='bold')
        
        # Caption below
        ax_swatches.text(x_start + 3, 0.15, caption, fontsize=9, ha='center', style='italic')
        
        # Arrow through middle
        arr = FancyArrowPatch((x_start + 0.3, 0.9), (x_start + 5.7, 0.9), 
                             arrowstyle='-|>', mutation_scale=15, linewidth=1.25, color='black')
        ax_swatches.add_patch(arr)
    
    # ======================== BOTTOM: BAR CHART ========================
    ax_bar = fig.add_subplot(gs[1, 0])
    
    # Data
    labels = ['Lightness\n(w_L)', 'Chroma\n(w_C)', 'Hue\n(w_H)']
    values = [10.0, 1.0, 1.75]
    # Distinct colors: red, blue, teal (matching TikZ version)
    bar_colors = ['#e63946', '#4a7ba7', '#40a8a3']
    sources = ['10:1 ratio\n(Sekulovski 2007)', 'Baseline', 'Heuristic\n(needs validation)']
    
    # Plot bars with individual colors
    bars = ax_bar.bar(range(len(labels)), values, color=bar_colors, alpha=0.88, 
                      width=0.52, edgecolor='black', linewidth=0.8)
    
    # Formatting
    ax_bar.set_ylabel('Temporal sensitivity weight', fontsize=11, labelpad=11)
    ax_bar.set_xlabel('')
    ax_bar.set_xticks(range(len(labels)))
    ax_bar.set_xticklabels(labels, fontsize=10)
    ax_bar.set_ylim(0, max(values) * 1.42)
    ax_bar.yaxis.grid(True, linestyle='--', alpha=0.33, linewidth=0.85)
    ax_bar.tick_params(axis='y', labelsize=10)
    ax_bar.spines['top'].set_visible(False)
    ax_bar.spines['right'].set_visible(False)
    
    # Annotations: value inside bar, source above
    for i, (bar, val, src) in enumerate(zip(bars, values, sources)):
        h = bar.get_height()
        # Value label inside bar
        ax_bar.text(bar.get_x() + bar.get_width()/2, h * 0.62, f'{val:.2g}', 
                   ha='center', va='center', fontsize=11, fontweight='bold', color='white')
        # Source label above
        ax_bar.text(bar.get_x() + bar.get_width()/2, h + max(values)*0.045, src, 
                   ha='center', va='bottom', fontsize=9, style='italic')
    
    # Reference line at y=1
    ax_bar.axhline(1.0, color='gray', linestyle='--', linewidth=1.0, alpha=0.55, zorder=0)
    ax_bar.text(len(labels)-0.2, 1.07, 'Baseline=1.0', ha='right', va='bottom', 
               fontsize=9, color='gray', style='italic')
    
    # Overall title
    fig.suptitle('Channel weighting for temporal smoothness', fontsize=13, y=0.99, fontweight='bold')
    
    save_pdf(fig, "temporal-weights-justified.pdf")

def fig_interpolation_comparison():
    """
    Side-by-side comparison of RGB vs OKLab interpolation
    showing why perceptual uniformity matters
    """
    import numpy as np
    import matplotlib.colors as mcolors

    fig, axes = plt.subplots(3, 1, figsize=(9, 6), constrained_layout=True)

    # Define endpoint colors (sRGB, 0..1)
    blue = np.array([0.0, 0.0, 1.0])
    yellow = np.array([1.0, 1.0, 0.0])

    n_steps = 11

    # Helper: sRGB <-> linear RGB
    def srgb_to_linear(c):
        a = 0.055
        return np.where(c <= 0.04045, c / 12.92, ((c + a) / (1 + a)) ** 2.4)

    def linear_to_srgb(c):
        a = 0.055
        # avoid invalid fractional powers for negative inputs by clamping when using the power
        c_safe = np.maximum(c, 0.0)
        return np.where(c <= 0.0031308, 12.92 * c, (1 + a) * (c_safe ** (1 / 2.4)) - a)

    # OKLab conversion (from https://bottosson.github.io/posts/oklab/)
    M1 = np.array([[0.4122214708, 0.5363325363, 0.0514459929],
                   [0.2119034982, 0.6806995451, 0.1073969566],
                   [0.0883024619, 0.2817188376, 0.6299787005]])
    M2 = np.array([[0.2104542553, 0.7936177850, -0.0040720468],
                   [1.9779984951, -2.4285922050, 0.4505937099],
                   [0.0259040371, 0.7827717662, -0.8086757660]])
    M1_inv = np.array([[4.0767416621, -3.3077115913, 0.2309699292],
                       [-1.2684380046, 2.6097574011, -0.3413193965],
                       [-0.0041960863, -0.7034186147, 1.7076147010]])

    def srgb_to_oklab(srgb):
        lin = srgb_to_linear(srgb)
        lms = M1.dot(lin)
        lms_cbrt = np.cbrt(lms)
        L = M2[0].dot(lms_cbrt)
        a = M2[1].dot(lms_cbrt)
        b = M2[2].dot(lms_cbrt)
        return np.vstack([L, a, b]).T

    def oklab_to_srgb(ok):
        L, a, b = ok[..., 0], ok[..., 1], ok[..., 2]
        l_ = L + 0.3963377774 * a + 0.2158037573 * b
        m_ = L - 0.1055613458 * a - 0.0638541728 * b
        s_ = L - 0.0894841775 * a - 1.2914855480 * b
        l = l_ ** 3
        m = m_ ** 3
        s = s_ ** 3
        lin_rgb = M1_inv.dot(np.vstack([l, m, s]))
        srgb = linear_to_srgb(lin_rgb)
        return np.clip(srgb.T, 0, 1)

    # Panel 1: RGB interpolation (linear in sRGB)
    ax1 = axes[0]
    rgb_gradient = np.array([(1 - t) * blue + t * yellow for t in np.linspace(0, 1, n_steps)])
    for i, color in enumerate(rgb_gradient):
        ax1.add_patch(Rectangle((i, 0), 1, 1, facecolor=color, edgecolor='white', linewidth=2))
    ax1.set_xlim(0, n_steps)
    ax1.set_ylim(0, 1)
    ax1.axis('off')
    ax1.text(-0.5, 0.5, 'RGB\nLinear', va='center', ha='right', fontsize=11)

    # Panel 2: OKLab interpolation (linear in OKLab, rendered back to sRGB)
    ax2 = axes[1]
    ok0 = srgb_to_oklab(blue)
    ok1 = srgb_to_oklab(yellow)
    tvals = np.linspace(0, 1, n_steps)
    oklab_gradient = np.array([(1 - t) * ok0 + t * ok1 for t in tvals]).reshape(n_steps, 3)
    # Convert back to sRGB for display
    oklab_rgb = oklab_to_srgb(oklab_gradient)
    for i, color in enumerate(oklab_rgb):
        ax2.add_patch(Rectangle((i, 0), 1, 1, facecolor=color, edgecolor='white', linewidth=2))
    ax2.set_xlim(0, n_steps)
    ax2.set_ylim(0, 1)
    ax2.axis('off')
    ax2.text(-0.5, 0.5, 'OKLab\nLinear', va='center', ha='right', fontsize=11)

    # Panel 3: Perceptual distance plot (Euclidean in the OKLab space is perceptually meaningful)
    ax3 = axes[2]
    # Euclidean distances between adjacent steps in RGB (linear RGB) and OKLab
    rgb_lin = np.array([srgb_to_linear(c) for c in rgb_gradient])
    rgb_distances = np.linalg.norm(np.diff(rgb_lin, axis=0), axis=1)
    oklab_distances = np.linalg.norm(np.diff(oklab_gradient, axis=0), axis=1)

    x = np.arange(len(rgb_distances))
    ax3.plot(x, rgb_distances, 'o-', label='RGB (linear dist)', linewidth=2)
    ax3.plot(x, oklab_distances, 's-', label='OKLab (Euclidean)', linewidth=2)
    ax3.set_xlabel('Step number')
    ax3.set_ylabel('Distance')
    ax3.legend()
    ax3.grid(True, alpha=0.3)
    ax3.set_title('Perceptual distance between adjacent colors', fontsize=10)
    ax3.set_xticks(x)
    ax3.tick_params(axis='both', labelsize=9)
    # Annotate mean distances for quick comparison
    ax3.text(0.98, 0.95, f'Mean RGB = {rgb_distances.mean():.3f}\nMean OKLab = {oklab_distances.mean():.3f}',
             ha='right', va='top', transform=ax3.transAxes, fontsize=9, bbox=dict(facecolor='white', alpha=0.6, edgecolor='none'))

    save_pdf(fig, "interpolation-comparison.pdf")

def main():
    fig_metric_ellipses()
    fig_hue_720()
    fig_temporal_weights()
    fig_interpolation_comparison()
    print("Done. Rebuild LaTeX to pick up the PDFs.")

if __name__ == "__main__":
    main()