# goodman-assets
Fixed-address images used in Goodman English lesson follow-up emails (GitHub Pages).
**Never rename or move files in `cards/`** — every email already sent points at these URLs.
To redesign a card, overwrite the PNG under the same name. Source script: `src/make_cards.py`.

## explainers/
Pictures for the Grammar on the Move animated explainers (Lesson Pages). Master copies and the content file live in the private repo `goodman-english/grammar-on-the-move`.
- `explainers/three-futures/tf-1…7-*.webp` (640 px) and `explainers/three-futures/hd/` (1400 px, used by the big-picture layout): the pictures of Three futures (situations 1–7). **Never rename or move**: the live explainer points at these URLs. To change a picture, overwrite it under the same name.

## voice/
The Flashcards **voice page** (Hands-free mode with spoken answers). Course Tests pages run inside Google's Apps Script frame, which never allows the microphone, so the flashcards page's "🎤 Answer by voice" button opens `voice/` with the lesson's deck packed into the link's `#part` (never sent to any server). The page holds no lesson content of its own.
- `voice/index.html` is **built**, do not edit by hand: `python3 voice/src/build_voice.py voice/src/cards.vN.html voice/index.html` (source = the live `cards.vN.html` from Drive › Course Tests › app). Rebuild whenever a new cards version goes live.
- Keep the address `voice/` fixed: the live flashcards page points at it.
