# Style Preferences (Recommended, Not Mandatory)

Apply where the repo's own `AGENTS.md`, style guide or Project Policy Hook says
nothing. The repo's rules win; never rewrite existing code only to match these.

1. **No hash addresses for data objects**: name them by readable names, dates and sequence numbers.
2. **No pandas in compute-graph code** unless the architecture already uses it there; prefer polars, and compute with numpy, polars and torch.
3. **No hard-coded run paths**: every path comes from a parameter or a config.
4. **Interface style**: each logical module exposes one clear interface; its functions and features are clearly defined behind it.
5. **Parallelise compute-heavy work** wherever it can run in parallel.
6. **Comments in English**:
   - file header at most 5 lines, lines of about 80 characters at most;
   - function comment on one line;
   - short explanatory comments only where needed, never long essays.
7. **Large files are gitignored.**
