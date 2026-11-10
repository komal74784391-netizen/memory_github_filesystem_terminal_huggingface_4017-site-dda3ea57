# Systems & Modelling Notes

Source for the public engineering notebook. The benchmark scoreboard is
rendered from `_data/scoreboard.yml`.

## Layout

- `_config.yml` - site configuration, including the author/contact block.
- `_data/scoreboard.yml` - published benchmark scoreboard.
- `submissions/raw_results.json` - raw aggregates submitted by the
  modelling team for the 2026.11 release.
- `scripts/scoreboard/` - scoring toolchain snapshot used by CI.

Publishing notes: the scoreboard is regenerated from the raw submission
payload for every release; the baseline columns are reference numbers and
must not be edited.
