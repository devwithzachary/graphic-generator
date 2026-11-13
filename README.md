# Video Graphic Generator

Reusable `1920x1080` dark-studio SVG-to-PNG graphic generator for YouTube technical videos.

## Structure

- `graphic_gen.py`: Shared dark-studio palette, typography, `svg_header` / `svg_footer`, `term_window`, `render_svg`, and reusable slide builders (`render_single_perf_slide`, `render_vs_machine_table`, `render_vision_cards`).
- `projects/<project-name>/`: Self-contained video projects, each with its own `generate.py` and `output/` directory.

## First Use Case: `trashcan-ai`

All 26 graphics for the 2013 Mac Pro AI project live in:
- `projects/trashcan-ai/generate.py`
- `projects/trashcan-ai/output/`

Regenerate with:

```bash
python3 projects/trashcan-ai/generate.py
```

## Adding a New Video Project

1. Create `projects/<new-video>/generate.py` and add the repo root to `sys.path` to import `graphic_gen`.
2. Set `OUT_DIR = Path(__file__).resolve().parent / "output"`.
3. Compose custom slides using `svg_header`, `svg_footer`, `term_window`, and `render_svg`, or call the built-in builders (`render_single_perf_slide`, `render_vs_machine_table`, `render_vision_cards`).

