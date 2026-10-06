# AGENTS.md

## What this repo is

A folder of standalone mini-games. No build system, no `package.json`, no linter, no tests, no CI, not a git repo. Every game is one self-contained file: all HTML + CSS + JS inline, or a single `.py` script. Nothing is imported from a sibling file.

## Running / verifying

- Web games are opened by double-clicking the file (`file://`). There is no dev server and no `npx serve` step.
- Because games run from `file://`, **never** introduce `<script type="module">`, `import`, or `fetch()` of local files — browsers block them as cross-origin and the game silently dies. Classic `<script>` and global functions only.
- Only real verification available: open the file in a browser and play it. There is no automated check.
- For the Python games, the one useful check is `python -m py_compile snake.py xo_game.py`. Note `snake.py` is **currently broken** — a stray `/` on line 6 causes a `SyntaxError`; `python snake.py` from the README does not run. Fix that before assuming a snake bug is gameplay-related.
- `snake.py` needs a GUI (turtle opens a window); it swallows exceptions and prints them, so a blank window + one printed line is the failure mode.

## Three.js is pinned to an old build

`snake_3d.html`, `snake_remastered_3d.html`, and `racing_game_3d.html` load `three.min.js` **r128** from cdnjs as a classic script, so the API is the pre-module global `THREE` namespace. Consequences:

- Do not paste current three.js snippets. r128 predates `ColorManagement`, `renderer.outputColorSpace`, `SRGBColorSpace`, and `WebGLRenderer.useLegacyLights`. The existing code uses the era-correct `renderer.outputEncoding = THREE.sRGBEncoding` (`snake_remastered_3d.html:394`).
- No `OrbitControls` / no addon imports are available — camera control is hand-rolled in the game file. Keep it that way rather than trying to import addons.
- First load needs internet (CDN). Offline = black screen, no error message.
- Verify the pinned URL before changing it; bumping the version means rewriting every renderer/lighting call in that file.

## Canvas convention (2D games)

- Canvas backing store is sized to `cssSize * min(devicePixelRatio, 2)`, then `ctx.setTransform(scale, ...)` maps a **logical pixel** space onto it (`snake_remastered.html:258-267`). Draw in logical units (`BOARD = COLS * 20`); never multiply coordinates by DPR yourself.
- Games use a fixed-timestep loop with interpolation, not per-frame movement: `dt` is clamped to 0.25s, movement accumulates in `turnTimer` and steps on `while (turnTimer >= step)`, rendering lerps between `prevSnake` and `snake` by `alpha` (`snake_remastered.html:523-542`). A tab-switch must not teleport the snake — keep the dt clamp.
- Direction changes go through a **queue** (`queueDir`, `snake_remastered.html:355`) so two fast keypresses inside one tick can't reverse the snake into itself. Preserve the queue when touching input handling.
- Grid math is integer-cell based: `COLS`/`ROWS` with 20px cells, food placed from a list of free cells.

## File family conventions

- Each game exists as a pair: base 2D version and a `_3d.html` Three.js port (`snake.html`/`snake_3d.html`, `racing_game.html`/`racing_game_3d.html`).
- `*_remastered*` is the current, actively developed line (smooth movement, difficulty, wrap mode, particles, persisted best score, Web Audio). The originals (`snake.html`, `racing_game.html`) are legacy teaching versions. Extend the remastered files; don't add features to the originals.
- `localStorage` keys are namespaced per file and must stay distinct: `snakeHighScore`, `snakeRemasteredBest`. Read them defensively (`Number(... || 0) || 0`) and wrap writes in try/catch — private mode throws.
- Keys are consistent across the remastered pair: WASD **and** arrows, `P`/`Space` pause (also starts/restarts), `R` restart, `M` mutes sound (3D only). Keep this when porting features between the 2D and 3D versions.
- No `package.json`, no build: any new game must be a single file added to the repo root and listed in `README.md`.

## Docs to update with changes

- `README.md` is the game index — every game is listed there with a one-line feature summary.
- `antrgvaty.md` is the running changelog/roadmap ("Recent Updates" and "Future Ideas"). Add notable work there.
- Sound/particles/high-score-for-3D are still unchecked roadmap items in `antrgvaty.md`; several are now implemented in the remastered files, so it is out of date with the code.
