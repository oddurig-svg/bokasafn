from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]
INDEX = ROOT / "index.html"
CSS_DIR = ROOT / "css"
JS_DIR = ROOT / "js"

html = INDEX.read_text(encoding="utf-8")
CSS_DIR.mkdir(exist_ok=True)
JS_DIR.mkdir(exist_ok=True)

# --- CSS -----------------------------------------------------------------
# Keep the cascade exactly as it currently appears. The first style block is
# the base site CSS; the remaining blocks are the existing theme/override CSS.
style_re = re.compile(r"<style(?P<attrs>[^>]*)>(?P<content>.*?)</style>", re.DOTALL | re.IGNORECASE)
styles = list(style_re.finditer(html))

if not styles:
    raise RuntimeError("No inline <style> blocks found in index.html")

base_css = styles[0].group("content").strip() + "\n"
theme_css = "\n\n".join(m.group("content").strip() for m in styles[1:]).strip() + "\n"

(CSS_DIR / "main.css").write_text(base_css, encoding="utf-8")
(CSS_DIR / "themes.css").write_text(theme_css, encoding="utf-8")

first_style = True

def replace_style(match: re.Match) -> str:
    global first_style
    if first_style:
        first_style = False
        return '<link rel="stylesheet" href="css/main.css">\n    <link rel="stylesheet" href="css/themes.css">'
    return ""

html = style_re.sub(replace_style, html)

# --- JavaScript -----------------------------------------------------------
# Extract each inline script to an external classic script at the exact same
# location. This keeps synchronous execution order and existing globals intact.
script_re = re.compile(r"<script(?P<attrs>[^>]*)>(?P<content>.*?)</script>", re.DOTALL | re.IGNORECASE)
script_counter = 0
created_scripts = []

def script_name(attrs: str, content: str) -> str:
    global script_counter
    id_match = re.search(r'\bid=["\']([^"\']+)["\']', attrs, re.IGNORECASE)
    script_id = id_match.group(1) if id_match else ""

    if script_id == "appearance-toggle-script":
        return "appearance.js"
    if script_id == "auto-system-theme":
        return "system-theme.js"
    if "const BOKASAFN_THEMES" in content or "function setBokasafnTheme" in content:
        return "themes.js"
    if "let allBooks = []" in content and "function fetchBooks" in content:
        return "app.js"

    script_counter += 1
    return f"inline-{script_counter}.js"


def replace_script(match: re.Match) -> str:
    attrs = match.group("attrs") or ""
    content = match.group("content")

    # Keep existing external scripts (e.g. Tailwind) untouched.
    if re.search(r"\bsrc\s*=", attrs, re.IGNORECASE):
        return match.group(0)

    # Skip truly empty inline blocks.
    if not content.strip():
        return match.group(0)

    name = script_name(attrs, content)
    path = JS_DIR / name
    path.write_text(content.strip() + "\n", encoding="utf-8")
    created_scripts.append(name)

    # Preserve id if one existed; drop other inline-only attributes.
    id_match = re.search(r'\bid=["\']([^"\']+)["\']', attrs, re.IGNORECASE)
    id_attr = f' id="{id_match.group(1)}"' if id_match else ""
    return f'<script{id_attr} src="js/{name}"></script>'

html = script_re.sub(replace_script, html)

INDEX.write_text(html, encoding="utf-8")

print(f"Extracted {len(styles)} style blocks -> css/main.css + css/themes.css")
print("Extracted inline scripts -> " + ", ".join(created_scripts))
