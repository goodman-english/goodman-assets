#!/usr/bin/env python3
"""Build voice/index.html (the Flashcards VOICE page) from the Course Tests flashcards page cards.vN.html.

Why: Course Tests pages run inside Google's Apps Script frame, which never lets a page use the microphone.
The flashcards page's "🎤 Answer by voice" button opens THIS page with the deck packed into the link's #part
(never sent to any server); this page unpacks it and runs the very same flashcards code, microphone allowed.

Usage:  python3 voice/src/build_voice.py voice/src/cards.vN.html voice/index.html
Rebuild whenever a new cards.vN.html goes live in Drive > Course Tests > app.
"""
import sys

src, out = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()

def rep(old, new):
    global s
    assert s.count(old) == 1, 'expected once: ' + old[:60]
    s = s.replace(old, new)

rep('<!--CT_HEAD-->', '<meta name="viewport" content="width=device-width, initial-scale=1">\n<title>Flashcards – voice</title>')
rep('<script>\nconst D = /*CT_DATA*/null;\nconst LOGO = /*CT_LOGO*/"";',
    '<script type="text/plain" id="ctmain">\nconst D = window.__CT.D;\nconst LOGO = window.__CT.LOGO;')
LOADER = r'''<script>
/* voice page loader: unpack the deck from the link's #part, add the course look, then run the flashcards code */
window.__VOICE = true;
(async function () {
  function fail(m) { document.body.innerHTML = '<p style="font:19px Arial,sans-serif;padding:28px;color:#27272a;max-width:40em">' + m + '</p>'; }
  var h = location.hash.slice(1);
  if (!h) return fail('Open this page with the “🎤 Answer by voice” button on your flashcards.');
  try {
    var tag = h[0], b64 = h.slice(1).replace(/-/g, '+').replace(/_/g, '/');
    var bin = atob(b64 + '==='.slice((b64.length + 3) % 4)), bytes = new Uint8Array(bin.length);
    for (var i = 0; i < bin.length; i++) bytes[i] = bin.charCodeAt(i);
    var txt = tag === 'z' ? await new Response(new Blob([bytes]).stream().pipeThrough(new DecompressionStream('deflate-raw'))).text()
                          : new TextDecoder().decode(bytes);
    var P = JSON.parse(txt); window.__CT = P;
    if (P.HEAD) document.getElementById('ct-main-css').insertAdjacentHTML('beforebegin', P.HEAD);
    var s = document.createElement('script'); s.textContent = document.getElementById('ctmain').textContent; document.body.appendChild(s);
  } catch (e) { fail('These flashcards could not open here (' + e.message + '). Please open them again from your flashcards page and tap “🎤 Answer by voice”.'); }
})();
</script>
</body>'''
rep('</body>', LOADER)
open(out, 'w', encoding='utf-8').write(s)
print('wrote', out, len(s), 'bytes')
