# Getting Started

This project currently has no source code in the repository. As code is added, keep documentation up to date using this guide.

## Prerequisites
- bash
- Optional: Node.js, Python, or your chosen language toolchain

## Structure
- `docs/` — documentation sources
- `scripts/` — helper scripts for generating docs

## Generate docs
```bash
bash scripts/generate-docs.sh
```

If your project uses TypeScript, Python, Go, Java, Rust, or Doxygen-supported languages, the generator will attempt to build API references under `docs/generated/`.

## Contributing docs
- Use templates in `docs/templates/`
- Submit docs changes alongside code changes
- Keep examples minimal and runnable