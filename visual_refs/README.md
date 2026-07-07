# Visual References

`visual_refs/` stores internal visual references for paper figure design. It is not a raw-data archive and not a publication-ready asset directory.

Rules:

- Every saved visual reference needs a matching figure card.
- External paper figures need citation and release notes.
- Keep raw experiment data and generated scientific outputs in the project tree.
- Register reusable or paper-bound visual references in `registry/figures.yaml`.
- If a visual reference is reconstructed into editable assets, keep the source
  visual as a local-only reference unless it is explicitly sanitized. Store the
  reconstruction prompt, manifest, QA summary, and reproduction note with the
  current project's closeout assets, not as raw binaries in `visual_refs/`.
