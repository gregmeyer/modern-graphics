"""Pretext integration utilities for pixel-perfect SVG text rendering.

Uses @chenglou/pretext to measure text layout (line breaks, dimensions)
and renders as SVG <text> elements with precise positioning.
"""

PRETEXT_VERSION = "0.0.3"
PRETEXT_CDN_URL = f"https://cdn.jsdelivr.net/npm/@chenglou/pretext@{PRETEXT_VERSION}/dist/layout.js"


def generate_pretext_cdn_script() -> str:
    """Return <script> tag loading Pretext from CDN."""
    return f'<script type="module" src="{PRETEXT_CDN_URL}"></script>'


def generate_pretext_bootstrap_script() -> str:
    """Return <script> that measures .pretext-slot elements and injects SVG text.

    Runs on DOMContentLoaded. For each element with class ``pretext-slot``,
    reads data attributes for font, max-width, and line-height, then replaces
    the element's innerHTML with an inline SVG containing positioned <text>
    and <tspan> elements.

    Sets ``window.__pretextReady = true`` when all slots are processed so the
    Playwright export pipeline can wait before taking a screenshot.
    """
    return """
    <script type="module">
    import { prepareWithSegments, layoutWithLines } from '""" + PRETEXT_CDN_URL + """';

    function processSlots() {
      const slots = document.querySelectorAll('.pretext-slot');
      if (!slots.length) {
        window.__pretextReady = true;
        return;
      }

      for (const slot of slots) {
        const text = slot.getAttribute('data-pt-text') || slot.textContent.trim();
        const font = slot.getAttribute('data-pt-font') || '16px Inter';
        const maxWidth = parseFloat(slot.getAttribute('data-pt-max-width') || slot.offsetWidth || 900);
        const lineHeight = parseFloat(slot.getAttribute('data-pt-line-height') || '1.15');
        const fill = slot.getAttribute('data-pt-fill') || 'currentColor';
        const textAnchor = slot.getAttribute('data-pt-text-anchor') || 'start';

        // Parse font size from the font string (e.g. "64px 'Press Start 2P'" -> 64)
        const fontSizeMatch = font.match(/(\\d+(?:\\.\\d+)?)px/);
        const fontSize = fontSizeMatch ? parseFloat(fontSizeMatch[1]) : 16;

        // Compute absolute line height
        const absLineHeight = lineHeight < 4 ? fontSize * lineHeight : lineHeight;

        try {
          const prepared = prepareWithSegments(text, font);
          const result = layoutWithLines(prepared, maxWidth, absLineHeight);

          // Build SVG
          const svgNS = 'http://www.w3.org/2000/svg';
          const totalHeight = result.height || (result.lineCount * absLineHeight);
          const svg = document.createElementNS(svgNS, 'svg');
          svg.setAttribute('width', String(maxWidth));
          svg.setAttribute('height', String(totalHeight));
          svg.setAttribute('viewBox', `0 0 ${maxWidth} ${totalHeight}`);
          svg.style.display = 'block';
          svg.style.overflow = 'visible';

          const textEl = document.createElementNS(svgNS, 'text');
          textEl.setAttribute('font-family', font.replace(/^[\\d.]+px\\s*/, ''));
          textEl.setAttribute('font-size', String(fontSize));
          textEl.setAttribute('fill', fill);
          textEl.setAttribute('text-anchor', textAnchor);

          const xPos = textAnchor === 'middle' ? maxWidth / 2
                     : textAnchor === 'end' ? maxWidth
                     : 0;

          for (let i = 0; i < result.lines.length; i++) {
            const line = result.lines[i];
            const tspan = document.createElementNS(svgNS, 'tspan');
            tspan.setAttribute('x', String(xPos));
            // First line uses dominant-baseline offset, subsequent use dy
            if (i === 0) {
              tspan.setAttribute('y', String(fontSize));
            } else {
              tspan.setAttribute('dy', String(absLineHeight));
            }
            tspan.textContent = line.text;
            textEl.appendChild(tspan);
          }

          svg.appendChild(textEl);

          // Replace slot content but preserve the container element and its classes
          slot.innerHTML = '';
          slot.appendChild(svg);
          slot.setAttribute('data-pt-rendered', 'true');
        } catch (err) {
          // Fallback: leave original text content in place
          console.warn('Pretext rendering failed for slot:', err);
          slot.setAttribute('data-pt-error', err.message);
        }
      }

      window.__pretextReady = true;
    }

    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', processSlots);
    } else {
      processSlots();
    }
    </script>
    """
