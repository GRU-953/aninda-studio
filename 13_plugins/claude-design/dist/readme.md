# Aninda Studio — Claude Design project

Generated. The source of truth is the repository:
<https://github.com/GRU-953/aninda-studio>

- 18 preview cards in `guidelines/`
- 6 colour ramps of 11 steps in `tokens/`
- 4 themes: light, dark, high-contrast light, high-contrast dark
- 1 stylesheet, `styles.css`, holding the tokens, the component layer and the
  three inlined typefaces

To update this project, change the tokens in the repository, run
`13_plugins/claude-design/build.py`, and push the `dist/` folder. Editing a file
here by hand is undone by the next build, and nothing here will report that the
remote copy has fallen behind — which is why the build is the route.
