#!/usr/bin/env python3
"""
Generic 1920x1080 dark-studio YouTube video graphic generator library.

Provides a cohesive palette, typography, SVG->PNG rendering (via rsvg-convert),
and reusable slide builders for comparisons, benchmarks, terminal steps, and
model/feature grids.
"""

from __future__ import annotations

import html
import subprocess
from pathlib import Path

W, H = 1920, 1080

FONT_SANS = "Fira Sans, DejaVu Sans, sans-serif"
FONT_MONO = "DejaVu Sans Mono, monospace"

# Cohesive dark-studio color palette
BG_TOP = "#0B1020"
BG_BOT = "#121A2F"
CARD_BG = "#162038"
CARD_BORDER = "#29385E"
TEXT_MAIN = "#F8FAFC"
TEXT_MUTED = "#94A3B8"
TEXT_DIM = "#64748B"

COL_GOLD = "#F59E0B"      # Amber gold (hero hardware / primary accent)
COL_SKY = "#38BDF8"       # Sky blue
COL_VIOLET = "#A78BFA"    # Violet
COL_EMERALD = "#34D399"   # Emerald green
COL_DANGER = "#F87171"    # Coral red

# Backwards-friendly aliases
COL_MACPRO = COL_GOLD
COL_STARFIGHTER = COL_SKY
COL_NEO = COL_VIOLET
COL_STUDIO = COL_EMERALD


def esc(text: str) -> str:
    """Escape XML entities safely for SVG text elements."""
    return html.escape(str(text), quote=True)


def svg_header(title: str, subtitle: str, tag: str, accent: str = COL_GOLD) -> list[str]:
    """Return consistent 1920x1080 canvas defs and header banner."""
    pill_w = max(260, len(tag) * 11 + 52)
    pill_cx = 80 + pill_w // 2
    return [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
        "  <defs>",
        '    <linearGradient id="bgGrad" x1="0%" y1="0%" x2="100%" y2="100%">',
        f'      <stop offset="0%" stop-color="{BG_TOP}"/>',
        f'      <stop offset="100%" stop-color="{BG_BOT}"/>',
        "    </linearGradient>",
        '    <linearGradient id="heroGrad" x1="0%" y1="0%" x2="100%" y2="0%">',
        f'      <stop offset="0%" stop-color="{accent}"/>',
        '      <stop offset="100%" stop-color="#FBBF24"/>',
        "    </linearGradient>",
        "  </defs>",
        f'  <rect width="{W}" height="{H}" fill="url(#bgGrad)"/>',
        f'  <rect x="0" y="0" width="{W}" height="6" fill="url(#heroGrad)"/>',
        f'  <rect x="80" y="48" width="{pill_w}" height="36" rx="18" fill="#1F2937" stroke="{accent}" stroke-width="1.5"/>',
        f'  <text x="{pill_cx}" y="72" text-anchor="middle" font-family="{FONT_MONO}" font-size="16" font-weight="bold" fill="#FBBF24">{esc(tag)}</text>',
        f'  <text x="80" y="136" font-family="{FONT_SANS}" font-size="48" font-weight="bold" fill="{TEXT_MAIN}">{esc(title)}</text>',
        f'  <text x="80" y="176" font-family="{FONT_SANS}" font-size="23" fill="{TEXT_MUTED}">{esc(subtitle)}</text>',
    ]


def svg_footer(note: str, brand: str = "Studio Graphics // 1920x1080") -> list[str]:
    """Return consistent bottom provenance bar."""
    return [
        f'  <line x1="80" y1="1012" x2="1840" y2="1012" stroke="{CARD_BORDER}" stroke-width="1.5"/>',
        f'  <text x="80" y="1046" font-family="{FONT_SANS}" font-size="18" fill="{TEXT_DIM}">{esc(note)}</text>',
        f'  <text x="1840" y="1046" text-anchor="end" font-family="{FONT_MONO}" font-size="18" fill="{TEXT_DIM}">{esc(brand)}</text>',
        "</svg>",
    ]


def render_svg(out_dir: Path, name: str, lines: list[str]) -> Path:
    """Write SVG and render crisp 1920x1080 PNG via rsvg-convert."""
    out_dir.mkdir(parents=True, exist_ok=True)
    svg_path = out_dir / f"{name}.svg"
    png_path = out_dir / f"{name}.png"
    svg_path.write_text("\n".join(lines), encoding="utf-8")
    subprocess.run(
        ["rsvg-convert", "-w", str(W), "-h", str(H), "-o", str(png_path), str(svg_path)],
        check=True,
    )
    svg_path.unlink()
    return png_path


def term_window(lines: list[str], x: int, y: int, w: int, h: int, title_bar: str) -> None:
    """Draw a styled dark terminal window card."""
    lines.append(f'  <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" fill="#090D16" stroke="#334155" stroke-width="1.5"/>')
    lines.append(f'  <rect x="{x}" y="{y}" width="{w}" height="36" rx="14" fill="#1E293B"/>')
    lines.append(f'  <rect x="{x}" y="{y + 20}" width="{w}" height="16" fill="#1E293B"/>')
    lines.append(f'  <circle cx="{x + 20}" cy="{y + 18}" r="5.5" fill="#EF4444"/>')
    lines.append(f'  <circle cx="{x + 38}" cy="{y + 18}" r="5.5" fill="#F59E0B"/>')
    lines.append(f'  <circle cx="{x + 56}" cy="{y + 18}" r="5.5" fill="#10B981"/>')
    lines.append(f'  <text x="{x + 80}" y="{y + 23}" font-family="{FONT_MONO}" font-size="14" fill="{TEXT_MUTED}">{esc(title_bar)}</text>')


def render_single_perf_slide(
    out_dir: Path,
    filename: str,
    eyebrow: str,
    title: str,
    subtitle: str,
    accent: str,
    left_label: str,
    left_value: str,
    left_unit: str,
    left_note: str,
    right_label: str,
    right_value: str,
    right_unit: str,
    right_note: str,
    target_val: str,
    size_val: str,
    flags_val: str,
    footer_text: str,
    brand: str = "Studio Graphics // 1920x1080",
) -> Path:
    """Reusable full-slide single-item performance card (two hero metrics + 3-col spec strip)."""
    lines = svg_header(title, subtitle, eyebrow)

    lx, ly, lw, lh = 80, 216, 855, 456
    lines.append(f'  <rect x="{lx}" y="{ly}" width="{lw}" height="{lh}" rx="22" fill="{CARD_BG}" stroke="{COL_SKY}" stroke-width="2"/>')
    lines.append(f'  <rect x="{lx}" y="{ly}" width="{lw}" height="8" rx="4" fill="{COL_SKY}"/>')
    lines.append(f'  <text x="{lx + 48}" y="{ly + 66}" font-family="{FONT_MONO}" font-size="20" font-weight="bold" fill="{COL_SKY}">{esc(left_label)}</text>')
    lines.append(f'  <text x="{lx + 48}" y="{ly + 266}" font-family="{FONT_MONO}" font-size="128" font-weight="bold" fill="{TEXT_MAIN}">{esc(left_value)}</text>')
    lines.append(f'  <text x="{lx + 48}" y="{ly + 324}" font-family="{FONT_MONO}" font-size="32" font-weight="bold" fill="{COL_SKY}">{esc(left_unit)}</text>')
    lines.append(f'  <text x="{lx + 48}" y="{ly + 404}" font-family="{FONT_SANS}" font-size="22" fill="{TEXT_MUTED}">{esc(left_note)}</text>')

    rx, ry, rw, rh = 985, 216, 855, 456
    lines.append(f'  <rect x="{rx}" y="{ry}" width="{rw}" height="{rh}" rx="22" fill="{CARD_BG}" stroke="{accent}" stroke-width="2.5"/>')
    lines.append(f'  <rect x="{rx}" y="{ry}" width="{rw}" height="8" rx="4" fill="{accent}"/>')
    lines.append(f'  <text x="{rx + 48}" y="{ry + 66}" font-family="{FONT_MONO}" font-size="20" font-weight="bold" fill="{accent}">{esc(right_label)}</text>')
    lines.append(f'  <text x="{rx + 48}" y="{ry + 266}" font-family="{FONT_MONO}" font-size="128" font-weight="bold" fill="{TEXT_MAIN}">{esc(right_value)}</text>')
    lines.append(f'  <text x="{rx + 48}" y="{ry + 324}" font-family="{FONT_MONO}" font-size="32" font-weight="bold" fill="{accent}">{esc(right_unit)}</text>')
    lines.append(f'  <text x="{rx + 48}" y="{ry + 404}" font-family="{FONT_SANS}" font-size="22" fill="{TEXT_MUTED}">{esc(right_note)}</text>')

    sx, sy, sw, sh = 80, 712, 1760, 246
    lines.append(f'  <rect x="{sx}" y="{sy}" width="{sw}" height="{sh}" rx="20" fill="{CARD_BG}" stroke="{CARD_BORDER}" stroke-width="1.5"/>')

    specs = [
        ("EXECUTION TARGET", target_val, accent),
        ("MODEL FOOTPRINT", size_val, TEXT_MAIN),
        ("TUNED FLAGS", flags_val, COL_GOLD),
    ]
    col_w = sw // 3
    for idx, (s_lbl, s_val, s_col) in enumerate(specs):
        cx = sx + idx * col_w
        if idx > 0:
            lines.append(f'  <line x1="{cx}" y1="{sy + 36}" x2="{cx}" y2="{sy + sh - 36}" stroke="{CARD_BORDER}" stroke-width="1.5"/>')
        lines.append(f'  <text x="{cx + 48}" y="{sy + 82}" font-family="{FONT_MONO}" font-size="17" font-weight="bold" fill="{TEXT_DIM}">{esc(s_lbl)}</text>')
        lines.append(f'  <text x="{cx + 48}" y="{sy + 150}" font-family="{FONT_SANS}" font-size="28" font-weight="bold" fill="{s_col}">{esc(s_val)}</text>')

    lines.extend(svg_footer(footer_text, brand=brand))
    return render_svg(out_dir, filename, lines)


def render_vs_machine_table(
    out_dir: Path,
    filename: str,
    eyebrow: str,
    title: str,
    subtitle: str,
    mac_legend: str,
    opp_legend: str,
    opp_tag: str,
    opp_color: str,
    opp_bg: str,
    rows: list[dict],
    footer_text: str,
    mac_tag: str = "MAC PRO",
    brand: str = "Studio Graphics // 1920x1080",
) -> Path:
    """Shared 4-row head-to-head comparison table between two machines."""
    lines = svg_header(title, subtitle, eyebrow)

    lines.append(f'  <rect x="80" y="204" width="1760" height="48" rx="12" fill="#0F172A" stroke="{CARD_BORDER}" stroke-width="1.5"/>')
    lines.append(f'  <text x="116" y="234" font-family="{FONT_MONO}" font-size="16" font-weight="bold" fill="{TEXT_DIM}">MODEL</text>')
    lines.append(f'  <text x="430" y="234" font-family="{FONT_MONO}" font-size="16" font-weight="bold" fill="{TEXT_DIM}">TOKEN GENERATION (tg128 tok/s)</text>')
    lines.append(f'  <text x="1030" y="234" font-family="{FONT_MONO}" font-size="16" font-weight="bold" fill="{TEXT_DIM}">PROMPT PREFILL (pp512 tok/s)</text>')
    lines.append(f'  <text x="1570" y="234" font-family="{FONT_MONO}" font-size="16" font-weight="bold" fill="{TEXT_DIM}">VERDICT</text>')

    lines.append(f'  <circle cx="1370" cy="158" r="8" fill="{COL_GOLD}"/>')
    lines.append(f'  <text x="1388" y="164" font-family="{FONT_SANS}" font-size="18" font-weight="bold" fill="{COL_GOLD}">{esc(mac_legend)}</text>')
    lines.append(f'  <circle cx="1636" cy="158" r="8" fill="{opp_color}"/>')
    lines.append(f'  <text x="1654" y="164" font-family="{FONT_SANS}" font-size="18" font-weight="bold" fill="{opp_color}">{esc(opp_legend)}</text>')

    ry = 268
    rh = 158
    gap = 20
    for r in rows:
        lines.append(f'  <rect x="80" y="{ry}" width="1760" height="{rh}" rx="16" fill="{CARD_BG}" stroke="{CARD_BORDER}" stroke-width="1.5"/>')
        lines.append(f'  <text x="116" y="{ry + 68}" font-family="{FONT_MONO}" font-size="26" font-weight="bold" fill="{TEXT_MAIN}">{esc(r["size"])}</text>')
        lines.append(f'  <text x="116" y="{ry + 104}" font-family="{FONT_SANS}" font-size="19" fill="{TEXT_MUTED}">{esc(r["sub"])}</text>')

        mac_g_win = r["gen_win"] == "mac"
        opp_g_win = r["gen_win"] == "opp"
        lines.append(f'  <rect x="430" y="{ry + 32}" width="248" height="94" rx="12" fill="{"#422006" if mac_g_win else "#0F172A"}" stroke="{COL_GOLD if mac_g_win else "#334155"}" stroke-width="{"2" if mac_g_win else "1"}"/>')
        lines.append(f'  <text x="450" y="{ry + 62}" font-family="{FONT_MONO}" font-size="14" font-weight="bold" fill="{COL_GOLD}">{esc(mac_tag)} {"(WIN)" if mac_g_win else ""}</text>')
        gen_mac_str = f'{r["gen_mac"]:.2f}' if r["gen_mac"] < 10 else f'{r["gen_mac"]:.1f}'
        lines.append(f'  <text x="450" y="{ry + 104}" font-family="{FONT_MONO}" font-size="32" font-weight="bold" fill="{TEXT_MAIN if mac_g_win else TEXT_MUTED}">{gen_mac_str} <tspan font-size="17">t/s</tspan></text>')

        if r["gen_opp"] is None:
            lines.append(f'  <rect x="694" y="{ry + 32}" width="248" height="94" rx="12" fill="#450A0A" stroke="{COL_DANGER}" stroke-width="1.5"/>')
            lines.append(f'  <text x="714" y="{ry + 62}" font-family="{FONT_MONO}" font-size="14" font-weight="bold" fill="{COL_DANGER}">{esc(opp_tag)}</text>')
            lines.append(f'  <text x="714" y="{ry + 104}" font-family="{FONT_MONO}" font-size="28" font-weight="bold" fill="#FCA5A5">OOM <tspan font-size="15">(&gt;8 GB)</tspan></text>')
        else:
            lines.append(f'  <rect x="694" y="{ry + 32}" width="248" height="94" rx="12" fill="{opp_bg if opp_g_win else "#0F172A"}" stroke="{opp_color if opp_g_win else "#334155"}" stroke-width="{"2" if opp_g_win else "1"}"/>')
            lines.append(f'  <text x="714" y="{ry + 62}" font-family="{FONT_MONO}" font-size="14" font-weight="bold" fill="{opp_color}">{esc(opp_tag)} {"(WIN)" if opp_g_win else ""}</text>')
            gen_opp_str = f'{r["gen_opp"]:.2f}' if r["gen_opp"] < 10 else f'{r["gen_opp"]:.1f}'
            lines.append(f'  <text x="714" y="{ry + 104}" font-family="{FONT_MONO}" font-size="32" font-weight="bold" fill="{TEXT_MAIN if opp_g_win else TEXT_MUTED}">{gen_opp_str} <tspan font-size="17">t/s</tspan></text>')

        mac_p_win = r["pp_win"] == "mac"
        opp_p_win = r["pp_win"] == "opp"
        lines.append(f'  <rect x="1030" y="{ry + 32}" width="240" height="94" rx="12" fill="{"#422006" if mac_p_win else "#0F172A"}" stroke="{COL_GOLD if mac_p_win else "#334155"}" stroke-width="{"2" if mac_p_win else "1"}"/>')
        lines.append(f'  <text x="1050" y="{ry + 62}" font-family="{FONT_MONO}" font-size="14" font-weight="bold" fill="{COL_GOLD}">{esc(mac_tag)} {"(WIN)" if mac_p_win else ""}</text>')
        pp_mac_str = f'{r["pp_mac"]:.2f}' if r["pp_mac"] < 10 else f'{r["pp_mac"]:.1f}'
        lines.append(f'  <text x="1050" y="{ry + 104}" font-family="{FONT_MONO}" font-size="30" font-weight="bold" fill="{TEXT_MAIN if mac_p_win else TEXT_MUTED}">{pp_mac_str} <tspan font-size="16">t/s</tspan></text>')

        if r["pp_opp"] is None:
            lines.append(f'  <rect x="1286" y="{ry + 32}" width="248" height="94" rx="12" fill="#450A0A" stroke="{COL_DANGER}" stroke-width="1.5"/>')
            lines.append(f'  <text x="1306" y="{ry + 62}" font-family="{FONT_MONO}" font-size="14" font-weight="bold" fill="{COL_DANGER}">{esc(opp_tag)}</text>')
            lines.append(f'  <text x="1306" y="{ry + 104}" font-family="{FONT_MONO}" font-size="28" font-weight="bold" fill="#FCA5A5">OOM <tspan font-size="15">(&gt;8 GB)</tspan></text>')
        else:
            lines.append(f'  <rect x="1286" y="{ry + 32}" width="248" height="94" rx="12" fill="{opp_bg if opp_p_win else "#0F172A"}" stroke="{opp_color if opp_p_win else "#334155"}" stroke-width="{"2" if opp_p_win else "1"}"/>')
            lines.append(f'  <text x="1306" y="{ry + 62}" font-family="{FONT_MONO}" font-size="14" font-weight="bold" fill="{opp_color}">{esc(opp_tag)} {"(WIN)" if opp_p_win else ""}</text>')
            pp_opp_str = f'{r["pp_opp"]:.2f}' if r["pp_opp"] < 10 else f'{r["pp_opp"]:.1f}'
            lines.append(f'  <text x="1306" y="{ry + 104}" font-family="{FONT_MONO}" font-size="30" font-weight="bold" fill="{TEXT_MAIN if opp_p_win else TEXT_MUTED}">{pp_opp_str} <tspan font-size="16">t/s</tspan></text>')

        v_bg = "#422006" if r["v_col"] == COL_GOLD else opp_bg
        lines.append(f'  <rect x="1566" y="{ry + 49}" width="246" height="60" rx="12" fill="{v_bg}" stroke="{r["v_col"]}" stroke-width="1.5"/>')
        lines.append(f'  <text x="1689" y="{ry + 85}" text-anchor="middle" font-family="{FONT_MONO}" font-size="15" font-weight="bold" fill="{r["v_col"]}">{esc(r["verdict"])}</text>')

        ry += rh + gap

    lines.extend(svg_footer(footer_text, brand=brand))
    return render_svg(out_dir, filename, lines)


def render_vision_cards(
    out_dir: Path,
    filename: str,
    eyebrow: str,
    title: str,
    subtitle: str,
    cards: list[dict],
    footer_text: str,
    brand: str = "Studio Graphics // 1920x1080",
) -> Path:
    """Shared 3- or 4-column comparison card layout."""
    lines = svg_header(title, subtitle, eyebrow)

    n = len(cards)
    total_w = 1760
    gx = 34 if n == 3 else 28
    cw = (total_w - (n - 1) * gx) // n
    ch = 766
    x0, y0 = 80, 208
    pad = 32 if n == 3 else 24

    for idx, c in enumerate(cards):
        cx = x0 + idx * (cw + gx)
        acc = c["accent"]

        lines.append(f'  <rect x="{cx}" y="{y0}" width="{cw}" height="{ch}" rx="20" fill="{CARD_BG}" stroke="{acc}" stroke-width="2"/>')
        lines.append(f'  <rect x="{cx}" y="{y0}" width="{cw}" height="8" rx="4" fill="{acc}"/>')

        lines.append(f'  <rect x="{cx + pad}" y="{y0 + 34}" width="160" height="34" rx="8" fill="{c["pill_bg"]}" stroke="{acc}" stroke-width="1"/>')
        lines.append(f'  <text x="{cx + pad + 80}" y="{y0 + 57}" text-anchor="middle" font-family="{FONT_MONO}" font-size="15" font-weight="bold" fill="{acc}">{esc(c["rank"])}</text>')
        title_size = 32 if n == 3 else 27
        sub_size = 19 if n == 3 else 17
        lines.append(f'  <text x="{cx + pad}" y="{y0 + 112}" font-family="{FONT_SANS}" font-size="{title_size}" font-weight="bold" fill="{TEXT_MAIN}">{esc(c["title"])}</text>')
        lines.append(f'  <text x="{cx + pad}" y="{y0 + 146}" font-family="{FONT_SANS}" font-size="{sub_size}" fill="{TEXT_MUTED}">{esc(c["sub"])}</text>')

        lines.append(f'  <rect x="{cx + pad}" y="{y0 + 180}" width="{cw - 2 * pad}" height="196" rx="16" fill="#0F172A" stroke="#334155" stroke-width="1.5"/>')
        lines.append(f'  <text x="{cx + pad + 20}" y="{y0 + 220}" font-family="{FONT_MONO}" font-size="14" font-weight="bold" fill="{TEXT_DIM}">IMAGE ENCODE (ViT)</text>')
        vit_size = 68 if n == 3 else 58
        lines.append(f'  <text x="{cx + pad + 20}" y="{y0 + 298}" font-family="{FONT_MONO}" font-size="{vit_size}" font-weight="bold" fill="{TEXT_MAIN}">{esc(c["vit_val"])}</text>')
        vit_sub_size = 16 if n == 3 else 14
        lines.append(f'  <text x="{cx + pad + 20}" y="{y0 + 346}" font-family="{FONT_MONO}" font-size="{vit_sub_size}" fill="{TEXT_MUTED}">{esc(c["vit_sub"])}</text>')

        lines.append(f'  <rect x="{cx + pad}" y="{y0 + 404}" width="{cw - 2 * pad}" height="234" rx="16" fill="#0F172A" stroke="{acc}" stroke-width="1.5"/>')
        lines.append(f'  <text x="{cx + pad + 20}" y="{y0 + 444}" font-family="{FONT_MONO}" font-size="14" font-weight="bold" fill="{acc}">END-TO-END ALT-TEXT</text>')

        lbl_size = 19 if n == 3 else 16
        val_size = 36 if n == 3 else 30
        lines.append(f'  <text x="{cx + pad + 20}" y="{y0 + 498}" font-family="{FONT_SANS}" font-size="{lbl_size}" fill="{TEXT_MUTED}">{"2939x2499 IDE Screenshot" if n == 3 else "IDE Screenshot"}</text>')
        lines.append(f'  <text x="{cx + cw - pad - 20}" y="{y0 + 502}" text-anchor="end" font-family="{FONT_MONO}" font-size="{val_size}" font-weight="bold" fill="{TEXT_MAIN}">{esc(c["e2e_ide"])}</text>')

        lines.append(f'  <line x1="{cx + pad + 20}" y1="{y0 + 534}" x2="{cx + cw - pad - 20}" y2="{y0 + 534}" stroke="#1E293B" stroke-width="1.5"/>')

        lines.append(f'  <text x="{cx + pad + 20}" y="{y0 + 586}" font-family="{FONT_SANS}" font-size="{lbl_size}" fill="{TEXT_MUTED}">{"640x427 Park Scene Photo" if n == 3 else "Park Scene Photo"}</text>')
        lines.append(f'  <text x="{cx + cw - pad - 20}" y="{y0 + 590}" text-anchor="end" font-family="{FONT_MONO}" font-size="{val_size}" font-weight="bold" fill="{acc}">{esc(c["e2e_photo"])}</text>')

        lines.append(f'  <rect x="{cx + pad}" y="{y0 + 672}" width="{cw - 2 * pad}" height="58" rx="12" fill="{c["pill_bg"]}" stroke="{acc}" stroke-width="1.5"/>')
        pill_size = 16 if n == 3 else 14
        lines.append(f'  <text x="{cx + cw // 2}" y="{y0 + 708}" text-anchor="middle" font-family="{FONT_MONO}" font-size="{pill_size}" font-weight="bold" fill="{acc}">{esc(c["verdict"])}</text>')

    lines.extend(svg_footer(footer_text, brand=brand))
    return render_svg(out_dir, filename, lines)

