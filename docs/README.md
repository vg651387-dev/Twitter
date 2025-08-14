# Twitter Documentation

This repository currently contains minimal source files. This documentation scaffold is prepared to host complete docs as code is added.

- **Getting Started**: See `docs/getting-started.md` for environment setup and common workflows
- **Public APIs**: See `docs/api/README.md` for endpoints and library APIs
- **Components**: See `docs/components/README.md` for UI/component documentation
- **Examples**: See `docs/examples/README.md` for runnable examples and snippets
- **Templates**: See `docs/templates/` for authoring templates

## Generate docs (auto)
- Run: `bash scripts/generate-docs.sh`
- Output will be placed in `docs/generated/` when supported project types are detected (TypeScript, Python, Go, Java, Rust, PHP, C/C++ via Doxygen)

## Authoring conventions
- Prefer clear, task-oriented explanations over internal details
- Include short examples for every API/function/component
- Show parameter names, types, and default values
- Document return values and error cases
- Link cross-references using relative paths
- Keep examples minimal and runnable where possible