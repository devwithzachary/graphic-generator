#!/usr/bin/env python3
"""TrashCanAI video graphics project using the shared graphic_gen library."""

from __future__ import annotations

import sys
import textwrap
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT_DIR))

import graphic_gen as gg
from graphic_gen import (
    BG_BOT,
    BG_TOP,
    CARD_BG,
    CARD_BORDER,
    COL_DANGER,
    COL_MACPRO,
    COL_NEO,
    COL_STARFIGHTER,
    COL_STUDIO,
    FONT_MONO,
    FONT_SANS,
    H,
    TEXT_DIM,
    TEXT_MAIN,
    TEXT_MUTED,
    W,
    esc,
    svg_header,
    term_window,
)

OUT_DIR = Path(__file__).resolve().parent / "output"
BRAND = "TrashCanAI // MacPro6,1 Benchmarks"


def svg_footer(note: str) -> list[str]:
    return gg.svg_footer(note, brand=BRAND)


def render_svg(name: str, lines: list[str]) -> Path:
    return gg.render_svg(OUT_DIR, name, lines)


def chart_00_gpu_vs_cpu_simple_explainer() -> Path:
    """Early-video conceptual graphic: why GPUs crush CPUs at AI (no dense benchmark tables)."""
    lines = svg_header(
        "Why GPUs Are Built for AI (And CPUs Aren't)",
        "AI models require billions of simple calculations at once, not one complex task at a time",
        "CONCEPT // CPU VS. GPU",
    )

    # Left Card: CPU (x=80..910, w=830, y=206..976, h=770)
    lx, ly, lw, lh = 80, 206, 830, 770
    lines.append(f'  <rect x="{lx}" y="{ly}" width="{lw}" height="{lh}" rx="20" fill="{CARD_BG}" stroke="#475569" stroke-width="2"/>')
    lines.append(f'  <rect x="{lx}" y="{ly}" width="{lw}" height="8" rx="4" fill="#64748B"/>')
    lines.append(f'  <text x="{lx + 34}" y="{ly + 54}" font-family="{FONT_SANS}" font-size="32" font-weight="bold" fill="{TEXT_MAIN}">THE XEON CPU</text>')
    lines.append(f'  <text x="{lx + 34}" y="{ly + 84}" font-family="{FONT_SANS}" font-size="18" fill="{TEXT_MUTED}">Optimized for sequential logic, operating systems, and single-thread speed</text>')

    # Visual Diagram Box inside CPU card
    lines.append(f'  <rect x="{lx + 34}" y="{ly + 108}" width="{lw - 68}" height="240" rx="14" fill="#0F172A" stroke="#334155" stroke-width="1.5"/>')
    lines.append(f'  <text x="{lx + 56}" y="{ly + 140}" font-family="{FONT_MONO}" font-size="16" font-weight="bold" fill="#94A3B8">12 XEON CPU CORES</text>')
    
    # Draw 12 large cores (6x2 grid)
    for r in range(2):
        for c in range(6):
            cx = lx + 56 + c * 52
            cy = ly + 158 + r * 56
            lines.append(f'  <rect x="{cx}" y="{cy}" width="44" height="46" rx="8" fill="#1E293B" stroke="#64748B" stroke-width="1.5"/>')
            lines.append(f'  <text x="{cx + 22}" y="{cy + 29}" text-anchor="middle" font-family="{FONT_MONO}" font-size="14" font-weight="bold" fill="{TEXT_MUTED}">Core</text>')

    # Narrow memory pipe area on right half of CPU diagram
    lines.append(f'  <text x="{lx + 430}" y="{ly + 140}" font-family="{FONT_MONO}" font-size="16" font-weight="bold" fill="{COL_DANGER}">SYSTEM MEMORY BUS</text>')
    lines.append(f'  <rect x="{lx + 430}" y="{ly + 168}" width="320" height="24" rx="8" fill="#1E293B" stroke="#64748B" stroke-width="1.5"/>')
    lines.append(f'  <text x="{lx + 590}" y="{ly + 222}" text-anchor="middle" font-family="{FONT_MONO}" font-size="20" font-weight="bold" fill="{TEXT_MUTED}">Quad-Channel DDR3 (~50 GB/s)</text>')
    lines.append(f'  <text x="{lx + 590}" y="{ly + 252}" text-anchor="middle" font-family="{FONT_SANS}" font-size="16" fill="{TEXT_DIM}">Weights queue up sequentially across system RAM</text>')
    lines.append(f'  <text x="{lx + 590}" y="{ly + 276}" text-anchor="middle" font-family="{FONT_SANS}" font-size="15" fill="{TEXT_DIM}">(Measured: 28.6 GB/s sustained on 14B CPU)</text>')

    cpu_bullets = [
        (
            "Sequential Processing",
            "Built for one complex task at a time. Struggles when millions of numbers must be calculated simultaneously.",
        ),
        (
            "Memory Bandwidth Limit",
            "Every word requires streaming weights from RAM. At ~50 GB/s, memory speed bottlenecks generation.",
        ),
        (
            "The Default Driver Problem",
            "Legacy drivers and ROCm drop the Mac Pro GPUs, trapping AI completely on the CPU.",
        ),
        (
            "Ideal Machine Role",
            "Coordinates Linux, storage, networking, and handles 32B+ models that exceed graphics memory.",
        ),
    ]
    by = ly + 392
    for head, body in cpu_bullets:
        lines.append(f'  <rect x="{lx + 34}" y="{by - 24}" width="8" height="30" rx="4" fill="#64748B"/>')
        lines.append(f'  <text x="{lx + 54}" y="{by}" font-family="{FONT_SANS}" font-size="22" font-weight="bold" fill="{TEXT_MAIN}">{esc(head)}</text>')
        wrapped = textwrap.wrap(body, width=68)
        for line_idx, line_txt in enumerate(wrapped):
            lines.append(f'  <text x="{lx + 54}" y="{by + 28 + line_idx * 26}" font-family="{FONT_SANS}" font-size="18" fill="{TEXT_MUTED}">{esc(line_txt)}</text>')
        by += 94

    # Right Card: Dual GPUs (x=1010..1840, w=830, y=206..976, h=770)
    rx, ry, rw, rh = 1010, 206, 830, 770
    lines.append(f'  <rect x="{rx}" y="{ry}" width="{rw}" height="{rh}" rx="20" fill="{CARD_BG}" stroke="{COL_MACPRO}" stroke-width="2.5"/>')
    lines.append(f'  <rect x="{rx}" y="{ry}" width="{rw}" height="8" rx="4" fill="url(#heroGrad)"/>')
    lines.append(f'  <text x="{rx + 34}" y="{ry + 54}" font-family="{FONT_SANS}" font-size="32" font-weight="bold" fill="{TEXT_MAIN}">DUAL FIREPRO D500 GPUS</text>')
    lines.append(f'  <text x="{rx + 34}" y="{ry + 84}" font-family="{FONT_SANS}" font-size="18" fill="{COL_MACPRO}">Optimized for massive parallel matrix math and dedicated high-bandwidth VRAM</text>')

    # Visual Diagram Box inside GPU card
    lines.append(f'  <rect x="{rx + 34}" y="{ly + 108}" width="{rw - 68}" height="240" rx="14" fill="#0F172A" stroke="#78350F" stroke-width="1.5"/>')
    lines.append(f'  <text x="{rx + 56}" y="{ly + 140}" font-family="{FONT_MONO}" font-size="16" font-weight="bold" fill="{COL_MACPRO}">3,052 GPU CORES (DUAL D500)</text>')
    
    # Dense parallel core grid (20 cols x 7 rows = 140 glowing cores)
    for r in range(7):
        for c in range(20):
            gx = rx + 56 + c * 16
            gy = ly + 158 + r * 16
            lines.append(f'  <rect x="{gx}" y="{gy}" width="11" height="11" rx="2" fill="{COL_MACPRO}" fill-opacity="0.88"/>')

    # Wide multi-lane highway in right half of GPU diagram
    lines.append(f'  <text x="{rx + 430}" y="{ly + 140}" font-family="{FONT_MONO}" font-size="16" font-weight="bold" fill="{COL_STUDIO}">~10x WIDER MEMORY HIGHWAY</text>')
    for lane in range(4):
        ly_bar = ly + 162 + lane * 20
        lines.append(f'  <rect x="{rx + 430}" y="{ly_bar}" width="320" height="13" rx="4" fill="url(#heroGrad)"/>')
    lines.append(f'  <text x="{rx + 590}" y="{ly + 262}" text-anchor="middle" font-family="{FONT_MONO}" font-size="20" font-weight="bold" fill="{COL_MACPRO}">GDDR5 VRAM (2x 240 = 480 GB/s)</text>')
    lines.append(f'  <text x="{rx + 590}" y="{ly + 288}" text-anchor="middle" font-family="{FONT_SANS}" font-size="16" fill="{TEXT_MUTED}">High-speed graphics memory feeds all cores at once</text>')

    gpu_bullets = [
        (
            "Massive Parallelism",
            "Thousands of execution cores calculate whole matrix layers in parallel at the same instant.",
        ),
        (
            "High-Speed GDDR5 Memory",
            "Combined 480 GB/s bandwidth feeds weights to compute units nearly 10x faster than DDR3.",
        ),
        (
            "Why Unlocking Them Matters",
            "Enables full GPU acceleration on 1.5B to 7B models, plus hybrid offload for 14B at interactive speeds.",
        ),
        (
            "Ideal Machine Role",
            "Drives prompt processing, token generation, and vision encoding while keeping CPU load light.",
        ),
    ]
    by = ry + 392
    for head, body in gpu_bullets:
        lines.append(f'  <rect x="{rx + 34}" y="{by - 24}" width="8" height="30" rx="4" fill="{COL_MACPRO}"/>')
        lines.append(f'  <text x="{rx + 54}" y="{by}" font-family="{FONT_SANS}" font-size="22" font-weight="bold" fill="{TEXT_MAIN}">{esc(head)}</text>')
        wrapped = textwrap.wrap(body, width=68)
        for line_idx, line_txt in enumerate(wrapped):
            lines.append(f'  <text x="{rx + 54}" y="{by + 28 + line_idx * 26}" font-family="{FONT_SANS}" font-size="18" fill="{TEXT_MUTED}">{esc(line_txt)}</text>')
        by += 94

    # Centered VS badge between cards (x=960, y=591)
    lines.append(f'  <circle cx="960" cy="591" r="36" fill="#0B1020" stroke="{COL_MACPRO}" stroke-width="2.5"/>')
    lines.append(f'  <text x="960" y="600" text-anchor="middle" font-family="{FONT_MONO}" font-size="24" font-weight="bold" fill="{COL_MACPRO}">VS</text>')

    lines.extend(svg_footer("Architecture comparison: Dual AMD FirePro D500 (3,052 total cores, 480 GB/s) vs. Xeon E5-2697 v2 DDR3 (~50 GB/s)"))
    return render_svg("00_why_gpu_beats_cpu_simple", lines)


def term_window(lines: list[str], x: int, y: int, w: int, h: int, title_bar: str) -> None:
    """Helper to draw a styled dark terminal window card."""
    lines.append(f'  <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" fill="#090D16" stroke="#334155" stroke-width="1.5"/>')
    lines.append(f'  <rect x="{x}" y="{y}" width="{w}" height="36" rx="14" fill="#1E293B"/>')
    lines.append(f'  <rect x="{x}" y="{y + 20}" width="{w}" height="16" fill="#1E293B"/>')
    lines.append(f'  <circle cx="{x + 20}" cy="{y + 18}" r="5.5" fill="#EF4444"/>')
    lines.append(f'  <circle cx="{x + 38}" cy="{y + 18}" r="5.5" fill="#F59E0B"/>')
    lines.append(f'  <circle cx="{x + 56}" cy="{y + 18}" r="5.5" fill="#10B981"/>')
    lines.append(f'  <text x="{x + 80}" y="{y + 23}" font-family="{FONT_MONO}" font-size="14" fill="{TEXT_MUTED}">{esc(title_bar)}</text>')


def chart_09a_driver_step1_grub() -> Path:
    """Full-screen slide: Step 1 - Add Kernel Boot Flags to GRUB."""
    lines = svg_header(
        "Step 1: Add Kernel Boot Flags to GRUB",
        "Disable legacy Southern Islands on radeon (=0) and force the modern amdgpu driver (=1)",
        "DRIVER SETUP // STEP 1 OF 4",
    )

    # Top Terminal Box (x=80, y=210, w=1760, h=410)
    tx, ty, tw, th = 80, 210, 1760, 410
    term_window(lines, tx, ty, tw, th, "bash  //  /etc/default/grub")

    lines.append(f'  <text x="{tx + 36}" y="{ty + 82}" font-family="{FONT_MONO}" font-size="22" font-weight="bold" fill="{COL_STARFIGHTER}">$ sudo nano /etc/default/grub</text>')
    lines.append(f'  <text x="{tx + 36}" y="{ty + 130}" font-family="{FONT_MONO}" font-size="18" fill="{TEXT_DIM}"># 1. Locate the default kernel parameters line (typically quiet splash):</text>')
    lines.append(f'  <text x="{tx + 36}" y="{ty + 168}" font-family="{FONT_MONO}" font-size="20" fill="#94A3B8">GRUB_CMDLINE_LINUX_DEFAULT="quiet splash"</text>')

    lines.append(f'  <text x="{tx + 36}" y="{ty + 226}" font-family="{FONT_MONO}" font-size="18" fill="{TEXT_DIM}"># 2. Append the Southern Islands (si_support) overrides:</text>')
    lines.append(f'  <rect x="{tx + 36}" y="{ty + 252}" width="{tw - 72}" height="76" rx="10" fill="#1E293B" stroke="{COL_MACPRO}" stroke-width="2"/>')
    lines.append(f'  <text x="{tx + 56}" y="{ty + 288}" font-family="{FONT_MONO}" font-size="21" font-weight="bold" fill="{TEXT_MAIN}">GRUB_CMDLINE_LINUX_DEFAULT="quiet splash <tspan fill="{COL_MACPRO}">radeon.si_support=0 amdgpu.si_support=1</tspan>"</text>')
    lines.append(f'  <text x="{tx + 56}" y="{ty + 314}" font-family="{FONT_MONO}" font-size="15" fill="{TEXT_MUTED}">Save and exit: Ctrl+O, Enter, Ctrl+X</text>')

    lines.append(f'  <text x="{tx + 36}" y="{ty + 372}" font-family="{FONT_SANS}" font-size="18" fill="{COL_STUDIO}">Tip: In scripts/restore-trashcan.sh, this edit is automated via Python regex so it can run non-interactively.</text>')

    # Bottom 3 Context Cards (x=80, y=644, h=332)
    cards = [
        (
            "radeon.si_support=0",
            COL_DANGER,
            "#450A0A",
            "Disables Legacy Driver",
            [
                "Tells the legacy radeon kernel driver to ignore GCN 1.0 (Southern Islands) Tahiti chips.",
                "Without this flag, radeon claims both GPUs first, blocking the modern driver from loading.",
            ],
        ),
        (
            "amdgpu.si_support=1",
            COL_MACPRO,
            "#451A03",
            "Enables Modern amdgpu Driver",
            [
                "Forces the modern amdgpu driver to claim and initialize both AMD FirePro D500 GPUs.",
                "Unlocks Mesa RADV Vulkan 1.3 support, giving llama.cpp full multi-GPU hardware acceleration.",
            ],
        ),
        (
            "Why You Need Both Flags",
            COL_STUDIO,
            "#064E3B",
            "Resolves Driver Contention",
            [
                "Southern Islands support in amdgpu is marked experimental, so Ubuntu defaults to radeon.",
                "Passing both parameters simultaneously guarantees zero conflict during initial kernel boot.",
            ],
        ),
    ]

    cx = 80
    cw = 566
    cy = 644
    ch = 332
    for title, accent, bg, badge, bullets in cards:
        lines.append(f'  <rect x="{cx}" y="{cy}" width="{cw}" height="{ch}" rx="16" fill="{CARD_BG}" stroke="{accent}" stroke-width="1.5"/>')
        lines.append(f'  <rect x="{cx + 24}" y="{cy + 24}" width="260" height="34" rx="8" fill="{bg}" stroke="{accent}" stroke-width="1"/>')
        lines.append(f'  <text x="{cx + 154}" y="{cy + 47}" text-anchor="middle" font-family="{FONT_MONO}" font-size="15" font-weight="bold" fill="{accent}">{esc(title)}</text>')
        lines.append(f'  <text x="{cx + 24}" y="{cy + 96}" font-family="{FONT_SANS}" font-size="23" font-weight="bold" fill="{TEXT_MAIN}">{esc(badge)}</text>')

        by = cy + 138
        for b in bullets:
            wrapped = textwrap.wrap(b, width=42)
            lines.append(f'  <circle cx="{cx + 32}" cy="{by - 6}" r="4" fill="{accent}"/>')
            lines.append(f'  <text x="{cx + 48}" y="{by}" font-family="{FONT_SANS}" font-size="17" fill="{TEXT_MUTED}">{esc(wrapped[0])}</text>')
            if len(wrapped) > 1:
                lines.append(f'  <text x="{cx + 48}" y="{by + 26}" font-family="{FONT_SANS}" font-size="17" fill="{TEXT_MUTED}">{esc(wrapped[1])}</text>')
            if len(wrapped) > 2:
                lines.append(f'  <text x="{cx + 48}" y="{by + 52}" font-family="{FONT_SANS}" font-size="17" fill="{TEXT_MUTED}">{esc(wrapped[2])}</text>')
            by += 80

        cx += cw + 31

    lines.extend(svg_footer("Step 1 of 4: GRUB kernel command line configuration for 2013 Mac Pro (Ubuntu Server 24.04 LTS)"))
    return render_svg("09a_driver_step1_grub_boot_flags", lines)


def chart_09b_driver_step2_modprobe() -> Path:
    """Full-screen slide: Step 2 - Lock Modprobe Rules and User Permissions."""
    lines = svg_header(
        "Step 2: Lock Modprobe Rules and User Permissions",
        "Ensure driver priority persists across kernel updates and grant your user account GPU compute access",
        "DRIVER SETUP // STEP 2 OF 4",
    )

    # Left Card: Modprobe conf (x=80, y=210, w=862, h=766)
    lx, ly, lw, lh = 80, 210, 862, 766
    lines.append(f'  <rect x="{lx}" y="{ly}" width="{lw}" height="{lh}" rx="18" fill="{CARD_BG}" stroke="{CARD_BORDER}" stroke-width="1.5"/>')
    lines.append(f'  <rect x="{lx}" y="{ly}" width="{lw}" height="8" rx="4" fill="{COL_STARFIGHTER}"/>')
    lines.append(f'  <text x="{lx + 28}" y="{ly + 52}" font-family="{FONT_SANS}" font-size="28" font-weight="bold" fill="{TEXT_MAIN}">2.1 Create /etc/modprobe.d/amdgpu.conf</text>')
    lines.append(f'  <text x="{lx + 28}" y="{ly + 84}" font-family="{FONT_SANS}" font-size="18" fill="{TEXT_MUTED}">Locks module load options inside the initramfs ramdisk:</text>')

    term_window(lines, lx + 28, ly + 110, lw - 56, 260, "bash  //  persist module options")
    lines.append(f'  <text x="{lx + 52}" y="{ly + 176}" font-family="{FONT_MONO}" font-size="17" fill="{COL_STARFIGHTER}">$ cat &lt;&lt;EOF | sudo tee /etc/modprobe.d/amdgpu.conf</text>')
    lines.append(f'  <text x="{lx + 52}" y="{ly + 214}" font-family="{FONT_MONO}" font-size="18" font-weight="bold" fill="{COL_MACPRO}">options amdgpu si_support=1</text>')
    lines.append(f'  <text x="{lx + 52}" y="{ly + 250}" font-family="{FONT_MONO}" font-size="18" font-weight="bold" fill="{COL_MACPRO}">options radeon si_support=0</text>')
    lines.append(f'  <text x="{lx + 52}" y="{ly + 288}" font-family="{FONT_MONO}" font-size="17" fill="{COL_STARFIGHTER}">EOF</text>')
    lines.append(f'  <text x="{lx + 52}" y="{ly + 332}" font-family="{FONT_MONO}" font-size="15" fill="{COL_STUDIO}"># Also recommended: echo "blacklist radeonfb" | sudo tee ...</text>')

    # Context block inside Left card
    lines.append(f'  <rect x="{lx + 28}" y="{ly + 396}" width="{lw - 56}" height="336" rx="14" fill="#0F172A" stroke="#334155" stroke-width="1.5"/>')
    lines.append(f'  <text x="{lx + 52}" y="{ly + 436}" font-family="{FONT_MONO}" font-size="17" font-weight="bold" fill="{COL_STARFIGHTER}">WHY MODPROBE MATTERS</text>')

    mod_points = [
        ("Survives Kernel Updates", "Ubuntu frequently updates the Linux kernel. A modprobe config file ensures that newly installed kernels always inherit the amdgpu si_support rules."),
        ("Early Boot Hardware Binding", "During initramfs phase, Linux loads drivers before the root filesystem is even mounted. This file instructs the ramdisk to bind amdgpu immediately."),
        ("Prevents Framebuffer Lockup", "Blacklisting radeonfb prevents the legacy console framebuffer from claiming the D500s and crashing early boot."),
    ]
    my = ly + 476
    for m_head, m_desc in mod_points:
        lines.append(f'  <circle cx="{lx + 60}" cy="{my - 6}" r="4" fill="{COL_STARFIGHTER}"/>')
        lines.append(f'  <text x="{lx + 76}" y="{my}" font-family="{FONT_SANS}" font-size="19" font-weight="bold" fill="{TEXT_MAIN}">{esc(m_head)}</text>')
        wrapped = textwrap.wrap(m_desc, width=64)
        for widx, wline in enumerate(wrapped):
            lines.append(f'  <text x="{lx + 76}" y="{my + 24 + widx * 22}" font-family="{FONT_SANS}" font-size="16" fill="{TEXT_MUTED}">{esc(wline)}</text>')
        my += 86

    # Right Card: Groups and permissions (x=978, y=210, w=862, h=766)
    rx, ry, rw, rh = 978, 210, 862, 766
    lines.append(f'  <rect x="{rx}" y="{ry}" width="{rw}" height="{rh}" rx="18" fill="{CARD_BG}" stroke="{COL_MACPRO}" stroke-width="2"/>')
    lines.append(f'  <rect x="{rx}" y="{ry}" width="{rw}" height="8" rx="4" fill="url(#heroGrad)"/>')
    lines.append(f'  <text x="{rx + 28}" y="{ry + 52}" font-family="{FONT_SANS}" font-size="28" font-weight="bold" fill="{TEXT_MAIN}">2.2 Add User to video and render Groups</text>')
    lines.append(f'  <text x="{rx + 28}" y="{ry + 84}" font-family="{FONT_SANS}" font-size="18" fill="{COL_MACPRO}">Allows non-root access to GPU compute and DRM render nodes:</text>')

    term_window(lines, rx + 28, ry + 110, rw - 56, 260, "bash  //  user compute permissions")
    lines.append(f'  <text x="{rx + 52}" y="{ry + 176}" font-family="{FONT_MONO}" font-size="18" font-weight="bold" fill="{TEXT_MAIN}">$ sudo usermod -aG video,render $USER</text>')
    lines.append(f'  <text x="{rx + 52}" y="{ry + 220}" font-family="{FONT_MONO}" font-size="16" fill="{TEXT_DIM}"># Verify active group memberships:</text>')
    lines.append(f'  <text x="{rx + 52}" y="{ry + 256}" font-family="{FONT_MONO}" font-size="17" fill="{COL_STARFIGHTER}">$ groups</text>')
    lines.append(f'  <text x="{rx + 52}" y="{ry + 292}" font-family="{FONT_MONO}" font-size="17" font-weight="bold" fill="{COL_STUDIO}">zachary adm cdrom sudo dip plugdev video render</text>')
    lines.append(f'  <text x="{rx + 52}" y="{ry + 332}" font-family="{FONT_MONO}" font-size="14" fill="{TEXT_MUTED}">(Log out and log back in, or reboot in Step 3 for groups to take effect)</text>')

    # Context block inside Right card
    lines.append(f'  <rect x="{rx + 28}" y="{ry + 396}" width="{rw - 56}" height="336" rx="14" fill="#0F172A" stroke="#78350F" stroke-width="1.5"/>')
    lines.append(f'  <text x="{rx + 52}" y="{ry + 436}" font-family="{FONT_MONO}" font-size="17" font-weight="bold" fill="{COL_MACPRO}">HARDWARE DEVICE ACCESS</text>')

    dev_points = [
        ("/dev/dri/renderD128 & renderD129", "The two AMD FirePro D500 GPUs expose direct compute rendering nodes in Linux. Vulkan shaders send matrix math through these nodes."),
        ("No Root Privileges Required", "Adding your user to the render group lets llama-server, llama-bench, and trash-top query and compute on the GPUs securely without sudo."),
        ("Seamless LAN Deployment", "Enables the trashcan-ai background service to run as a standard system user safely in production."),
    ]
    dy = ry + 476
    for d_head, d_desc in dev_points:
        lines.append(f'  <circle cx="{rx + 60}" cy="{dy - 6}" r="4" fill="{COL_MACPRO}"/>')
        lines.append(f'  <text x="{rx + 76}" y="{dy}" font-family="{FONT_SANS}" font-size="19" font-weight="bold" fill="{TEXT_MAIN}">{esc(d_head)}</text>')
        wrapped = textwrap.wrap(d_desc, width=64)
        for widx, wline in enumerate(wrapped):
            lines.append(f'  <text x="{rx + 76}" y="{dy + 24 + widx * 22}" font-family="{FONT_SANS}" font-size="16" fill="{TEXT_MUTED}">{esc(wline)}</text>')
        dy += 86

    lines.extend(svg_footer("Step 2 of 4: Modprobe persistence and user render group access for Dual FirePro D500s"))
    return render_svg("09b_driver_step2_modprobe_permissions", lines)


def chart_09c_driver_step3_rebuild_reboot() -> Path:
    """Full-screen slide: Step 3 - Rebuild Boot Images, Install Mesa & Reboot."""
    lines = svg_header(
        "Step 3: Rebuild Boot Images, Install Mesa & Reboot",
        "Bake kernel parameters into initramfs, install user-space Vulkan libraries, and restart",
        "DRIVER SETUP // STEP 3 OF 4",
    )

    # Top Big Terminal Box (x=80, y=210, w=1760, h=430)
    tx, ty, tw, th = 80, 210, 1760, 430
    term_window(lines, tx, ty, tw, th, "bash  //  apply configuration & install Vulkan")

    lines.append(f'  <text x="{tx + 36}" y="{ty + 76}" font-family="{FONT_MONO}" font-size="17" fill="{TEXT_DIM}"># 1. Update GRUB bootloader configuration file:</text>')
    lines.append(f'  <text x="{tx + 36}" y="{ty + 106}" font-family="{FONT_MONO}" font-size="22" font-weight="bold" fill="{TEXT_MAIN}">$ sudo update-grub</text>')
    lines.append(f'  <text x="{tx + 36}" y="{ty + 134}" font-family="{FONT_MONO}" font-size="16" fill="{COL_STUDIO}">Generating grub configuration file ... Found linux image: /boot/vmlinuz ... done</text>')

    lines.append(f'  <text x="{tx + 36}" y="{ty + 180}" font-family="{FONT_MONO}" font-size="17" fill="{TEXT_DIM}"># 2. Rebuild the initial RAM disk image:</text>')
    lines.append(f'  <text x="{tx + 36}" y="{ty + 210}" font-family="{FONT_MONO}" font-size="22" font-weight="bold" fill="{TEXT_MAIN}">$ sudo update-initramfs -u</text>')
    lines.append(f'  <text x="{tx + 36}" y="{ty + 238}" font-family="{FONT_MONO}" font-size="16" fill="{COL_STUDIO}">update-initramfs: Generating /boot/initrd.img-6.8.0-xx-generic</text>')

    lines.append(f'  <text x="{tx + 36}" y="{ty + 284}" font-family="{FONT_MONO}" font-size="17" fill="{TEXT_DIM}"># 3. Install Mesa Vulkan drivers and diagnostic tools:</text>')
    lines.append(f'  <text x="{tx + 36}" y="{ty + 314}" font-family="{FONT_MONO}" font-size="21" font-weight="bold" fill="{COL_STARFIGHTER}">$ sudo apt install -y mesa-vulkan-drivers vulkan-tools libvulkan-dev</text>')

    lines.append(f'  <text x="{tx + 36}" y="{ty + 364}" font-family="{FONT_MONO}" font-size="17" fill="{TEXT_DIM}"># 4. Reboot to load the new kernel driver:</text>')
    lines.append(f'  <text x="{tx + 36}" y="{ty + 396}" font-family="{FONT_MONO}" font-size="23" font-weight="bold" fill="{COL_MACPRO}">$ sudo reboot</text>')

    # Bottom 3 Action Cards (x=80, y=662, h=314)
    cards = [
        (
            "update-grub",
            COL_STARFIGHTER,
            "Rewrites /boot/grub/grub.cfg",
            "Scans /etc/default/grub and writes the new radeon.si_support=0 amdgpu.si_support=1 arguments directly into the boot menu entries.",
        ),
        (
            "update-initramfs -u",
            COL_MACPRO,
            "Rebuilds the Early RAM Disk",
            "Packs /etc/modprobe.d/amdgpu.conf into the boot image so the kernel receives the driver overrides before mounting filesystems.",
        ),
        (
            "sudo reboot",
            COL_STUDIO,
            "Loads the amdgpu Kernel Module",
            "Linux cannot hot-swap the active display driver while the console is running. A reboot cleanly initializes both D500s on amdgpu.",
        ),
    ]

    cx = 80
    cw = 566
    cy = 662
    ch = 314
    for cmd, col, subhead, desc in cards:
        lines.append(f'  <rect x="{cx}" y="{cy}" width="{cw}" height="{ch}" rx="16" fill="{CARD_BG}" stroke="{CARD_BORDER}" stroke-width="1.5"/>')
        lines.append(f'  <text x="{cx + 28}" y="{cy + 46}" font-family="{FONT_MONO}" font-size="24" font-weight="bold" fill="{col}">$ {esc(cmd)}</text>')
        lines.append(f'  <text x="{cx + 28}" y="{cy + 82}" font-family="{FONT_SANS}" font-size="20" font-weight="bold" fill="{TEXT_MAIN}">{esc(subhead)}</text>')
        lines.append(f'  <line x1="{cx + 28}" y1="{cy + 104}" x2="{cx + cw - 28}" y2="{cy + 104}" stroke="{CARD_BORDER}" stroke-width="1"/>')

        wrapped = textwrap.wrap(desc, width=44)
        wy = cy + 144
        for wline in wrapped:
            lines.append(f'  <text x="{cx + 28}" y="{wy}" font-family="{FONT_SANS}" font-size="18" fill="{TEXT_MUTED}">{esc(wline)}</text>')
            wy += 28

        cx += cw + 31

    lines.extend(svg_footer("Step 3 of 4: Applying bootloader changes, installing Mesa Vulkan, and rebooting Mac Pro"))
    return render_svg("09c_driver_step3_rebuild_initramfs_reboot", lines)


def chart_09d_driver_step4_verify_vulkan() -> Path:
    """Full-screen slide: Step 4 - Verify Dual-GPU Vulkan Is Active."""
    lines = svg_header(
        "Step 4: Verify Both GPUs Switched to amdgpu & Vulkan",
        "Confirm kernel driver binding and dual-GPU Vulkan 1.3 detection after system reboot",
        "DRIVER SETUP // STEP 4 OF 4",
    )

    # Left Card: lspci (x=80, y=210, w=862, h=766)
    lx, ly, lw, lh = 80, 210, 862, 766
    lines.append(f'  <rect x="{lx}" y="{ly}" width="{lw}" height="{lh}" rx="18" fill="{CARD_BG}" stroke="{COL_STARFIGHTER}" stroke-width="1.5"/>')
    lines.append(f'  <rect x="{lx}" y="{ly}" width="{lw}" height="8" rx="4" fill="{COL_STARFIGHTER}"/>')
    lines.append(f'  <text x="{lx + 28}" y="{ly + 52}" font-family="{FONT_SANS}" font-size="28" font-weight="bold" fill="{TEXT_MAIN}">4.1 Kernel Driver Verification</text>')
    lines.append(f'  <text x="{lx + 28}" y="{ly + 84}" font-family="{FONT_SANS}" font-size="18" fill="{TEXT_MUTED}">Check that both PCI devices are actively bound to amdgpu:</text>')

    term_window(lines, lx + 28, ly + 110, lw - 56, 360, "bash  //  lspci -nnk")
    lines.append(f'  <text x="{lx + 52}" y="{ly + 172}" font-family="{FONT_MONO}" font-size="17" font-weight="bold" fill="{COL_STARFIGHTER}">$ lspci -nnk | grep -EA3 "VGA|3D"</text>')
    lines.append(f'  <text x="{lx + 52}" y="{ly + 208}" font-family="{FONT_MONO}" font-size="14" fill="{TEXT_MUTED}">01:00.0 VGA compatible controller [0300]: AMD Tahiti LE [FirePro D500]</text>')
    lines.append(f'  <text x="{lx + 52}" y="{ly + 236}" font-family="{FONT_MONO}" font-size="16" font-weight="bold" fill="{COL_STUDIO}">        Kernel driver in use: amdgpu</text>')
    lines.append(f'  <text x="{lx + 52}" y="{ly + 260}" font-family="{FONT_MONO}" font-size="14" fill="{TEXT_DIM}">        Kernel modules: radeon, amdgpu</text>')
    lines.append(f'  <text x="{lx + 52}" y="{ly + 294}" font-family="{FONT_MONO}" font-size="14" fill="{TEXT_MUTED}">02:00.0 Display controller [0380]: AMD Tahiti LE [FirePro D500]</text>')
    lines.append(f'  <text x="{lx + 52}" y="{ly + 322}" font-family="{FONT_MONO}" font-size="16" font-weight="bold" fill="{COL_STUDIO}">        Kernel driver in use: amdgpu</text>')
    lines.append(f'  <text x="{lx + 52}" y="{ly + 346}" font-family="{FONT_MONO}" font-size="14" fill="{TEXT_DIM}">        Kernel modules: radeon, amdgpu</text>')
    lines.append(f'  <text x="{lx + 52}" y="{ly + 400}" font-family="{FONT_MONO}" font-size="15" fill="{COL_STUDIO}">Check: Both GPUs report "Kernel driver in use: amdgpu"</text>')

    # Verification checklist inside Left card
    lines.append(f'  <rect x="{lx + 28}" y="{ly + 496}" width="{lw - 56}" height="240" rx="14" fill="#0F172A" stroke="#334155" stroke-width="1.5"/>')
    lines.append(f'  <text x="{lx + 52}" y="{ly + 536}" font-family="{FONT_MONO}" font-size="17" font-weight="bold" fill="{COL_STARFIGHTER}">PCI BUS VALIDATION</text>')

    pci_checks = [
        "Both FirePro D500 GPUs are visible on separate PCI buses (01:00.0 and 02:00.0).",
        "Neither card is held hostage by the obsolete radeon driver.",
        "Both GPUs run at full PCIe 3.0 x16 (8 GT/s) link bandwidth for fast tensor offload.",
    ]
    py = ly + 576
    for ptext in pci_checks:
        lines.append(f'  <circle cx="{lx + 60}" cy="{py - 6}" r="4" fill="{COL_STUDIO}"/>')
        wrapped = textwrap.wrap(ptext, width=58)
        lines.append(f'  <text x="{lx + 76}" y="{py}" font-family="{FONT_SANS}" font-size="17" fill="{TEXT_MAIN}">{esc(wrapped[0])}</text>')
        if len(wrapped) > 1:
            lines.append(f'  <text x="{lx + 76}" y="{py + 24}" font-family="{FONT_SANS}" font-size="17" fill="{TEXT_MUTED}">{esc(wrapped[1])}</text>')
        py += 56

    # Right Card: vulkaninfo (x=978, y=210, w=862, h=766)
    rx, ry, rw, rh = 978, 210, 862, 766
    lines.append(f'  <rect x="{rx}" y="{ry}" width="{rw}" height="{rh}" rx="18" fill="{CARD_BG}" stroke="{COL_STUDIO}" stroke-width="2"/>')
    lines.append(f'  <rect x="{rx}" y="{ry}" width="{rw}" height="8" rx="4" fill="{COL_STUDIO}"/>')
    lines.append(f'  <text x="{rx + 28}" y="{ry + 52}" font-family="{FONT_SANS}" font-size="28" font-weight="bold" fill="{TEXT_MAIN}">4.2 Vulkan 1.3 Detection</text>')
    lines.append(f'  <text x="{rx + 28}" y="{ry + 84}" font-family="{FONT_SANS}" font-size="18" fill="{COL_STUDIO}">Verify Mesa RADV exposes both GPUs to Vulkan compute:</text>')

    term_window(lines, rx + 28, ry + 110, rw - 56, 360, "bash  //  vulkaninfo --summary")
    lines.append(f'  <text x="{rx + 52}" y="{ry + 172}" font-family="{FONT_MONO}" font-size="17" font-weight="bold" fill="{COL_STARFIGHTER}">$ vulkaninfo --summary</text>')
    lines.append(f'  <text x="{rx + 52}" y="{ry + 208}" font-family="{FONT_MONO}" font-size="16" fill="{TEXT_MAIN}">Vulkan API Version: <tspan fill="{COL_STUDIO}" font-weight="bold">1.3.xxx</tspan></text>')
    lines.append(f'  <text x="{rx + 52}" y="{ry + 242}" font-family="{FONT_MONO}" font-size="15" fill="{TEXT_DIM}">Devices:</text>')
    lines.append(f'  <text x="{rx + 52}" y="{ry + 274}" font-family="{FONT_MONO}" font-size="16" font-weight="bold" fill="{COL_MACPRO}">GPU0: AMD Radeon HD 7800 Series (RADV TAHITI)</text>')
    lines.append(f'  <text x="{rx + 76}" y="{ry + 298}" font-family="{FONT_MONO}" font-size="14" fill="{TEXT_MUTED}">deviceType = PHYSICAL_DEVICE_TYPE_DISCRETE_GPU (3072 MiB VRAM)</text>')
    lines.append(f'  <text x="{rx + 52}" y="{ry + 332}" font-family="{FONT_MONO}" font-size="16" font-weight="bold" fill="{COL_MACPRO}">GPU1: AMD Radeon HD 7800 Series (RADV TAHITI)</text>')
    lines.append(f'  <text x="{rx + 76}" y="{ry + 356}" font-family="{FONT_MONO}" font-size="14" fill="{TEXT_MUTED}">deviceType = PHYSICAL_DEVICE_TYPE_DISCRETE_GPU (3072 MiB VRAM)</text>')
    lines.append(f'  <text x="{rx + 52}" y="{ry + 400}" font-family="{FONT_MONO}" font-size="15" fill="{COL_STUDIO}">Total accelerated graphics memory: 6,144 MiB (~6.1 GB)</text>')

    # Bottom Victory Box inside Right card
    lines.append(f'  <rect x="{rx + 28}" y="{ry + 496}" width="{rw - 56}" height="240" rx="14" fill="#064E3B" fill-opacity="0.5" stroke="{COL_STUDIO}" stroke-width="1.5"/>')
    lines.append(f'  <text x="{rx + 52}" y="{ry + 536}" font-family="{FONT_MONO}" font-size="18" font-weight="bold" fill="#6EE7B7">READY FOR LLAMA.CPP VULKAN</text>')

    vulkan_wins = [
        "llama-cli and llama-server can now offload model layers using -ngl.",
        "Multi-GPU layer splitting enabled with --tensor-split 1,1 (--split-mode layer).",
        "Full 28-layer 7B models fit 100% inside VRAM across both GPUs at 13.0 tok/s.",
    ]
    vy = ry + 576
    for vtext in vulkan_wins:
        lines.append(f'  <circle cx="{rx + 60}" cy="{vy - 6}" r="4" fill="#6EE7B7"/>')
        wrapped = textwrap.wrap(vtext, width=58)
        lines.append(f'  <text x="{rx + 76}" y="{vy}" font-family="{FONT_SANS}" font-size="17" fill="{TEXT_MAIN}">{esc(wrapped[0])}</text>')
        if len(wrapped) > 1:
            lines.append(f'  <text x="{rx + 76}" y="{vy + 24}" font-family="{FONT_SANS}" font-size="17" fill="{TEXT_MUTED}">{esc(wrapped[1])}</text>')
        vy += 56

    lines.extend(svg_footer("Step 4 of 4: Dual AMD FirePro D500 Vulkan 1.3 verification complete"))
    return render_svg("09d_driver_step4_verify_vulkan_detection", lines)


def chart_10_build_custom_llama() -> Path:
    """Light-on-text, pause-friendly slide: Building custom llama.cpp for the 2013 Mac Pro."""
    lines = svg_header(
        "Building Custom llama.cpp for the 2013 Mac Pro",
        "Enables Vulkan dual-GPU acceleration while disabling AVX2 to prevent Ivy Bridge crashes",
        "BUILD GUIDE // LLAMA.CPP FOR TRASH CAN",
    )

    # Full-Height Terminal Card (x=80, y=210, w=1760, h=766)
    tx, ty, tw, th = 80, 210, 1760, 766
    term_window(lines, tx, ty, tw, th, "bash  //  build llama.cpp with Ivy Bridge AVX + Vulkan")

    # Step 1
    lines.append(f'  <text x="{tx + 44}" y="{ty + 84}" font-family="{FONT_MONO}" font-size="18" fill="{TEXT_DIM}"># 1. Clone repository and create build directory:</text>')
    lines.append(f'  <text x="{tx + 44}" y="{ty + 120}" font-family="{FONT_MONO}" font-size="22" font-weight="bold" fill="{COL_STARFIGHTER}">$ git clone https://github.com/ggerganov/llama.cpp.git</text>')
    lines.append(f'  <text x="{tx + 44}" y="{ty + 156}" font-family="{FONT_MONO}" font-size="22" font-weight="bold" fill="{COL_STARFIGHTER}">$ cd llama.cpp &amp;&amp; mkdir build &amp;&amp; cd build</text>')

    # Step 2: CMake with highlighted box
    lines.append(f'  <text x="{tx + 44}" y="{ty + 214}" font-family="{FONT_MONO}" font-size="18" fill="{TEXT_DIM}"># 2. Configure with CMake (CRITICAL FLAGS FOR 2013 MAC PRO):</text>')

    lines.append(f'  <rect x="{tx + 44}" y="{ty + 236}" width="{tw - 88}" height="236" rx="12" fill="#1E293B" stroke="{COL_MACPRO}" stroke-width="2"/>')
    lines.append(f'  <text x="{tx + 72}" y="{ty + 278}" font-family="{FONT_MONO}" font-size="23" font-weight="bold" fill="{TEXT_MAIN}">$ cmake .. \\</text>')
    lines.append(f'  <text x="{tx + 116}" y="{ty + 316}" font-family="{FONT_MONO}" font-size="23" font-weight="bold" fill="{COL_STUDIO}">    -DGGML_VULKAN=ON \\         <tspan font-size="18" fill="{TEXT_MUTED}"># Unlocks Dual FirePro D500 GPUs (Mesa RADV)</tspan></text>')
    lines.append(f'  <text x="{tx + 116}" y="{ty + 354}" font-family="{FONT_MONO}" font-size="23" font-weight="bold" fill="{COL_MACPRO}">    -DGGML_AVX=ON \\            <tspan font-size="18" fill="{TEXT_MUTED}"># Supported by Ivy Bridge Xeon</tspan></text>')
    lines.append(f'  <text x="{tx + 116}" y="{ty + 392}" font-family="{FONT_MONO}" font-size="23" font-weight="bold" fill="{COL_DANGER}">    -DGGML_AVX2=OFF -DGGML_FMA=OFF \\ <tspan font-size="18" fill="#FCA5A5"># PREVENTS "Illegal instruction" CRASH</tspan></text>')
    lines.append(f'  <text x="{tx + 116}" y="{ty + 430}" font-family="{FONT_MONO}" font-size="23" font-weight="bold" fill="{TEXT_MAIN}">    -DGGML_F16C=ON -DCMAKE_BUILD_TYPE=Release</text>')

    # Step 3
    lines.append(f'  <text x="{tx + 44}" y="{ty + 518}" font-family="{FONT_MONO}" font-size="18" fill="{TEXT_DIM}"># 3. Compile in parallel across all 12 cores (24 threads):</text>')
    lines.append(f'  <text x="{tx + 44}" y="{ty + 556}" font-family="{FONT_MONO}" font-size="25" font-weight="bold" fill="{TEXT_MAIN}">$ cmake --build . --config Release -j$(nproc)</text>')

    # Step 4
    lines.append(f'  <text x="{tx + 44}" y="{ty + 620}" font-family="{FONT_MONO}" font-size="18" fill="{TEXT_DIM}"># 4. Verify GPU detection:</text>')
    lines.append(f'  <text x="{tx + 44}" y="{ty + 658}" font-family="{FONT_MONO}" font-size="23" font-weight="bold" fill="{COL_STARFIGHTER}">$ ./bin/llama-cli --list-devices</text>')
    lines.append(f'  <text x="{tx + 44}" y="{ty + 694}" font-family="{FONT_MONO}" font-size="18" font-weight="bold" fill="{COL_STUDIO}">Vulkan0: AMD Radeon HD 7800 Series (RADV TAHITI) (3072 MiB, discrete GPU)</text>')
    lines.append(f'  <text x="{tx + 44}" y="{ty + 724}" font-family="{FONT_MONO}" font-size="18" font-weight="bold" fill="{COL_STUDIO}">Vulkan1: AMD Radeon HD 7800 Series (RADV TAHITI) (3072 MiB, discrete GPU)</text>')

    lines.extend(svg_footer("Tested on 12-core Xeon E5-2697 v2 with Dual AMD FirePro D500 (commit 0f35d6d7b)"))
    return render_svg("10_build_custom_llama_cpp", lines)


def chart_11_thread_scaling_12_vs_24() -> Path:
    """Simple high-impact graphic: performance gain from 12 physical cores vs 24 threads."""
    lines = svg_header(
        "Physical Cores vs. Hyper-Threading: Why 12 Beats 24",
        "On a 12-core Xeon, matching threads to physical cores (-t 12) is +12% faster than -t 24",
        "CPU TUNING // THREAD SCALING",
    )

    # Left Card: 24 Threads (x=80, y=208, w=840, h=766)
    lx, ly, lw, lh = 80, 208, 840, 766
    lines.append(f'  <rect x="{lx}" y="{ly}" width="{lw}" height="{lh}" rx="20" fill="{CARD_BG}" stroke="#475569" stroke-width="2"/>')
    lines.append(f'  <rect x="{lx}" y="{ly}" width="{lw}" height="8" rx="4" fill="#64748B"/>')
    lines.append(f'  <rect x="{lx + 36}" y="{ly + 36}" width="110" height="34" rx="8" fill="#1E293B" stroke="#64748B" stroke-width="1"/>')
    lines.append(f'  <text x="{lx + 91}" y="{ly + 59}" text-anchor="middle" font-family="{FONT_MONO}" font-size="17" font-weight="bold" fill="#94A3B8">-t 24</text>')
    lines.append(f'  <text x="{lx + 164}" y="{ly + 62}" font-family="{FONT_SANS}" font-size="30" font-weight="bold" fill="{TEXT_MAIN}">24 Threads (Hyper-Threading)</text>')
    lines.append(f'  <text x="{lx + 36}" y="{ly + 104}" font-family="{FONT_SANS}" font-size="20" fill="{TEXT_MUTED}">All logical threads active (2 threads per physical core)</text>')

    # Speed display inside Left Card
    lines.append(f'  <rect x="{lx + 36}" y="{ly + 140}" width="{lw - 72}" height="184" rx="16" fill="#0F172A" stroke="#334155" stroke-width="1.5"/>')
    lines.append(f'  <text x="{lx + 64}" y="{ly + 184}" font-family="{FONT_MONO}" font-size="16" font-weight="bold" fill="{TEXT_DIM}">TOKEN GENERATION SPEED (7B Q4_K_M)</text>')
    lines.append(f'  <text x="{lx + 64}" y="{ly + 258}" font-family="{FONT_MONO}" font-size="64" font-weight="bold" fill="{TEXT_MUTED}">9.45 <tspan font-size="26" fill="{TEXT_DIM}">tok/s</tspan></text>')
    lines.append(f'  <text x="{lx + 64}" y="{ly + 298}" font-family="{FONT_MONO}" font-size="18" fill="{TEXT_DIM}">Prompt prefill: 55.5 tok/s</text>')

    # Diagram inside Left Card: Shared Core Contention
    lines.append(f'  <rect x="{lx + 36}" y="{ly + 356}" width="{lw - 72}" height="284" rx="16" fill="#0F172A" stroke="#450A0A" stroke-width="1.5"/>')
    lines.append(f'  <text x="{lx + 64}" y="{ly + 398}" font-family="{FONT_MONO}" font-size="17" font-weight="bold" fill="{COL_DANGER}">RESOURCE CONTENTION INSIDE CORE</text>')

    # Visual core box with 2 threads squeezed into 1 core
    lines.append(f'  <rect x="{lx + 64}" y="{ly + 424}" width="346" height="176" rx="12" fill="#1E293B" stroke="{COL_DANGER}" stroke-width="1.5"/>')
    lines.append(f'  <text x="{lx + 86}" y="{ly + 458}" font-family="{FONT_MONO}" font-size="15" font-weight="bold" fill="#94A3B8">PHYSICAL CORE 0</text>')

    lines.append(f'  <rect x="{lx + 86}" y="{ly + 478}" width="142" height="44" rx="8" fill="#334155" stroke="#64748B" stroke-width="1"/>')
    lines.append(f'  <text x="{lx + 157}" y="{ly + 506}" text-anchor="middle" font-family="{FONT_MONO}" font-size="15" font-weight="bold" fill="{TEXT_MUTED}">Thread 0</text>')

    lines.append(f'  <rect x="{lx + 246}" y="{ly + 478}" width="142" height="44" rx="8" fill="#334155" stroke="#64748B" stroke-width="1"/>')
    lines.append(f'  <text x="{lx + 317}" y="{ly + 506}" text-anchor="middle" font-family="{FONT_MONO}" font-size="15" font-weight="bold" fill="{TEXT_MUTED}">Thread 12</text>')

    lines.append(f'  <text x="{lx + 237}" y="{ly + 566}" text-anchor="middle" font-family="{FONT_SANS}" font-size="15" fill="{COL_DANGER}">Fighting for same AVX units &amp; L1/L2 cache</text>')

    # Bullet points on right of diagram
    lines.append(f'  <text x="{lx + 436}" y="{ly + 464}" font-family="{FONT_SANS}" font-size="18" fill="{TEXT_MAIN}">• L1/L2 cache lines evicted constantly</text>')
    lines.append(f'  <text x="{lx + 436}" y="{ly + 514}" font-family="{FONT_SANS}" font-size="18" fill="{TEXT_MAIN}">• SIMD execution ports stalled</text>')
    lines.append(f'  <text x="{lx + 436}" y="{ly + 564}" font-family="{FONT_SANS}" font-size="18" fill="{COL_DANGER}">• Slower output + higher overhead</text>')

    # Left Card Status Pill
    lines.append(f'  <rect x="{lx + 36}" y="{ly + 672}" width="{lw - 72}" height="58" rx="12" fill="#450A0A" stroke="{COL_DANGER}" stroke-width="1.5"/>')
    lines.append(f'  <text x="{lx + lw // 2}" y="{ly + 708}" text-anchor="middle" font-family="{FONT_MONO}" font-size="19" font-weight="bold" fill="#FCA5A5">SLOWER: -11% DROP FROM HARDWARE CONTENTION</text>')

    # Right Card: 12 Threads (Hero) (x=1000, y=208, w=840, h=766)
    rx, ry, rw, rh = 1000, 208, 840, 766
    lines.append(f'  <rect x="{rx}" y="{ry}" width="{rw}" height="{rh}" rx="20" fill="{CARD_BG}" stroke="{COL_STUDIO}" stroke-width="2.5"/>')
    lines.append(f'  <rect x="{rx}" y="{ry}" width="{rw}" height="8" rx="4" fill="{COL_STUDIO}"/>')
    lines.append(f'  <rect x="{rx + 36}" y="{ry + 36}" width="110" height="34" rx="8" fill="#064E3B" stroke="{COL_STUDIO}" stroke-width="1"/>')
    lines.append(f'  <text x="{rx + 91}" y="{ry + 59}" text-anchor="middle" font-family="{FONT_MONO}" font-size="17" font-weight="bold" fill="#6EE7B7">-t 12</text>')
    lines.append(f'  <text x="{rx + 164}" y="{ry + 62}" font-family="{FONT_SANS}" font-size="30" font-weight="bold" fill="{TEXT_MAIN}">12 Threads (Physical Cores Only)</text>')
    lines.append(f'  <text x="{rx + 36}" y="{ry + 104}" font-family="{FONT_SANS}" font-size="20" fill="{COL_STUDIO}">1 thread per physical core (Optimal configuration)</text>')

    # Speed display inside Right Card
    lines.append(f'  <rect x="{rx + 36}" y="{ry + 140}" width="{rw - 72}" height="184" rx="16" fill="#0F172A" stroke="{COL_STUDIO}" stroke-width="1.5"/>')
    lines.append(f'  <text x="{rx + 64}" y="{ry + 184}" font-family="{FONT_MONO}" font-size="16" font-weight="bold" fill="{COL_MACPRO}">TOKEN GENERATION SPEED (7B Q4_K_M)</text>')
    lines.append(f'  <text x="{rx + 64}" y="{ry + 258}" font-family="{FONT_MONO}" font-size="64" font-weight="bold" fill="{TEXT_MAIN}">10.59 <tspan font-size="26" fill="{COL_STUDIO}">tok/s</tspan></text>')
    lines.append(f'  <text x="{rx + 64}" y="{ry + 298}" font-family="{FONT_MONO}" font-size="18" fill="{COL_STUDIO}">Prompt prefill: 57.9 tok/s (+4.3% faster prefill)</text>')

    # Gain badge inside speed display
    lines.append(f'  <rect x="{rx + rw - 248}" y="{ry + 174}" width="184" height="58" rx="12" fill="#064E3B" stroke="{COL_STUDIO}" stroke-width="1.5"/>')
    lines.append(f'  <text x="{rx + rw - 156}" y="{ry + 211}" text-anchor="middle" font-family="{FONT_MONO}" font-size="23" font-weight="bold" fill="#6EE7B7">+12% FASTER</text>')

    # Diagram inside Right Card: Dedicated Core Resources
    lines.append(f'  <rect x="{rx + 36}" y="{ry + 356}" width="{rw - 72}" height="284" rx="16" fill="#0F172A" stroke="#064E3B" stroke-width="1.5"/>')
    lines.append(f'  <text x="{rx + 64}" y="{ry + 398}" font-family="{FONT_MONO}" font-size="17" font-weight="bold" fill="{COL_STUDIO}">DEDICATED CORE RESOURCES</text>')

    # Visual core box with 1 dedicated thread per core
    lines.append(f'  <rect x="{rx + 64}" y="{ry + 424}" width="346" height="176" rx="12" fill="#1E293B" stroke="{COL_STUDIO}" stroke-width="1.5"/>')
    lines.append(f'  <text x="{rx + 86}" y="{ry + 458}" font-family="{FONT_MONO}" font-size="15" font-weight="bold" fill="#94A3B8">PHYSICAL CORE 0</text>')

    lines.append(f'  <rect x="{rx + 86}" y="{ry + 478}" width="302" height="44" rx="8" fill="#064E3B" stroke="{COL_STUDIO}" stroke-width="1.5"/>')
    lines.append(f'  <text x="{rx + 237}" y="{ry + 506}" text-anchor="middle" font-family="{FONT_MONO}" font-size="16" font-weight="bold" fill="#6EE7B7">Thread 0 (100% Dedicated)</text>')

    lines.append(f'  <text x="{rx + 237}" y="{ly + 566}" text-anchor="middle" font-family="{FONT_SANS}" font-size="15" fill="{COL_STUDIO}">Full L1/L2 cache + unshared AVX ports</text>')

    # Bullet points on right of diagram
    lines.append(f'  <text x="{rx + 436}" y="{ry + 464}" font-family="{FONT_SANS}" font-size="18" fill="{TEXT_MAIN}">• 100% of L1/L2 cache per thread</text>')
    lines.append(f'  <text x="{rx + 436}" y="{ry + 514}" font-family="{FONT_SANS}" font-size="18" fill="{TEXT_MAIN}">• Zero execution port contention</text>')
    lines.append(f'  <text x="{rx + 436}" y="{ry + 564}" font-family="{FONT_SANS}" font-size="18" fill="{COL_STUDIO}">• Maximum sustained matrix throughput</text>')

    # Right Card Status Pill
    lines.append(f'  <rect x="{rx + 36}" y="{ry + 672}" width="{rw - 72}" height="58" rx="12" fill="#064E3B" stroke="{COL_STUDIO}" stroke-width="1.5"/>')
    lines.append(f'  <text x="{rx + rw // 2}" y="{ry + 708}" text-anchor="middle" font-family="{FONT_MONO}" font-size="19" font-weight="bold" fill="#6EE7B7">OPTIMAL: 10.59 TOK/S ON PHYSICAL CORES ONLY</text>')

    # Centered VS circle (x=960, y=591)
    lines.append(f'  <circle cx="960" cy="591" r="32" fill="#0B1020" stroke="{COL_MACPRO}" stroke-width="2"/>')
    lines.append(f'  <text x="960" y="599" text-anchor="middle" font-family="{FONT_MONO}" font-size="20" font-weight="bold" fill="{COL_MACPRO}">VS</text>')

    lines.extend(svg_footer("Tested on 12-core Xeon E5-2697 v2 running Qwen 2.5 Coder 7B Q4_K_M Pure CPU (llama.cpp 0f35d6d7b)"))
    return render_svg("11_thread_scaling_12_vs_24", lines)


def chart_12_transparent_huge_pages() -> Path:
    """Simple high-impact graphic: performance improvement from Linux Transparent Huge Pages (THP always)."""
    lines = svg_header(
        "Linux Huge Pages: +60% Faster CPU Inference",
        "Switching Transparent Huge Pages from madvise (4 KB) to always (2 MB) eliminates TLB thrashing",
        "LINUX KERNEL TUNING // TRANSPARENT HUGE PAGES",
    )

    # Left Card: Standard 4 KB Pages (x=80, y=208, w=840, h=766)
    lx, ly, lw, lh = 80, 208, 840, 766
    lines.append(f'  <rect x="{lx}" y="{ly}" width="{lw}" height="{lh}" rx="20" fill="{CARD_BG}" stroke="#475569" stroke-width="2"/>')
    lines.append(f'  <rect x="{lx}" y="{ly}" width="{lw}" height="8" rx="4" fill="#64748B"/>')
    lines.append(f'  <rect x="{lx + 36}" y="{ly + 36}" width="110" height="34" rx="8" fill="#1E293B" stroke="#64748B" stroke-width="1"/>')
    lines.append(f'  <text x="{lx + 91}" y="{ly + 59}" text-anchor="middle" font-family="{FONT_MONO}" font-size="17" font-weight="bold" fill="#94A3B8">4 KB</text>')
    lines.append(f'  <text x="{lx + 164}" y="{ly + 62}" font-family="{FONT_SANS}" font-size="30" font-weight="bold" fill="{TEXT_MAIN}">Standard Pages (THP madvise)</text>')
    lines.append(f'  <text x="{lx + 36}" y="{ly + 104}" font-family="{FONT_SANS}" font-size="20" fill="{TEXT_MUTED}">Linux default memory page size (tiny 4 KB blocks)</text>')

    # Speed display inside Left Card
    lines.append(f'  <rect x="{lx + 36}" y="{ly + 140}" width="{lw - 72}" height="184" rx="16" fill="#0F172A" stroke="#334155" stroke-width="1.5"/>')
    lines.append(f'  <text x="{lx + 64}" y="{ly + 184}" font-family="{FONT_MONO}" font-size="16" font-weight="bold" fill="{TEXT_DIM}">TOKEN GENERATION SPEED (14B Q4_K_M)</text>')
    lines.append(f'  <text x="{lx + 64}" y="{ly + 258}" font-family="{FONT_MONO}" font-size="64" font-weight="bold" fill="{TEXT_MUTED}">3.42 <tspan font-size="26" fill="{TEXT_DIM}">tok/s</tspan></text>')
    lines.append(f'  <text x="{lx + 64}" y="{ly + 298}" font-family="{FONT_MONO}" font-size="18" fill="{TEXT_DIM}">Pure CPU baseline (-ngl 0 -t 12)</text>')

    # Diagram inside Left Card: TLB Cache Thrashing
    lines.append(f'  <rect x="{lx + 36}" y="{ly + 356}" width="{lw - 72}" height="284" rx="16" fill="#0F172A" stroke="#450A0A" stroke-width="1.5"/>')
    lines.append(f'  <text x="{lx + 64}" y="{ly + 398}" font-family="{FONT_MONO}" font-size="17" font-weight="bold" fill="{COL_DANGER}">TLB CACHE THRASHING</text>')

    # Visual memory grid box showing fragmented 4 KB pages
    lines.append(f'  <rect x="{lx + 64}" y="{ly + 424}" width="346" height="176" rx="12" fill="#1E293B" stroke="{COL_DANGER}" stroke-width="1.5"/>')
    lines.append(f'  <text x="{lx + 86}" y="{ly + 458}" font-family="{FONT_MONO}" font-size="15" font-weight="bold" fill="#94A3B8">~8.4 GB MODEL IN RAM</text>')

    # Small grid of tiny 4 KB blocks (2 rows x 6 cols)
    for r in range(2):
        for c in range(6):
            bx = lx + 86 + c * 51
            by = ly + 476 + r * 30
            lines.append(f'  <rect x="{bx}" y="{by}" width="44" height="22" rx="4" fill="#334155" stroke="#64748B" stroke-width="1"/>')
            lines.append(f'  <text x="{bx + 22}" y="{by + 15}" text-anchor="middle" font-family="{FONT_MONO}" font-size="10" fill="{TEXT_MUTED}">4K</text>')

    lines.append(f'  <text x="{lx + 237}" y="{ly + 566}" text-anchor="middle" font-family="{FONT_SANS}" font-size="15" fill="{COL_DANGER}">~2,100,000 tiny pages overflow TLB</text>')

    # Bullet points on right of diagram
    lines.append(f'  <text x="{lx + 436}" y="{ly + 464}" font-family="{FONT_SANS}" font-size="18" fill="{TEXT_MAIN}">• 2.1 million page table lookups</text>')
    lines.append(f'  <text x="{lx + 436}" y="{ly + 514}" font-family="{FONT_SANS}" font-size="18" fill="{TEXT_MAIN}">• Constant TLB cache misses</text>')
    lines.append(f'  <text x="{lx + 436}" y="{ly + 564}" font-family="{FONT_SANS}" font-size="18" fill="{COL_DANGER}">• CPU stalls walking page tables</text>')

    # Left Card Status Pill
    lines.append(f'  <rect x="{lx + 36}" y="{ly + 672}" width="{lw - 72}" height="58" rx="12" fill="#450A0A" stroke="{COL_DANGER}" stroke-width="1.5"/>')
    lines.append(f'  <text x="{lx + lw // 2}" y="{ly + 708}" text-anchor="middle" font-family="{FONT_MONO}" font-size="19" font-weight="bold" fill="#FCA5A5">BOTTLENECK: HEAVY TLB PAGE-WALK OVERHEAD</text>')

    # Right Card: 2 MB Huge Pages (Hero) (x=1000, y=208, w=840, h=766)
    rx, ry, rw, rh = 1000, 208, 840, 766
    lines.append(f'  <rect x="{rx}" y="{ry}" width="{rw}" height="{rh}" rx="20" fill="{CARD_BG}" stroke="{COL_STUDIO}" stroke-width="2.5"/>')
    lines.append(f'  <rect x="{rx}" y="{ry}" width="{rw}" height="8" rx="4" fill="{COL_STUDIO}"/>')
    lines.append(f'  <rect x="{rx + 36}" y="{ry + 36}" width="110" height="34" rx="8" fill="#064E3B" stroke="{COL_STUDIO}" stroke-width="1"/>')
    lines.append(f'  <text x="{rx + 91}" y="{ry + 59}" text-anchor="middle" font-family="{FONT_MONO}" font-size="17" font-weight="bold" fill="#6EE7B7">2 MB</text>')
    lines.append(f'  <text x="{rx + 164}" y="{ry + 62}" font-family="{FONT_SANS}" font-size="30" font-weight="bold" fill="{TEXT_MAIN}">Huge Pages (THP always)</text>')
    lines.append(f'  <text x="{rx + 36}" y="{ry + 104}" font-family="{FONT_SANS}" font-size="20" fill="{COL_STUDIO}">512x larger memory pages (THP always + defrag)</text>')

    # Speed display inside Right Card
    lines.append(f'  <rect x="{rx + 36}" y="{ry + 140}" width="{rw - 72}" height="184" rx="16" fill="#0F172A" stroke="{COL_STUDIO}" stroke-width="1.5"/>')
    lines.append(f'  <text x="{rx + 64}" y="{ry + 184}" font-family="{FONT_MONO}" font-size="16" font-weight="bold" fill="{COL_MACPRO}">TOKEN GENERATION SPEED (14B Q4_K_M)</text>')
    lines.append(f'  <text x="{rx + 64}" y="{ry + 258}" font-family="{FONT_MONO}" font-size="64" font-weight="bold" fill="{TEXT_MAIN}">5.47 <tspan font-size="26" fill="{COL_STUDIO}">tok/s</tspan></text>')
    lines.append(f'  <text x="{rx + 64}" y="{ry + 298}" font-family="{FONT_MONO}" font-size="18" fill="{COL_STUDIO}">Pure CPU + THP always (-ngl 0 -t 12)</text>')

    # Gain badge inside speed display
    lines.append(f'  <rect x="{rx + rw - 248}" y="{ry + 174}" width="184" height="58" rx="12" fill="#064E3B" stroke="{COL_STUDIO}" stroke-width="1.5"/>')
    lines.append(f'  <text x="{rx + rw - 156}" y="{ry + 211}" text-anchor="middle" font-family="{FONT_MONO}" font-size="23" font-weight="bold" fill="#6EE7B7">+60% FASTER</text>')

    # Diagram inside Right Card: TLB Cache Hit Rate Maximized
    lines.append(f'  <rect x="{rx + 36}" y="{ry + 356}" width="{rw - 72}" height="284" rx="16" fill="#0F172A" stroke="#064E3B" stroke-width="1.5"/>')
    lines.append(f'  <text x="{rx + 64}" y="{ry + 398}" font-family="{FONT_MONO}" font-size="17" font-weight="bold" fill="{COL_STUDIO}">TLB CACHE HIT RATE MAXIMIZED</text>')

    # Visual memory box showing large contiguous 2 MB blocks
    lines.append(f'  <rect x="{rx + 64}" y="{ry + 424}" width="346" height="176" rx="12" fill="#1E293B" stroke="{COL_STUDIO}" stroke-width="1.5"/>')
    lines.append(f'  <text x="{rx + 86}" y="{ry + 458}" font-family="{FONT_MONO}" font-size="15" font-weight="bold" fill="#94A3B8">~8.4 GB MODEL IN RAM</text>')

    for c in range(2):
        bx = rx + 86 + c * 156
        lines.append(f'  <rect x="{bx}" y="{ry + 476}" width="146" height="52" rx="8" fill="#064E3B" stroke="{COL_STUDIO}" stroke-width="1.5"/>')
        lines.append(f'  <text x="{bx + 73}" y="{ry + 508}" text-anchor="middle" font-family="{FONT_MONO}" font-size="16" font-weight="bold" fill="#6EE7B7">2 MB Page</text>')

    lines.append(f'  <text x="{rx + 237}" y="{ry + 566}" text-anchor="middle" font-family="{FONT_SANS}" font-size="15" fill="{COL_STUDIO}">~4,200 huge pages fit cleanly in TLB</text>')

    # Bullet points on right of diagram
    lines.append(f'  <text x="{rx + 436}" y="{ry + 464}" font-family="{FONT_SANS}" font-size="18" fill="{TEXT_MAIN}">• 500x fewer page table entries</text>')
    lines.append(f'  <text x="{rx + 436}" y="{ry + 514}" font-family="{FONT_SANS}" font-size="18" fill="{TEXT_MAIN}">• Eliminates TLB cache thrashing</text>')
    lines.append(f'  <text x="{rx + 436}" y="{ry + 564}" font-family="{FONT_SANS}" font-size="18" fill="{COL_STUDIO}">• Full DDR3 memory bandwidth used</text>')

    # Right Card Status Pill
    lines.append(f'  <rect x="{rx + 36}" y="{ry + 672}" width="{rw - 72}" height="58" rx="12" fill="#064E3B" stroke="{COL_STUDIO}" stroke-width="1.5"/>')
    lines.append(f'  <text x="{rx + rw // 2}" y="{ry + 708}" text-anchor="middle" font-family="{FONT_MONO}" font-size="19" font-weight="bold" fill="#6EE7B7">HUGE WIN: 5.47 TOK/S (+60% CPU SPEEDUP)</text>')

    # Centered VS circle (x=960, y=591)
    lines.append(f'  <circle cx="960" cy="591" r="32" fill="#0B1020" stroke="{COL_MACPRO}" stroke-width="2"/>')
    lines.append(f'  <text x="960" y="599" text-anchor="middle" font-family="{FONT_MONO}" font-size="20" font-weight="bold" fill="{COL_MACPRO}">VS</text>')

    lines.extend(svg_footer("Tested on 12-core Xeon E5-2697 v2 running Qwen 2.5 Coder 14B Q4_K_M Pure CPU (llama.cpp 0f35d6d7b)"))
    return render_svg("12_transparent_huge_pages", lines)


def chart_13_flash_attention() -> Path:
    """Simple high-impact graphic: performance improvement from enabling Flash Attention (-fa on) on 1.5B."""
    lines = svg_header(
        "Flash Attention on 2013 GPUs: -fa on",
        "Fusing attention math inside Mesa RADV shaders doubles 1.5B prompt prefill (+109%)",
        "GPU TUNING // FLASH ATTENTION",
    )

    # Left Card: Standard Attention (x=80, y=208, w=840, h=766)
    lx, ly, lw, lh = 80, 208, 840, 766
    lines.append(f'  <rect x="{lx}" y="{ly}" width="{lw}" height="{lh}" rx="20" fill="{CARD_BG}" stroke="#475569" stroke-width="2"/>')
    lines.append(f'  <rect x="{lx}" y="{ly}" width="{lw}" height="8" rx="4" fill="#64748B"/>')
    lines.append(f'  <rect x="{lx + 36}" y="{ly + 36}" width="118" height="34" rx="8" fill="#1E293B" stroke="#64748B" stroke-width="1"/>')
    lines.append(f'  <text x="{lx + 95}" y="{ly + 59}" text-anchor="middle" font-family="{FONT_MONO}" font-size="17" font-weight="bold" fill="#94A3B8">-fa off</text>')
    lines.append(f'  <text x="{lx + 172}" y="{ly + 62}" font-family="{FONT_SANS}" font-size="30" font-weight="bold" fill="{TEXT_MAIN}">Standard Attention</text>')
    lines.append(f'  <text x="{lx + 36}" y="{ly + 104}" font-family="{FONT_SANS}" font-size="20" fill="{TEXT_MUTED}">Unfused attention passes through slow VRAM</text>')

    # Speed display inside Left Card
    lines.append(f'  <rect x="{lx + 36}" y="{ly + 140}" width="{lw - 72}" height="184" rx="16" fill="#0F172A" stroke="#334155" stroke-width="1.5"/>')
    lines.append(f'  <text x="{lx + 64}" y="{ly + 184}" font-family="{FONT_MONO}" font-size="16" font-weight="bold" fill="{TEXT_DIM}">PROMPT PREFILL SPEED (1.5B Q8_0)</text>')
    lines.append(f'  <text x="{lx + 64}" y="{ly + 258}" font-family="{FONT_MONO}" font-size="64" font-weight="bold" fill="{TEXT_MUTED}">187.9 <tspan font-size="26" fill="{TEXT_DIM}">tok/s</tspan></text>')
    lines.append(f'  <text x="{lx + 64}" y="{ly + 298}" font-family="{FONT_MONO}" font-size="18" fill="{TEXT_DIM}">Token generation: 33.5 tok/s</text>')

    # Diagram inside Left Card: Repeated VRAM Round-Trips
    lines.append(f'  <rect x="{lx + 36}" y="{ly + 356}" width="{lw - 72}" height="284" rx="16" fill="#0F172A" stroke="#450A0A" stroke-width="1.5"/>')
    lines.append(f'  <text x="{lx + 64}" y="{ly + 398}" font-family="{FONT_MONO}" font-size="17" font-weight="bold" fill="{COL_DANGER}">REPEATED VRAM ROUND-TRIPS</text>')

    # Visual pipeline box showing unfused steps hitting VRAM
    lines.append(f'  <rect x="{lx + 64}" y="{ly + 424}" width="346" height="176" rx="12" fill="#1E293B" stroke="{COL_DANGER}" stroke-width="1.5"/>')
    lines.append(f'  <text x="{lx + 86}" y="{ly + 458}" font-family="{FONT_MONO}" font-size="15" font-weight="bold" fill="#94A3B8">ATTENTION PIPELINE</text>')

    lines.append(f'  <rect x="{lx + 86}" y="{ly + 478}" width="92" height="44" rx="8" fill="#334155" stroke="#64748B" stroke-width="1"/>')
    lines.append(f'  <text x="{lx + 132}" y="{ly + 505}" text-anchor="middle" font-family="{FONT_MONO}" font-size="14" font-weight="bold" fill="{TEXT_MUTED}">Q x K</text>')

    lines.append(f'  <rect x="{lx + 191}" y="{ly + 478}" width="92" height="44" rx="8" fill="#450A0A" stroke="{COL_DANGER}" stroke-width="1"/>')
    lines.append(f'  <text x="{lx + 237}" y="{ly + 505}" text-anchor="middle" font-family="{FONT_MONO}" font-size="14" font-weight="bold" fill="#FCA5A5">VRAM</text>')

    lines.append(f'  <rect x="{lx + 296}" y="{ly + 478}" width="92" height="44" rx="8" fill="#334155" stroke="#64748B" stroke-width="1"/>')
    lines.append(f'  <text x="{lx + 342}" y="{ly + 505}" text-anchor="middle" font-family="{FONT_MONO}" font-size="14" font-weight="bold" fill="{TEXT_MUTED}">x V</text>')

    lines.append(f'  <text x="{lx + 237}" y="{ly + 566}" text-anchor="middle" font-family="{FONT_SANS}" font-size="15" fill="{COL_DANGER}">Writes &amp; reads huge matrix in VRAM</text>')

    # Bullet points on right of diagram
    lines.append(f'  <text x="{lx + 436}" y="{ly + 464}" font-family="{FONT_SANS}" font-size="18" fill="{TEXT_MAIN}">• Writes attention matrix to VRAM</text>')
    lines.append(f'  <text x="{lx + 436}" y="{ly + 514}" font-family="{FONT_SANS}" font-size="18" fill="{TEXT_MAIN}">• Extra memory bandwidth stalls</text>')
    lines.append(f'  <text x="{lx + 436}" y="{ly + 564}" font-family="{FONT_SANS}" font-size="18" fill="{COL_DANGER}">• Higher VRAM pressure on long prompts</text>')

    # Left Card Status Pill
    lines.append(f'  <rect x="{lx + 36}" y="{ly + 672}" width="{lw - 72}" height="58" rx="12" fill="#450A0A" stroke="{COL_DANGER}" stroke-width="1.5"/>')
    lines.append(f'  <text x="{lx + lw // 2}" y="{ly + 708}" text-anchor="middle" font-family="{FONT_MONO}" font-size="19" font-weight="bold" fill="#FCA5A5">SLOWER: EXTRA VRAM BANDWIDTH OVERHEAD</text>')

    # Right Card: Flash Attention (Hero) (x=1000, y=208, w=840, h=766)
    rx, ry, rw, rh = 1000, 208, 840, 766
    lines.append(f'  <rect x="{rx}" y="{ry}" width="{rw}" height="{rh}" rx="20" fill="{CARD_BG}" stroke="{COL_STUDIO}" stroke-width="2.5"/>')
    lines.append(f'  <rect x="{rx}" y="{ry}" width="{rw}" height="8" rx="4" fill="{COL_STUDIO}"/>')
    lines.append(f'  <rect x="{rx + 36}" y="{ry + 36}" width="118" height="34" rx="8" fill="#064E3B" stroke="{COL_STUDIO}" stroke-width="1"/>')
    lines.append(f'  <text x="{rx + 95}" y="{ry + 59}" text-anchor="middle" font-family="{FONT_MONO}" font-size="17" font-weight="bold" fill="#6EE7B7">-fa on</text>')
    lines.append(f'  <text x="{rx + 172}" y="{ry + 62}" font-family="{FONT_SANS}" font-size="30" font-weight="bold" fill="{TEXT_MAIN}">Flash Attention (Vulkan)</text>')
    lines.append(f'  <text x="{rx + 36}" y="{ry + 104}" font-family="{FONT_SANS}" font-size="20" fill="{COL_STUDIO}">Fused tiled attention inside fast GPU shaders</text>')

    # Speed display inside Right Card
    lines.append(f'  <rect x="{rx + 36}" y="{ry + 140}" width="{rw - 72}" height="184" rx="16" fill="#0F172A" stroke="{COL_STUDIO}" stroke-width="1.5"/>')
    lines.append(f'  <text x="{rx + 64}" y="{ry + 184}" font-family="{FONT_MONO}" font-size="16" font-weight="bold" fill="{COL_MACPRO}">PROMPT PREFILL SPEED (1.5B Q8_0)</text>')
    lines.append(f'  <text x="{rx + 64}" y="{ry + 258}" font-family="{FONT_MONO}" font-size="64" font-weight="bold" fill="{TEXT_MAIN}">392.5 <tspan font-size="26" fill="{COL_STUDIO}">tok/s</tspan></text>')
    lines.append(f'  <text x="{rx + 64}" y="{ry + 298}" font-family="{FONT_MONO}" font-size="18" fill="{COL_STUDIO}">Token generation: 36.6 tok/s (+9.3%)</text>')

    # Gain badge inside speed display
    lines.append(f'  <rect x="{rx + rw - 248}" y="{ry + 174}" width="184" height="58" rx="12" fill="#064E3B" stroke="{COL_STUDIO}" stroke-width="1.5"/>')
    lines.append(f'  <text x="{rx + rw - 156}" y="{ry + 211}" text-anchor="middle" font-family="{FONT_MONO}" font-size="23" font-weight="bold" fill="#6EE7B7">+109% FASTER</text>')

    # Diagram inside Right Card: Fused Tiled Compute
    lines.append(f'  <rect x="{rx + 36}" y="{ry + 356}" width="{rw - 72}" height="284" rx="16" fill="#0F172A" stroke="#064E3B" stroke-width="1.5"/>')
    lines.append(f'  <text x="{rx + 64}" y="{ry + 398}" font-family="{FONT_MONO}" font-size="17" font-weight="bold" fill="{COL_STUDIO}">FUSED TILED COMPUTE</text>')

    # Visual box showing single fused GPU shader pass
    lines.append(f'  <rect x="{rx + 64}" y="{ry + 424}" width="346" height="176" rx="12" fill="#1E293B" stroke="{COL_STUDIO}" stroke-width="1.5"/>')
    lines.append(f'  <text x="{rx + 86}" y="{ry + 458}" font-family="{FONT_MONO}" font-size="15" font-weight="bold" fill="#94A3B8">GPU SHADER TILE (ON-CHIP)</text>')

    lines.append(f'  <rect x="{rx + 86}" y="{ry + 478}" width="302" height="44" rx="8" fill="#064E3B" stroke="{COL_STUDIO}" stroke-width="1.5"/>')
    lines.append(f'  <text x="{rx + 237}" y="{ry + 506}" text-anchor="middle" font-family="{FONT_MONO}" font-size="15" font-weight="bold" fill="#6EE7B7">Q x K -&gt; Softmax -&gt; x V</text>')

    lines.append(f'  <text x="{rx + 237}" y="{ry + 566}" text-anchor="middle" font-family="{FONT_SANS}" font-size="15" fill="{COL_STUDIO}">Single fused pass, zero VRAM round-trips</text>')

    # Bullet points on right of diagram
    lines.append(f'  <text x="{rx + 436}" y="{ry + 464}" font-family="{FONT_SANS}" font-size="18" fill="{TEXT_MAIN}">• Fuses attention into one tiled pass</text>')
    lines.append(f'  <text x="{rx + 436}" y="{ry + 514}" font-family="{FONT_SANS}" font-size="18" fill="{TEXT_MAIN}">• Cuts redundant VRAM reads &amp; writes</text>')
    lines.append(f'  <text x="{rx + 436}" y="{ry + 564}" font-family="{FONT_SANS}" font-size="18" fill="{COL_STUDIO}">• Works on 2013 GCN 1.0 Mesa RADV</text>')

    # Right Card Status Pill
    lines.append(f'  <rect x="{rx + 36}" y="{ry + 672}" width="{rw - 72}" height="58" rx="12" fill="#064E3B" stroke="{COL_STUDIO}" stroke-width="1.5"/>')
    lines.append(f'  <text x="{rx + rw // 2}" y="{ry + 708}" text-anchor="middle" font-family="{FONT_MONO}" font-size="19" font-weight="bold" fill="#6EE7B7">OPTIMAL: 392.5 TOK/S (+109% PROMPT PREFILL)</text>')

    # Centered VS circle (x=960, y=591)
    lines.append(f'  <circle cx="960" cy="591" r="32" fill="#0B1020" stroke="{COL_MACPRO}" stroke-width="2"/>')
    lines.append(f'  <text x="960" y="599" text-anchor="middle" font-family="{FONT_MONO}" font-size="20" font-weight="bold" fill="{COL_MACPRO}">VS</text>')

    lines.extend(svg_footer("Tested on Dual AMD FirePro D500 (Mesa RADV Vulkan) running Qwen 2.5 Coder 1.5B Q8_0 (llama.cpp 0f35d6d7b)"))
    return render_svg("13_flash_attention", lines)


def chart_14_fan_thermal_tuning() -> Path:
    """Simple high-impact graphic: thermal and sustained performance gains from applesmc fan1_min=1300."""
    lines = svg_header(
        "Thermal & Fan Tuning: 790 RPM vs 1300 RPM",
        "Raising the Apple SMC fan floor keeps the unified core at ~70C under 100% load with zero throttling",
        "SYSTEM TUNING // APPLESMC THERMALS",
    )

    # Left Card: Stock Fan Curve (x=80, y=208, w=840, h=766)
    lx, ly, lw, lh = 80, 208, 840, 766
    lines.append(f'  <rect x="{lx}" y="{ly}" width="{lw}" height="{lh}" rx="20" fill="{CARD_BG}" stroke="#475569" stroke-width="2"/>')
    lines.append(f'  <rect x="{lx}" y="{ly}" width="{lw}" height="8" rx="4" fill="#64748B"/>')
    lines.append(f'  <rect x="{lx + 36}" y="{ly + 36}" width="126" height="34" rx="8" fill="#1E293B" stroke="#64748B" stroke-width="1"/>')
    lines.append(f'  <text x="{lx + 99}" y="{ly + 59}" text-anchor="middle" font-family="{FONT_MONO}" font-size="17" font-weight="bold" fill="#94A3B8">790 RPM</text>')
    lines.append(f'  <text x="{lx + 180}" y="{ly + 62}" font-family="{FONT_SANS}" font-size="30" font-weight="bold" fill="{TEXT_MAIN}">Stock Apple Fan Curve</text>')
    lines.append(f'  <text x="{lx + 36}" y="{ly + 104}" font-family="{FONT_SANS}" font-size="20" fill="{TEXT_MUTED}">Prioritizes silence until the unified core gets hot</text>')

    # Temp display inside Left Card
    lines.append(f'  <rect x="{lx + 36}" y="{ly + 140}" width="{lw - 72}" height="184" rx="16" fill="#0F172A" stroke="#334155" stroke-width="1.5"/>')
    lines.append(f'  <text x="{lx + 64}" y="{ly + 184}" font-family="{FONT_MONO}" font-size="16" font-weight="bold" fill="{TEXT_DIM}">LOAD TEMPERATURE THRESHOLD</text>')
    lines.append(f'  <text x="{lx + 64}" y="{ly + 258}" font-family="{FONT_MONO}" font-size="64" font-weight="bold" fill="{TEXT_MUTED}">80+ <tspan font-size="28" fill="{TEXT_DIM}">C</tspan></text>')
    lines.append(f'  <text x="{lx + 64}" y="{ly + 298}" font-family="{FONT_MONO}" font-size="18" fill="{TEXT_DIM}">Default fan1_min: 790 RPM</text>')

    # Diagram inside Left Card: Heat Soak Risk
    lines.append(f'  <rect x="{lx + 36}" y="{ly + 356}" width="{lw - 72}" height="284" rx="16" fill="#0F172A" stroke="#450A0A" stroke-width="1.5"/>')
    lines.append(f'  <text x="{lx + 64}" y="{ly + 398}" font-family="{FONT_MONO}" font-size="17" font-weight="bold" fill="{COL_DANGER}">HEAT SOAK &amp; THROTTLING RISK</text>')

    # Visual thermal bar box
    lines.append(f'  <rect x="{lx + 64}" y="{ly + 424}" width="346" height="176" rx="12" fill="#1E293B" stroke="{COL_DANGER}" stroke-width="1.5"/>')
    lines.append(f'  <text x="{lx + 86}" y="{ly + 458}" font-family="{FONT_MONO}" font-size="15" font-weight="bold" fill="#94A3B8">UNIFIED THERMAL CORE</text>')

    lines.append(f'  <rect x="{lx + 86}" y="{ly + 482}" width="302" height="36" rx="8" fill="#0F172A" stroke="#334155" stroke-width="1"/>')
    lines.append(f'  <rect x="{lx + 86}" y="{ly + 482}" width="268" height="36" rx="8" fill="#7F1D1D" stroke="{COL_DANGER}" stroke-width="1"/>')
    lines.append(f'  <text x="{lx + 237}" y="{ly + 506}" text-anchor="middle" font-family="{FONT_MONO}" font-size="15" font-weight="bold" fill="#FCA5A5">80C+ BEFORE FAN RAMPS</text>')

    lines.append(f'  <text x="{lx + 237}" y="{ly + 566}" text-anchor="middle" font-family="{FONT_SANS}" font-size="15" fill="{COL_DANGER}">Slow reactive ramp under AI load</text>')

    # Bullet points on right of diagram
    lines.append(f'  <text x="{lx + 436}" y="{ly + 464}" font-family="{FONT_SANS}" font-size="18" fill="{TEXT_MAIN}">• Idles near 790 RPM too long</text>')
    lines.append(f'  <text x="{lx + 436}" y="{ly + 514}" font-family="{FONT_SANS}" font-size="18" fill="{TEXT_MAIN}">• Triangular heatsink heat-soaks</text>')
    lines.append(f'  <text x="{lx + 436}" y="{ly + 564}" font-family="{FONT_SANS}" font-size="18" fill="{COL_DANGER}">• Risks clock dips on long runs</text>')

    # Left Card Status Pill
    lines.append(f'  <rect x="{lx + 36}" y="{ly + 672}" width="{lw - 72}" height="58" rx="12" fill="#450A0A" stroke="{COL_DANGER}" stroke-width="1.5"/>')
    lines.append(f'  <text x="{lx + lw // 2}" y="{ly + 708}" text-anchor="middle" font-family="{FONT_MONO}" font-size="19" font-weight="bold" fill="#FCA5A5">REACTIVE: WAITS FOR 80C+ TO RAMP UP</text>')

    # Right Card: Tuned Fan Floor (Hero) (x=1000, y=208, w=840, h=766)
    rx, ry, rw, rh = 1000, 208, 840, 766
    lines.append(f'  <rect x="{rx}" y="{ry}" width="{rw}" height="{rh}" rx="20" fill="{CARD_BG}" stroke="{COL_STUDIO}" stroke-width="2.5"/>')
    lines.append(f'  <rect x="{rx}" y="{ry}" width="{rw}" height="8" rx="4" fill="{COL_STUDIO}"/>')
    lines.append(f'  <rect x="{rx + 36}" y="{ry + 36}" width="134" height="34" rx="8" fill="#064E3B" stroke="{COL_STUDIO}" stroke-width="1"/>')
    lines.append(f'  <text x="{rx + 103}" y="{ry + 59}" text-anchor="middle" font-family="{FONT_MONO}" font-size="17" font-weight="bold" fill="#6EE7B7">1300 RPM</text>')
    lines.append(f'  <text x="{rx + 188}" y="{ry + 62}" font-family="{FONT_SANS}" font-size="30" font-weight="bold" fill="{TEXT_MAIN}">Tuned Fan Floor (applesmc)</text>')
    lines.append(f'  <text x="{rx + 36}" y="{ry + 104}" font-family="{FONT_SANS}" font-size="20" fill="{COL_STUDIO}">Proactive airflow across CPU + Dual D500 GPUs</text>')

    # Temp display inside Right Card
    lines.append(f'  <rect x="{rx + 36}" y="{ry + 140}" width="{rw - 72}" height="184" rx="16" fill="#0F172A" stroke="{COL_STUDIO}" stroke-width="1.5"/>')
    lines.append(f'  <text x="{rx + 64}" y="{ry + 184}" font-family="{FONT_MONO}" font-size="16" font-weight="bold" fill="{COL_MACPRO}">100% ALL-CORE LOAD TEMP</text>')
    lines.append(f'  <text x="{rx + 64}" y="{ry + 258}" font-family="{FONT_MONO}" font-size="64" font-weight="bold" fill="{TEXT_MAIN}">~70 <tspan font-size="28" fill="{COL_STUDIO}">C</tspan></text>')
    lines.append(f'  <text x="{rx + 64}" y="{ry + 298}" font-family="{FONT_MONO}" font-size="18" fill="{COL_STUDIO}">fan1_min = 1300 RPM (whisper-quiet)</text>')

    # Badge inside temp display
    lines.append(f'  <rect x="{rx + rw - 264}" y="{ry + 174}" width="200" height="58" rx="12" fill="#064E3B" stroke="{COL_STUDIO}" stroke-width="1.5"/>')
    lines.append(f'  <text x="{rx + rw - 164}" y="{ry + 211}" text-anchor="middle" font-family="{FONT_MONO}" font-size="22" font-weight="bold" fill="#6EE7B7">NO THROTTLING</text>')

    # Diagram inside Right Card: Proactive Cooling + Full Clocks
    lines.append(f'  <rect x="{rx + 36}" y="{ry + 356}" width="{rw - 72}" height="284" rx="16" fill="#0F172A" stroke="#064E3B" stroke-width="1.5"/>')
    lines.append(f'  <text x="{rx + 64}" y="{ry + 398}" font-family="{FONT_MONO}" font-size="17" font-weight="bold" fill="{COL_STUDIO}">PROACTIVE COOLING + FULL CLOCKS</text>')

    # Visual box showing sysfs command + steady temp
    lines.append(f'  <rect x="{rx + 64}" y="{ry + 424}" width="346" height="176" rx="12" fill="#1E293B" stroke="{COL_STUDIO}" stroke-width="1.5"/>')
    lines.append(f'  <text x="{rx + 86}" y="{ry + 458}" font-family="{FONT_MONO}" font-size="15" font-weight="bold" fill="#94A3B8">APPLESMC.768 SYSFS FLOOR</text>')

    lines.append(f'  <rect x="{rx + 86}" y="{ry + 482}" width="302" height="36" rx="8" fill="#064E3B" stroke="{COL_STUDIO}" stroke-width="1.5"/>')
    lines.append(f'  <text x="{rx + 237}" y="{ry + 506}" text-anchor="middle" font-family="{FONT_MONO}" font-size="15" font-weight="bold" fill="#6EE7B7">echo 1300 &gt; fan1_min</text>')

    lines.append(f'  <text x="{rx + 237}" y="{ry + 566}" text-anchor="middle" font-family="{FONT_SANS}" font-size="15" fill="{COL_STUDIO}">Holds ~70C even at 100% load</text>')

    # Bullet points on right of diagram
    lines.append(f'  <text x="{rx + 436}" y="{ry + 464}" font-family="{FONT_SANS}" font-size="18" fill="{TEXT_MAIN}">• Eliminates thermal throttling</text>')
    lines.append(f'  <text x="{rx + 436}" y="{ry + 514}" font-family="{FONT_SANS}" font-size="18" fill="{TEXT_MAIN}">• Sustains GPU DPM high clocks</text>')
    lines.append(f'  <text x="{rx + 436}" y="{ry + 564}" font-family="{FONT_SANS}" font-size="18" fill="{COL_STUDIO}">• Persisted at boot via systemd</text>')

    # Right Card Status Pill
    lines.append(f'  <rect x="{rx + 36}" y="{ry + 672}" width="{rw - 72}" height="58" rx="12" fill="#064E3B" stroke="{COL_STUDIO}" stroke-width="1.5"/>')
    lines.append(f'  <text x="{rx + rw // 2}" y="{ry + 708}" text-anchor="middle" font-family="{FONT_MONO}" font-size="19" font-weight="bold" fill="#6EE7B7">OPTIMAL: ~70C SUSTAINED + WHISPER QUIET</text>')

    # Centered VS circle (x=960, y=591)
    lines.append(f'  <circle cx="960" cy="591" r="32" fill="#0B1020" stroke="{COL_MACPRO}" stroke-width="2"/>')
    lines.append(f'  <text x="960" y="599" text-anchor="middle" font-family="{FONT_MONO}" font-size="20" font-weight="bold" fill="{COL_MACPRO}">VS</text>')

    lines.extend(svg_footer("Tuned via /sys/devices/platform/applesmc.768/fan1_min=1300 + AMD DPM high on MacPro6,1"))
    return render_svg("14_fan_thermal_tuning", lines)


def chart_15_models_and_usecases() -> Path:
    """Clean 3x2 grid introducing the 6 AI models, full names, and intended use cases (no perf numbers)."""
    lines = svg_header(
        "Meet the Models: Lineup & Use Cases",
        "Six open-weight GGUF models chosen to cover every local AI workflow on the 2013 Mac Pro",
        "MODEL ROSTER // INTENDED USE CASES",
    )

    cards = [
        {
            "badge": "1.5B Q8_0",
            "size": "~1.9 GB",
            "accent": COL_STUDIO,
            "model": "Qwen 2.5 Coder 1.5B Instruct",
            "usecase": "Instant Autocomplete",
            "desc": "Quick code snippets & fast replies",
            "hardware": "Fits 100% in Dual D500 VRAM",
        },
        {
            "badge": "3B Q4_K_M",
            "size": "~2.0 GB",
            "accent": COL_STUDIO,
            "model": "Qwen 2.5 3B Instruct",
            "usecase": "Grammar & Social Copy",
            "desc": "Spellcheck, rewrites & hashtags",
            "hardware": "Fits 100% in Dual D500 VRAM",
        },
        {
            "badge": "7B Q4_K_M",
            "size": "~4.4 GB",
            "accent": COL_MACPRO,
            "model": "Qwen 2.5 Coder 7B Instruct",
            "usecase": "Daily Coding Driver",
            "desc": "Android, Kotlin & Linux scripts",
            "hardware": "Fits 100% in Dual D500 VRAM",
        },
        {
            "badge": "14B Q4_K_M",
            "size": "~8.4 GB",
            "accent": COL_STARFIGHTER,
            "model": "Qwen 2.5 Coder 14B Instruct",
            "usecase": "Deep Reasoning",
            "desc": "Multi-file refactors & debugging",
            "hardware": "Hybrid: Dual D500 + Xeon CPU",
        },
        {
            "badge": "32B Q4_K_M",
            "size": "~18.5 GB",
            "accent": COL_NEO,
            "model": "Qwen 2.5 Coder 32B Instruct",
            "usecase": "Heavyweight Tasks",
            "desc": "Complex coding & architecture",
            "hardware": "Pure CPU in 64 GB ECC RAM",
        },
        {
            "badge": "VISION F16",
            "size": "~3.7 GB",
            "accent": COL_STUDIO,
            "model": "Moondream2 Vision (F16)",
            "usecase": "Image & Alt-Text",
            "desc": "Photo captioning & UI screenshots",
            "hardware": "Fits 100% in Dual D500 VRAM",
        },
    ]

    cw, ch = 566, 368
    gx, gy = 31, 30
    x0, y0 = 80, 208

    for idx, c in enumerate(cards):
        col = idx % 3
        row = idx // 3
        cx = x0 + col * (cw + gx)
        cy = y0 + row * (ch + gy)
        acc = c["accent"]

        lines.append(f'  <rect x="{cx}" y="{cy}" width="{cw}" height="{ch}" rx="20" fill="{CARD_BG}" stroke="{acc}" stroke-width="2"/>')
        lines.append(f'  <rect x="{cx}" y="{cy}" width="{cw}" height="8" rx="4" fill="{acc}"/>')

        # Top row: Model badge + file size
        lines.append(f'  <rect x="{cx + 28}" y="{cy + 30}" width="136" height="34" rx="8" fill="#0F172A" stroke="{acc}" stroke-width="1.5"/>')
        lines.append(f'  <text x="{cx + 96}" y="{cy + 53}" text-anchor="middle" font-family="{FONT_MONO}" font-size="16" font-weight="bold" fill="{acc}">{esc(c["badge"])}</text>')
        lines.append(f'  <text x="{cx + cw - 28}" y="{cy + 53}" text-anchor="end" font-family="{FONT_MONO}" font-size="16" fill="{TEXT_DIM}">{esc(c["size"])}</text>')

        # Full model name
        lines.append(f'  <text x="{cx + 28}" y="{cy + 108}" font-family="{FONT_SANS}" font-size="25" font-weight="bold" fill="{TEXT_MAIN}">{esc(c["model"])}</text>')

        # Intended Use Case box
        lines.append(f'  <rect x="{cx + 28}" y="{cy + 136}" width="{cw - 56}" height="118" rx="12" fill="#0F172A" stroke="#334155" stroke-width="1"/>')
        lines.append(f'  <text x="{cx + 48}" y="{cy + 164}" font-family="{FONT_MONO}" font-size="13" font-weight="bold" fill="{acc}">INTENDED USE CASE</text>')
        lines.append(f'  <text x="{cx + 48}" y="{cy + 200}" font-family="{FONT_SANS}" font-size="24" font-weight="bold" fill="{TEXT_MAIN}">{esc(c["usecase"])}</text>')
        lines.append(f'  <text x="{cx + 48}" y="{cy + 232}" font-family="{FONT_SANS}" font-size="17" fill="{TEXT_MUTED}">{esc(c["desc"])}</text>')

        # Bottom hardware target pill (no performance numbers)
        lines.append(f'  <rect x="{cx + 28}" y="{cy + 278}" width="{cw - 56}" height="56" rx="12" fill="#0F172A" stroke="{acc}" stroke-width="1.5"/>')
        lines.append(f'  <text x="{cx + cw // 2}" y="{cy + 313}" text-anchor="middle" font-family="{FONT_MONO}" font-size="17" font-weight="bold" fill="{acc}">{esc(c["hardware"])}</text>')

    lines.extend(svg_footer("6 GGUF models sized for 6 GB Dual FirePro D500 VRAM + 64 GB Quad-Channel ECC RAM"))
    return render_svg("15_models_and_usecases", lines)


def chart_16_14b_hybrid_split() -> Path:
    """Visual breakdown of how 14B Q4_K_M (~8.4 GB) is optimized with a 24/48 Hybrid GPU+CPU split."""
    lines = svg_header(
        "Optimizing 14B: Hybrid GPU + CPU Split",
        "Splitting 48 layers across Dual D500 VRAM and Xeon ECC RAM boosts 14B speed +87% over stock CPU",
        "HYBRID OFFLOAD // 14B OPTIMIZATION",
    )

    # Left Card: Speed Progression (x=80, y=208, w=840, h=766)
    lx, ly, lw, lh = 80, 208, 840, 766
    lines.append(f'  <rect x="{lx}" y="{ly}" width="{lw}" height="{lh}" rx="20" fill="{CARD_BG}" stroke="#475569" stroke-width="2"/>')
    lines.append(f'  <rect x="{lx}" y="{ly}" width="{lw}" height="8" rx="4" fill="{COL_MACPRO}"/>')
    lines.append(f'  <rect x="{lx + 36}" y="{ly + 36}" width="132" height="34" rx="8" fill="#1E293B" stroke="{COL_MACPRO}" stroke-width="1"/>')
    lines.append(f'  <text x="{lx + 102}" y="{ly + 59}" text-anchor="middle" font-family="{FONT_MONO}" font-size="16" font-weight="bold" fill="{COL_MACPRO}">~8.4 GB</text>')
    lines.append(f'  <text x="{lx + 186}" y="{ly + 62}" font-family="{FONT_SANS}" font-size="30" font-weight="bold" fill="{TEXT_MAIN}">14B Optimization Path</text>')
    lines.append(f'  <text x="{lx + 36}" y="{ly + 104}" font-family="{FONT_SANS}" font-size="20" fill="{TEXT_MUTED}">Too big for 6 GB VRAM alone, so every layer counts</text>')

    steps = [
        ("1. STOCK CPU BASELINE", "Pure CPU (-ngl 0, THP madvise)", "3.42", "tok/s", "#64748B", "#1E293B", "Baseline"),
        ("2. + HUGE PAGES & -t 12", "Pure CPU (-ngl 0, THP always)", "5.47", "tok/s", COL_STARFIGHTER, "#0F172A", "+60%"),
        ("3. + HYBRID GPU/CPU SPLIT", "24/48 layers on Dual D500 (-fa on)", "6.40", "tok/s", COL_STUDIO, "#064E3B", "+87%"),
    ]

    sy = ly + 144
    for title_s, sub_s, val_s, unit_s, col_s, badge_bg, delta_s in steps:
        lines.append(f'  <rect x="{lx + 36}" y="{sy}" width="{lw - 72}" height="150" rx="14" fill="#0F172A" stroke="{col_s}" stroke-width="1.5"/>')
        lines.append(f'  <text x="{lx + 64}" y="{sy + 40}" font-family="{FONT_MONO}" font-size="15" font-weight="bold" fill="{col_s}">{esc(title_s)}</text>')
        lines.append(f'  <text x="{lx + 64}" y="{sy + 74}" font-family="{FONT_SANS}" font-size="19" fill="{TEXT_MUTED}">{esc(sub_s)}</text>')
        lines.append(f'  <text x="{lx + 64}" y="{sy + 124}" font-family="{FONT_MONO}" font-size="42" font-weight="bold" fill="{TEXT_MAIN}">{esc(val_s)} <tspan font-size="20" fill="{col_s}">{esc(unit_s)}</tspan></text>')

        # Right delta pill
        lines.append(f'  <rect x="{lx + lw - 210}" y="{sy + 48}" width="146" height="52" rx="10" fill="{badge_bg}" stroke="{col_s}" stroke-width="1.5"/>')
        lines.append(f'  <text x="{lx + lw - 137}" y="{sy + 81}" text-anchor="middle" font-family="{FONT_MONO}" font-size="20" font-weight="bold" fill="{col_s}">{esc(delta_s)}</text>')
        sy += 174

    # Left Card Bottom Status Pill
    lines.append(f'  <rect x="{lx + 36}" y="{ly + 672}" width="{lw - 72}" height="58" rx="12" fill="#422006" stroke="{COL_MACPRO}" stroke-width="1.5"/>')
    lines.append(f'  <text x="{lx + lw // 2}" y="{ly + 708}" text-anchor="middle" font-family="{FONT_MONO}" font-size="19" font-weight="bold" fill="{COL_MACPRO}">RESULT: +87% FASTER THAN STOCK CPU</text>')

    # Right Card: 3-Way Hardware Split Architecture (x=1000, y=208, w=840, h=766)
    rx, ry, rw, rh = 1000, 208, 840, 766
    lines.append(f'  <rect x="{rx}" y="{ry}" width="{rw}" height="{rh}" rx="20" fill="{CARD_BG}" stroke="{COL_STUDIO}" stroke-width="2.5"/>')
    lines.append(f'  <rect x="{rx}" y="{ry}" width="{rw}" height="8" rx="4" fill="{COL_STUDIO}"/>')
    lines.append(f'  <rect x="{rx + 36}" y="{ry + 36}" width="126" height="34" rx="8" fill="#064E3B" stroke="{COL_STUDIO}" stroke-width="1"/>')
    lines.append(f'  <text x="{rx + 99}" y="{ry + 59}" text-anchor="middle" font-family="{FONT_MONO}" font-size="17" font-weight="bold" fill="#6EE7B7">-ngl 24</text>')
    lines.append(f'  <text x="{rx + 180}" y="{ry + 62}" font-family="{FONT_SANS}" font-size="30" font-weight="bold" fill="{TEXT_MAIN}">Balanced 3-Way Layer Split</text>')
    lines.append(f'  <text x="{rx + 36}" y="{ry + 104}" font-family="{FONT_SANS}" font-size="20" fill="{COL_STUDIO}">48 transformer layers split via -sm layer -ts 1,1</text>')

    tiers = [
        ("GPU 0: FIREPRO D500 (3 GB VRAM)", "12 Layers (L0..L11)", "Vulkan0 + Flash Attention (-fa on)", COL_STUDIO, "#064E3B"),
        ("GPU 1: FIREPRO D500 (3 GB VRAM)", "12 Layers (L12..L23)", "Vulkan1 + Flash Attention (-fa on)", COL_STUDIO, "#064E3B"),
        ("CPU: 12-CORE XEON (64 GB ECC RAM)", "24 Layers (L24..L47)", "Physical Cores (-t 12) + THP Huge Pages", COL_STARFIGHTER, "#0F172A"),
    ]

    ty = ry + 144
    for hw_label, layer_badge, detail_label, t_col, t_bg in tiers:
        lines.append(f'  <rect x="{rx + 36}" y="{ty}" width="{rw - 72}" height="150" rx="14" fill="#0F172A" stroke="{t_col}" stroke-width="1.5"/>')
        lines.append(f'  <text x="{rx + 64}" y="{ty + 42}" font-family="{FONT_MONO}" font-size="16" font-weight="bold" fill="{t_col}">{esc(hw_label)}</text>')
        lines.append(f'  <text x="{rx + 64}" y="{ty + 84}" font-family="{FONT_SANS}" font-size="26" font-weight="bold" fill="{TEXT_MAIN}">{esc(layer_badge)}</text>')
        lines.append(f'  <text x="{rx + 64}" y="{ty + 122}" font-family="{FONT_SANS}" font-size="18" fill="{TEXT_MUTED}">{esc(detail_label)}</text>')

        # Visual layer bar on right
        lines.append(f'  <rect x="{rx + rw - 236}" y="{ty + 48}" width="172" height="52" rx="10" fill="{t_bg}" stroke="{t_col}" stroke-width="1.5"/>')
        pct_text = "25% WEIGHTS" if "12 Layers" in layer_badge else "50% WEIGHTS"
        lines.append(f'  <text x="{rx + rw - 150}" y="{ty + 81}" text-anchor="middle" font-family="{FONT_MONO}" font-size="17" font-weight="bold" fill="{t_col}">{pct_text}</text>')
        ty += 174

    # Right Card Bottom Status Pill
    lines.append(f'  <rect x="{rx + 36}" y="{ry + 672}" width="{rw - 72}" height="58" rx="12" fill="#064E3B" stroke="{COL_STUDIO}" stroke-width="1.5"/>')
    lines.append(f'  <text x="{rx + rw // 2}" y="{ry + 708}" text-anchor="middle" font-family="{FONT_MONO}" font-size="19" font-weight="bold" fill="#6EE7B7">HYBRID: 27.6 TOK/S PREFILL | 6.40 TOK/S GEN</text>')

    lines.extend(svg_footer("Qwen 2.5 Coder 14B Q4_K_M on MacPro6,1 (llama.cpp 0f35d6d7b, preset [trash-deep])"))
    return render_svg("16_14b_hybrid_split", lines)


def chart_17_individual_model_perf() -> list[Path]:
    """Generate one dedicated performance graphic per model on the 2013 Mac Pro."""
    models = [
        dict(
            filename="17a_model_1.5b_perf",
            eyebrow="MODEL BENCHMARK // 1.5B (TRASH-FAST)",
            title="Qwen 2.5 Coder 1.5B Instruct (Q8_0)",
            subtitle="Instant autocomplete & quick code snippets running 100% in Dual FirePro D500 VRAM",
            accent=COL_STUDIO,
            left_label="PROMPT PREFILL (pp512)",
            left_value="392.5",
            left_unit="tok/s",
            left_note="Ingests 512-token code context in ~1.3 seconds",
            right_label="TOKEN GENERATION (tg128)",
            right_value="36.6",
            right_unit="tok/s",
            right_note="Faster than reading speed for instant inline replies",
            target_val="Dual FirePro D500 (Vulkan)",
            size_val="~1.89 GB (100% VRAM)",
            flags_val="-ngl 99 -ts 1,1 -fa on",
            footer_text="MacPro6,1 standardized benchmark (-p 512 -n 128 -r 3) on llama.cpp 0f35d6d7b",
        ),
        dict(
            filename="17b_model_3b_perf",
            eyebrow="MODEL BENCHMARK // 3B (TRASH-SOCIAL)",
            title="Qwen 2.5 3B Instruct (Q4_K_M)",
            subtitle="Grammar checks, rewrites & social copy running 100% in Dual FirePro D500 VRAM",
            accent=COL_STUDIO,
            left_label="PROMPT PREFILL (pp512)",
            left_value="178.3",
            left_unit="tok/s",
            left_note="Fast prompt ingestion across both Tahiti GPUs",
            right_label="TOKEN GENERATION (tg128)",
            right_value="22.1",
            right_unit="tok/s",
            right_note="Snappy conversational writing & text cleanup",
            target_val="Dual FirePro D500 (Vulkan)",
            size_val="~1.95 GiB (100% VRAM)",
            flags_val="-ngl 99 -ts 1,1 -fa on",
            footer_text="MacPro6,1 standardized benchmark (-p 512 -n 128 -r 3) on llama.cpp 0f35d6d7b",
        ),
        dict(
            filename="17c_model_7b_perf",
            eyebrow="MODEL BENCHMARK // 7B (TRASH-CODE)",
            title="Qwen 2.5 Coder 7B Instruct (Q4_K_M)",
            subtitle="Daily Android, Kotlin & Linux coding driver fitting all 28 layers across Dual D500 GPUs",
            accent=COL_MACPRO,
            left_label="PROMPT PREFILL (pp512)",
            left_value="74.4",
            left_unit="tok/s",
            left_note="Steady prompt processing with zero CPU spillover",
            right_label="TOKEN GENERATION (tg128)",
            right_value="13.0",
            right_unit="tok/s",
            right_note="Comfortable daily-driver speed on 12-year-old GPUs",
            target_val="Dual D500 (28/28 Layers)",
            size_val="~4.36 GiB (100% VRAM)",
            flags_val="-ngl 28 -ts 1,1 -fa on",
            footer_text="MacPro6,1 standardized benchmark (-p 512 -n 128 -r 3) on llama.cpp 0f35d6d7b",
        ),
        dict(
            filename="17d_model_14b_perf",
            eyebrow="MODEL BENCHMARK // 14B (TRASH-DEEP)",
            title="Qwen 2.5 Coder 14B Instruct (Q4_K_M)",
            subtitle="Deep reasoning & multi-file refactors using a 24/48 Hybrid GPU + Xeon CPU split",
            accent=COL_STARFIGHTER,
            left_label="PROMPT PREFILL (pp512)",
            left_value="27.6",
            left_unit="tok/s",
            left_note="24 layers GPU-accelerated + 24 layers on Xeon THP",
            right_label="TOKEN GENERATION (tg128)",
            right_value="6.40",
            right_unit="tok/s",
            right_note="+87% faster than unoptimized Pure CPU baseline (3.42)",
            target_val="Hybrid: Dual D500 + Xeon",
            size_val="~8.4 GB (24/48 GPU Layers)",
            flags_val="-ngl 24 -t 12 -fa on (THP)",
            footer_text="MacPro6,1 standardized benchmark (-p 512 -n 128 -r 3) on llama.cpp 0f35d6d7b",
        ),
        dict(
            filename="17e_model_32b_perf",
            eyebrow="MODEL BENCHMARK // 32B (TRASH-HEAVY)",
            title="Qwen 2.5 Coder 32B Instruct (Q4_K_M)",
            subtitle="Heavyweight coding running Pure CPU in 64 GB Quad-Channel ECC RAM (zero PCIe bottleneck)",
            accent=COL_NEO,
            left_label="PROMPT PREFILL (pp512)",
            left_value="9.06",
            left_unit="tok/s",
            left_note="Beats hybrid offload (3.84) by avoiding PCIe bounce",
            right_label="TOKEN GENERATION (tg128)",
            right_value="2.53",
            right_unit="tok/s",
            right_note="Runs reliably where 16 GB modern laptops OOM crash",
            target_val="12-Core Xeon (Pure CPU)",
            size_val="~18.5 GB (64 GB ECC RAM)",
            flags_val="-ngl 0 -t 12 (THP always)",
            footer_text="MacPro6,1 standardized benchmark (-p 512 -n 128 -r 3) on llama.cpp 0f35d6d7b",
        ),
        dict(
            filename="17f_model_moondream2_perf",
            eyebrow="MODEL BENCHMARK // VISION (TRASH-VISION)",
            title="Moondream2 Vision (F16)",
            subtitle="Multimodal image captioning & alt-text generation running 100% on Dual FirePro D500 GPUs",
            accent=COL_STUDIO,
            left_label="IMAGE ENCODE (ViT)",
            left_value="1.75",
            left_unit="seconds",
            left_note="1,749 ms on 2939x2499 IDE screenshot | 1,753 ms photo",
            right_label="END-TO-END ALT-TEXT",
            right_value="7.8s",
            right_unit="to 8.2s total",
            right_note="7.8s IDE screenshot | 8.2s park photo full description",
            target_val="Dual FirePro D500 (Vulkan)",
            size_val="~3.7 GB (Text + mmproj)",
            flags_val="-ngl 99 -ts 1,1 (vicuna)",
            footer_text="MacPro6,1 Moondream2 multimodal benchmark (llama-mtmd-cli, llama.cpp 0f35d6d7b)",
        ),
    ]
    return [gg.render_single_perf_slide(OUT_DIR, brand=BRAND, **m) for m in models]


def chart_18_trashcan_vs_starfighter() -> Path:
    """Head-to-head comparison: 2013 Mac Pro vs StarLabs StarFighter Ultra 5 across 4 model sizes."""
    rows = [
        {
            "size": "1.5B Q8_0",
            "sub": "Autocomplete",
            "gen_mac": 36.6, "gen_opp": 21.2, "gen_win": "mac",
            "pp_mac": 392.5, "pp_opp": 597.8, "pp_win": "opp",
            "verdict": "Mac Pro +72% Gen",
            "v_col": COL_MACPRO,
        },
        {
            "size": "7B Q4_K_M",
            "sub": "Daily Coding",
            "gen_mac": 13.0, "gen_opp": 11.7, "gen_win": "mac",
            "pp_mac": 74.4, "pp_opp": 188.3, "pp_win": "opp",
            "verdict": "Mac Pro +11% Gen",
            "v_col": COL_MACPRO,
        },
        {
            "size": "14B Q4_K_M",
            "sub": "Deep Reasoning",
            "gen_mac": 6.40, "gen_opp": 6.30, "gen_win": "mac",
            "pp_mac": 27.6, "pp_opp": 95.0, "pp_win": "opp",
            "verdict": "Mac Pro Gen / SF 3.4x PP",
            "v_col": COL_MACPRO,
        },
        {
            "size": "32B Q4_K_M",
            "sub": "Heavyweight",
            "gen_mac": 2.53, "gen_opp": 2.85, "gen_win": "opp",
            "pp_mac": 9.06, "pp_opp": 41.6, "pp_win": "opp",
            "verdict": "StarFighter +13% Gen",
            "v_col": COL_STARFIGHTER,
        },
    ]
    return gg.render_vs_machine_table(OUT_DIR, brand=BRAND, 
        filename="18_trashcan_vs_starfighter",
        eyebrow="HEAD-TO-HEAD // MAC PRO 2013 VS STARFIGHTER",
        title="2013 Trash Can vs. StarLabs StarFighter Ultra 5",
        subtitle="Mac Pro wins token generation on 1.5B, 7B & 14B via GDDR5; StarFighter sweeps prompt prefill (1.5x to 4.6x)",
        mac_legend="Mac Pro 2013 (Dual D500)",
        opp_legend="StarFighter (Intel Arc)",
        opp_tag="STARFIGHTER",
        opp_color=COL_STARFIGHTER,
        opp_bg="#082F49",
        rows=rows,
        footer_text="Mac Pro (Dual FirePro D500 + Xeon E5-2697 v2) vs StarLabs StarFighter Ultra 5 (Intel Arc, CachyOS 28W)",
    )


def chart_19_trashcan_vs_starfighter_cpu_8t() -> Path:
    """Normalized CPU-only (-ngl 0 -t 8) comparison: 2013 Mac Pro vs StarFighter Ultra 5."""
    rows = [
        {
            "size": "1.5B Q8_0",
            "sub": "Autocomplete",
            "gen_mac": 27.1, "gen_opp": 21.3, "gen_win": "mac",
            "pp_mac": 332.8, "pp_opp": 97.1, "pp_win": "mac",
            "verdict": "Mac Pro +27% / 3.4x PP",
            "v_col": COL_MACPRO,
        },
        {
            "size": "7B Q4_K_M",
            "sub": "Daily Coding",
            "gen_mac": 8.94, "gen_opp": 7.61, "gen_win": "mac",
            "pp_mac": 59.5, "pp_opp": 32.8, "pp_win": "mac",
            "verdict": "Mac Pro +17% / +81% PP",
            "v_col": COL_MACPRO,
        },
        {
            "size": "14B Q4_K_M",
            "sub": "Deep Reasoning",
            "gen_mac": 4.66, "gen_opp": 3.88, "gen_win": "mac",
            "pp_mac": 22.8, "pp_opp": 16.3, "pp_win": "mac",
            "verdict": "Mac Pro +20% / +40% PP",
            "v_col": COL_MACPRO,
        },
        {
            "size": "32B Q4_K_M",
            "sub": "Heavyweight",
            "gen_mac": 2.08, "gen_opp": 1.77, "gen_win": "mac",
            "pp_mac": 9.05, "pp_opp": 6.94, "pp_win": "mac",
            "verdict": "Mac Pro +18% / +30% PP",
            "v_col": COL_MACPRO,
        },
    ]
    return gg.render_vs_machine_table(OUT_DIR, brand=BRAND, 
        filename="19_trashcan_vs_starfighter_cpu_8t",
        eyebrow="PURE CPU NORMALIZED // -NGL 0 -T 8",
        title="Pure CPU (-t 8): Trash Can vs. StarFighter",
        subtitle="Quad-channel ECC DDR3 lets the 2013 Xeon sweep StarFighter on every model at 8 threads",
        mac_legend="Mac Pro 2013 (Xeon -t 8)",
        opp_legend="StarFighter (Ultra 5 -t 8)",
        opp_tag="STARFIGHTER",
        opp_color=COL_STARFIGHTER,
        opp_bg="#082F49",
        rows=rows,
        footer_text="Normalized CPU-only (-ngl 0 -t 8); StarFighter uses -dev none --no-host 1 to avoid i915.gem uncached slowdowns",
    )


def chart_20_trashcan_vs_macbook_neo() -> Path:
    """Head-to-head comparison: 2013 Mac Pro vs MacBook Neo (Apple A18 Pro, 8 GB Unified)."""
    rows = [
        {
            "size": "1.5B Q8_0",
            "sub": "Autocomplete",
            "gen_mac": 36.6, "gen_opp": 31.9, "gen_win": "mac",
            "pp_mac": 392.5, "pp_opp": 493.5, "pp_win": "opp",
            "verdict": "Mac Pro +15% Gen",
            "v_col": COL_MACPRO,
        },
        {
            "size": "7B Q4_K_M",
            "sub": "Daily Coding",
            "gen_mac": 13.0, "gen_opp": 11.7, "gen_win": "mac",
            "pp_mac": 74.4, "pp_opp": 96.6, "pp_win": "opp",
            "verdict": "Mac Pro +11% Gen",
            "v_col": COL_MACPRO,
        },
        {
            "size": "14B Q4_K_M",
            "sub": "Deep Reasoning",
            "gen_mac": 6.40, "gen_opp": None, "gen_win": "mac",
            "pp_mac": 27.6, "pp_opp": None, "pp_win": "mac",
            "verdict": "Mac Pro Wins (Neo OOM)",
            "v_col": COL_MACPRO,
        },
        {
            "size": "32B Q4_K_M",
            "sub": "Heavyweight",
            "gen_mac": 2.53, "gen_opp": None, "gen_win": "mac",
            "pp_mac": 9.06, "pp_opp": None, "pp_win": "mac",
            "verdict": "Mac Pro Wins (Neo OOM)",
            "v_col": COL_MACPRO,
        },
    ]
    return gg.render_vs_machine_table(OUT_DIR, brand=BRAND, 
        filename="20_trashcan_vs_macbook_neo",
        eyebrow="HEAD-TO-HEAD // MAC PRO 2013 VS MACBOOK NEO",
        title="2013 Trash Can vs. MacBook Neo (A18 Pro)",
        subtitle="Mac Pro beats Neo on 1.5B & 7B token generation, and runs 14B & 32B where 8 GB Neo crashes OOM",
        mac_legend="Mac Pro 2013 (Dual D500)",
        opp_legend="MacBook Neo (A18 Pro 8 GB)",
        opp_tag="MACBOOK NEO",
        opp_color=COL_NEO,
        opp_bg="#2E1065",
        rows=rows,
        footer_text="Mac Pro (Dual FirePro D500 + 64 GB ECC) vs MacBook Neo (Apple A18 Pro Metal, 8 GB RAM / 5.33 GiB cap)",
    )


def chart_21_trashcan_vs_macbook_neo_cpu() -> Path:
    """Pure CPU-only comparison: 2013 Mac Pro (-t 8) vs MacBook Neo (-t 6 max)."""
    rows = [
        {
            "size": "1.5B Q8_0",
            "sub": "Autocomplete",
            "gen_mac": 27.1, "gen_opp": 28.6, "gen_win": "opp",
            "pp_mac": 332.8, "pp_opp": 228.5, "pp_win": "mac",
            "verdict": "Neo +6% Gen / Mac +46% PP",
            "v_col": COL_MACPRO,
        },
        {
            "size": "7B Q4_K_M",
            "sub": "Daily Coding",
            "gen_mac": 8.94, "gen_opp": 9.60, "gen_win": "opp",
            "pp_mac": 59.5, "pp_opp": 38.3, "pp_win": "mac",
            "verdict": "Neo +7% Gen / Mac +55% PP",
            "v_col": COL_MACPRO,
        },
        {
            "size": "14B Q4_K_M",
            "sub": "Deep Reasoning",
            "gen_mac": 4.66, "gen_opp": None, "gen_win": "mac",
            "pp_mac": 22.8, "pp_opp": None, "pp_win": "mac",
            "verdict": "Mac Pro Wins (Neo OOM)",
            "v_col": COL_MACPRO,
        },
        {
            "size": "32B Q4_K_M",
            "sub": "Heavyweight",
            "gen_mac": 2.08, "gen_opp": None, "gen_win": "mac",
            "pp_mac": 9.05, "pp_opp": None, "pp_win": "mac",
            "verdict": "Mac Pro Wins (Neo OOM)",
            "v_col": COL_MACPRO,
        },
    ]
    return gg.render_vs_machine_table(OUT_DIR, brand=BRAND, 
        filename="21_trashcan_vs_macbook_neo_cpu",
        eyebrow="PURE CPU // MAC PRO (-T 8) VS MACBOOK NEO (-T 6)",
        title="Pure CPU: Trash Can vs. MacBook Neo",
        subtitle="Neo edges 1.5B & 7B gen, while Xeon sweeps prompt prefill (+46% to +55%) and runs 14B & 32B",
        mac_legend="Mac Pro 2013 (Xeon -t 8)",
        opp_legend="MacBook Neo (A18 Pro -t 6)",
        opp_tag="MACBOOK NEO",
        opp_color=COL_NEO,
        opp_bg="#2E1065",
        rows=rows,
        footer_text="Pure CPU (-ngl 0): Mac Pro Xeon (-t 8, 64 GB ECC) vs MacBook Neo A18 Pro (-t 6 max, 8 GB RAM)",
    )


def chart_22_vision_neo_starfighter_trashcan() -> Path:
    """3-way Moondream2 Vision comparison: MacBook Neo vs 2013 Mac Pro vs StarFighter Ultra 5."""
    cards = [
        {
            "rank": "#1 FASTEST",
            "title": "MacBook Neo",
            "sub": "Apple A18 Pro (Metal)",
            "accent": COL_NEO,
            "pill_bg": "#2E1065",
            "vit_val": "0.65s",
            "vit_sub": "659 ms IDE | 650 ms Photo",
            "e2e_ide": "4.27s",
            "e2e_photo": "6.90s",
            "verdict": "WINNER: FASTEST ENCODE + CAPTION",
        },
        {
            "rank": "#2 TOTAL TIME",
            "title": "2013 Mac Pro",
            "sub": "Dual FirePro D500 (Vulkan)",
            "accent": COL_MACPRO,
            "pill_bg": "#422006",
            "vit_val": "1.75s",
            "vit_sub": "1,749 ms IDE | 1,753 ms Photo",
            "e2e_ide": "7.80s",
            "e2e_photo": "8.20s",
            "verdict": "BEATS STARFIGHTER ON TOTAL TIME",
        },
        {
            "rank": "#3 TOTAL TIME",
            "title": "StarFighter Ultra 5",
            "sub": "Intel Arc iGPU (Vulkan ANV)",
            "accent": COL_STARFIGHTER,
            "pill_bg": "#082F49",
            "vit_val": "1.61s",
            "vit_sub": "1,607 ms IDE | 1,628 ms Photo",
            "e2e_ide": "10.36s",
            "e2e_photo": "11.30s",
            "verdict": "SLOWER END-TO-END TEXT OUTPUT",
        },
    ]
    return gg.render_vision_cards(OUT_DIR, brand=BRAND, 
        filename="22_vision_neo_starfighter_trashcan",
        eyebrow="MULTIMODAL VISION // MOONDREAM2 F16",
        title="Vision AI (Moondream2): Neo vs. Mac Pro vs. StarFighter",
        subtitle="MacBook Neo leads overall, while the 2013 Trash Can finishes alt-text faster than the StarFighter",
        cards=cards,
        footer_text="Moondream2 F16 (2.7G text + 868M mmproj) via llama-mtmd-cli (lower seconds = faster)",
    )


def chart_24_vision_all_4_machines() -> Path:
    """4-way Moondream2 Vision comparison: M4 Max Studio vs MacBook Neo vs 2013 Mac Pro vs StarFighter."""
    cards = [
        {
            "rank": "#1 FASTEST",
            "title": "M4 Max Studio",
            "sub": "32-Core GPU (Metal 4)",
            "accent": COL_STUDIO,
            "pill_bg": "#064E3B",
            "vit_val": "0.10s",
            "vit_sub": "100 ms IDE | 99 ms Photo",
            "e2e_ide": "0.97s",
            "e2e_photo": "1.27s",
            "verdict": "17.5x FASTER ENCODE",
        },
        {
            "rank": "#2 FASTEST",
            "title": "MacBook Neo",
            "sub": "Apple A18 Pro (Metal)",
            "accent": COL_NEO,
            "pill_bg": "#2E1065",
            "vit_val": "0.65s",
            "vit_sub": "659 ms IDE | 650 ms Photo",
            "e2e_ide": "4.27s",
            "e2e_photo": "6.90s",
            "verdict": "SUB-SECOND ENCODE",
        },
        {
            "rank": "#3 TOTAL TIME",
            "title": "2013 Mac Pro",
            "sub": "Dual FirePro D500 (Vulkan)",
            "accent": COL_MACPRO,
            "pill_bg": "#422006",
            "vit_val": "1.75s",
            "vit_sub": "1,749 ms IDE | 1,753 ms Photo",
            "e2e_ide": "7.80s",
            "e2e_photo": "8.20s",
            "verdict": "BEATS STARFIGHTER",
        },
        {
            "rank": "#4 TOTAL TIME",
            "title": "StarFighter",
            "sub": "Intel Arc iGPU (Vulkan ANV)",
            "accent": COL_STARFIGHTER,
            "pill_bg": "#082F49",
            "vit_val": "1.61s",
            "vit_sub": "1,607 ms IDE | 1,628 ms Photo",
            "e2e_ide": "10.36s",
            "e2e_photo": "11.30s",
            "verdict": "SLOWER TEXT OUTPUT",
        },
    ]
    return gg.render_vision_cards(OUT_DIR, brand=BRAND, 
        filename="24_vision_all_4_machines",
        eyebrow="MULTIMODAL VISION // ALL 4 MACHINES",
        title="Vision AI (Moondream2): All 4 Machines",
        subtitle="M4 Max hits sub-second total latency, while the 2013 Trash Can still beats the StarFighter",
        cards=cards,
        footer_text="Moondream2 F16 (2.7G text + 868M mmproj) via llama-mtmd-cli (lower seconds = faster)",
    )


def chart_23_trashcan_vs_mac_studio() -> Path:
    """Head-to-head comparison: 2013 Mac Pro vs M4 Max Mac Studio across 4 model sizes."""
    rows = [
        {
            "size": "1.5B Q8_0",
            "sub": "Autocomplete",
            "gen_mac": 36.6, "gen_opp": 164.9, "gen_win": "opp",
            "pp_mac": 392.5, "pp_opp": 3569.7, "pp_win": "opp",
            "verdict": "M4 Max 4.5x Gen / 9.1x PP",
            "v_col": COL_STUDIO,
        },
        {
            "size": "7B Q4_K_M",
            "sub": "Daily Coding",
            "gen_mac": 13.0, "gen_opp": 70.0, "gen_win": "opp",
            "pp_mac": 74.4, "pp_opp": 726.4, "pp_win": "opp",
            "verdict": "M4 Max 5.4x Gen / 9.8x PP",
            "v_col": COL_STUDIO,
        },
        {
            "size": "14B Q4_K_M",
            "sub": "Deep Reasoning",
            "gen_mac": 6.40, "gen_opp": 38.6, "gen_win": "opp",
            "pp_mac": 27.6, "pp_opp": 385.5, "pp_win": "opp",
            "verdict": "M4 Max 6.0x Gen / 14x PP",
            "v_col": COL_STUDIO,
        },
        {
            "size": "32B Q4_K_M",
            "sub": "Heavyweight",
            "gen_mac": 2.53, "gen_opp": 18.1, "gen_win": "opp",
            "pp_mac": 9.06, "pp_opp": 165.1, "pp_win": "opp",
            "verdict": "M4 Max 7.2x Gen / 18x PP",
            "v_col": COL_STUDIO,
        },
    ]
    return gg.render_vs_machine_table(OUT_DIR, brand=BRAND, 
        filename="23_trashcan_vs_mac_studio",
        eyebrow="12 YEARS OF SILICON // MAC PRO 2013 VS M4 MAX STUDIO",
        title="2013 Trash Can vs. M4 Max Mac Studio",
        subtitle="M4 Max runs 14B faster than the Mac Pro runs 1.5B, and sweeps 32B at 18.1 tok/s",
        mac_legend="Mac Pro 2013 (Dual D500)",
        opp_legend="M4 Max Studio (32C Metal)",
        opp_tag="M4 MAX",
        opp_color=COL_STUDIO,
        opp_bg="#064E3B",
        rows=rows,
        footer_text="Mac Pro 2013 (Dual FirePro D500 + Xeon) vs M4 Max Studio (32-core GPU Metal 4, 410 GB/s unified RAM)",
    )


def chart_25_d500_vs_d700_predicted() -> Path:
    """Model-by-model comparison: Tested Dual D500 (6 GB) vs Predicted Dual D700 (12 GB)."""
    lines = svg_header(
        "FirePro D500 (Tested) vs. D700 (*Predicted)",
        "Small models (1.5B, 7B) see only ~10% gains; 14B unlocks 100% VRAM offload and ~2x+ faster prefill",
        "GPU UPGRADE MATH // MODEL BY MODEL",
    )

    # Legend pills on right of header
    lines.append(f'  <circle cx="1310" cy="158" r="8" fill="{COL_MACPRO}"/>')
    lines.append(f'  <text x="1328" y="164" font-family="{FONT_SANS}" font-size="18" font-weight="bold" fill="{COL_MACPRO}">D500 6 GB (£210 Tested)</text>')
    lines.append(f'  <circle cx="1596" cy="158" r="8" fill="{COL_STUDIO}"/>')
    lines.append(f'  <text x="1614" y="164" font-family="{FONT_SANS}" font-size="18" font-weight="bold" fill="{COL_STUDIO}">D700 12 GB (£330 *Pred.)</text>')

    # Top Column Headers (y=204..252)
    lines.append(f'  <rect x="80" y="204" width="1760" height="48" rx="12" fill="#0F172A" stroke="{CARD_BORDER}" stroke-width="1.5"/>')
    lines.append(f'  <text x="116" y="234" font-family="{FONT_MONO}" font-size="16" font-weight="bold" fill="{TEXT_DIM}">MODEL</text>')
    lines.append(f'  <text x="410" y="234" font-family="{FONT_MONO}" font-size="16" font-weight="bold" fill="{TEXT_DIM}">DUAL D500 (6 GB TESTED)</text>')
    lines.append(f'  <text x="930" y="234" font-family="{FONT_MONO}" font-size="16" font-weight="bold" fill="{TEXT_DIM}">DUAL D700 (12 GB *PREDICTED)</text>')
    lines.append(f'  <text x="1500" y="234" font-family="{FONT_MONO}" font-size="16" font-weight="bold" fill="{TEXT_DIM}">UPGRADE IMPACT</text>')

    rows = [
        {
            "size": "1.5B Q8_0",
            "sub": "1.89 GB (Fits 6 GB)",
            "d500_val": "36.6 tok/s",
            "d500_note": "Already 100% in D500 VRAM",
            "d700_val": "~40 tok/s*",
            "d700_note": "100% VRAM (+10% bandwidth)",
            "verdict": "Modest (~+10%)",
            "v_col": TEXT_MUTED,
            "v_bg": "#1E293B",
            "hero": False,
        },
        {
            "size": "7B Q4_K_M",
            "sub": "4.36 GiB (Fits 6 GB)",
            "d500_val": "13.0 tok/s",
            "d500_note": "Already 28/28 layers in VRAM",
            "d700_val": "~14.3 tok/s*",
            "d700_note": "+10% gen, +20-34% PP, 16K-32K Ctx",
            "verdict": "Modest + Huge Context",
            "v_col": TEXT_MUTED,
            "v_bg": "#1E293B",
            "hero": False,
        },
        {
            "size": "14B Q4_K_M",
            "sub": "8.37 GiB (Exceeds 6 GB)",
            "d500_val": "6.40 tok/s",
            "d500_note": "Spills 24/48 layers to Xeon CPU",
            "d700_val": "~7.5 to 9+ tok/s*",
            "d700_note": "Fits 100% in 12 GB VRAM (~2x+ PP!)",
            "verdict": "BIG WIN: 100% VRAM",
            "v_col": COL_STUDIO,
            "v_bg": "#064E3B",
            "hero": True,
        },
        {
            "size": "32B Q4_K_M",
            "sub": "18.5 GiB (Exceeds 12 GB)",
            "d500_val": "2.53 tok/s",
            "d500_note": "Pure CPU in 64 GB ECC RAM",
            "d700_val": "~3.5 to 4 tok/s*",
            "d700_note": "Offloads ~half layers via GPU hybrid",
            "verdict": "Moderate (~Half GPU)",
            "v_col": COL_MACPRO,
            "v_bg": "#422006",
            "hero": False,
        },
    ]

    ry = 268
    rh = 158
    gap = 20
    for r in rows:
        is_hero = r["hero"]
        row_border = COL_STUDIO if is_hero else CARD_BORDER
        row_bg = "#0A221D" if is_hero else CARD_BG
        lines.append(f'  <rect x="80" y="{ry}" width="1760" height="{rh}" rx="16" fill="{row_bg}" stroke="{row_border}" stroke-width="{"2.5" if is_hero else "1.5"}"/>')

        # Model column
        lines.append(f'  <text x="116" y="{ry + 68}" font-family="{FONT_MONO}" font-size="26" font-weight="bold" fill="{TEXT_MAIN}">{esc(r["size"])}</text>')
        lines.append(f'  <text x="116" y="{ry + 104}" font-family="{FONT_SANS}" font-size="18" fill="{COL_STUDIO if is_hero else TEXT_MUTED}">{esc(r["sub"])}</text>')

        # D500 box (x=410..890)
        lines.append(f'  <rect x="410" y="{ry + 26}" width="480" height="106" rx="12" fill="#0F172A" stroke="{COL_MACPRO}" stroke-width="1.5"/>')
        lines.append(f'  <text x="434" y="{ry + 70}" font-family="{FONT_MONO}" font-size="30" font-weight="bold" fill="{TEXT_MAIN}">{esc(r["d500_val"])}</text>')
        lines.append(f'  <text x="434" y="{ry + 106}" font-family="{FONT_SANS}" font-size="17" fill="{TEXT_MUTED}">{esc(r["d500_note"])}</text>')

        # D700 box (x=930..1460)
        lines.append(f'  <rect x="930" y="{ry + 26}" width="530" height="106" rx="12" fill="{"#064E3B" if is_hero else "#0F172A"}" stroke="{COL_STUDIO if is_hero else "#334155"}" stroke-width="{"2" if is_hero else "1.5"}"/>')
        lines.append(f'  <text x="954" y="{ry + 70}" font-family="{FONT_MONO}" font-size="30" font-weight="bold" fill="{COL_STUDIO if is_hero else TEXT_MAIN}">{esc(r["d700_val"])}</text>')
        lines.append(f'  <text x="954" y="{ry + 106}" font-family="{FONT_SANS}" font-size="17" fill="{TEXT_MAIN if is_hero else TEXT_MUTED}">{esc(r["d700_note"])}</text>')

        # Impact Verdict pill (x=1494..1812)
        lines.append(f'  <rect x="1494" y="{ry + 49}" width="318" height="60" rx="12" fill="{r["v_bg"]}" stroke="{r["v_col"]}" stroke-width="1.5"/>')
        lines.append(f'  <text x="1653" y="{ry + 85}" text-anchor="middle" font-family="{FONT_MONO}" font-size="17" font-weight="bold" fill="{r["v_col"]}">{esc(r["verdict"])}</text>')

        ry += rh + gap

    lines.extend(svg_footer("D500 figures measured on MacPro6,1; *D700 projections extrapolated from 12 GB VRAM & +34% Tahiti shaders"))
    return render_svg("25_d500_vs_d700_predicted", lines)


def main() -> int:
    charts = [
        chart_00_gpu_vs_cpu_simple_explainer(),
        chart_09a_driver_step1_grub(),
        chart_09b_driver_step2_modprobe(),
        chart_09c_driver_step3_rebuild_reboot(),
        chart_09d_driver_step4_verify_vulkan(),
        chart_10_build_custom_llama(),
        chart_11_thread_scaling_12_vs_24(),
        chart_12_transparent_huge_pages(),
        chart_13_flash_attention(),
        chart_14_fan_thermal_tuning(),
        chart_15_models_and_usecases(),
        chart_16_14b_hybrid_split(),
    ]
    charts.extend(chart_17_individual_model_perf())
    charts.append(chart_18_trashcan_vs_starfighter())
    charts.append(chart_19_trashcan_vs_starfighter_cpu_8t())
    charts.append(chart_20_trashcan_vs_macbook_neo())
    charts.append(chart_21_trashcan_vs_macbook_neo_cpu())
    charts.append(chart_22_vision_neo_starfighter_trashcan())
    charts.append(chart_23_trashcan_vs_mac_studio())
    charts.append(chart_24_vision_all_4_machines())
    charts.append(chart_25_d500_vs_d700_predicted())
    for path in charts:
        print(f"Generated: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
