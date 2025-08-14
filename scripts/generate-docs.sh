#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")"/.. && pwd)
OUT_DIR="$ROOT_DIR/docs/generated"
mkdir -p "$OUT_DIR"

log() { echo "[docs] $*"; }

# Detect languages
has_ts=false
has_py=false
has_go=false
has_java=false
has_rust=false
has_doxygen=false

cd "$ROOT_DIR"

# Portable detection using find
if find . -type f \( -name '*.ts' -o -name '*.tsx' \) -print -quit | grep -q .; then has_ts=true; fi
if find . -type f -name '*.py' -print -quit | grep -q .; then has_py=true; fi
if [ -f go.mod ] || [ -d "$ROOT_DIR"/cmd ] || find . -type f -name '*.go' -print -quit | grep -q .; then has_go=true; fi
if find src -type f -name '*.java' -print -quit 2>/dev/null | grep -q .; then has_java=true; fi
if [ -f Cargo.toml ] || find . -type f -name '*.rs' -print -quit | grep -q .; then has_rust=true; fi
if [ -f Doxyfile ] || command -v doxygen >/dev/null 2>&1; then has_doxygen=true; fi

log "Output: $OUT_DIR"

# TypeScript via typedoc
if $has_ts; then
  if npx --yes typedoc --version >/dev/null 2>&1; then
    log "Generating TypeScript docs with TypeDoc"
    npx --yes typedoc --out "$OUT_DIR/typescript" || log "TypeDoc failed"
  else
    log "TypeDoc not found. Install with: npm i -D typedoc"
  fi
fi

# Python via pdoc
if $has_py; then
  if python -c "import pdoc" >/dev/null 2>&1; then
    log "Generating Python docs with pdoc"
    python -m pdoc -o "$OUT_DIR/python" . || log "pdoc failed"
  else
    log "pdoc not found. Install with: pip install pdoc"
  fi
fi

# Go via godoc (static site via pkgsite is complex; provide pointers)
if $has_go; then
  log "Go project detected. Consider using 'go doc' or 'pkgsite'."
  go list ./... >/dev/null 2>&1 && go doc ./... | sed 's/^/[go] /' > "$OUT_DIR/go.txt" || true
fi

# Java via javadoc
if $has_java; then
  if command -v javadoc >/dev/null 2>&1; then
    log "Generating Java docs with javadoc"
    mkdir -p "$OUT_DIR/java"
    javadoc -d "$OUT_DIR/java" -sourcepath src $(find src -name '*.java' | tr '\n' ' ') || log "javadoc failed"
  else
    log "javadoc not found. Install JDK to enable."
  fi
fi

# Rust via rustdoc
if $has_rust; then
  if command -v cargo >/dev/null 2>&1; then
    log "Generating Rust docs with cargo doc"
    cargo doc --no-deps || log "cargo doc failed"
    mkdir -p "$OUT_DIR/rust"
    cp -r target/doc/* "$OUT_DIR/rust" 2>/dev/null || true
  else
    log "cargo not found. Install Rust toolchain to enable."
  fi
fi

# Doxygen (for C/C++ and others)
if $has_doxygen; then
  if command -v doxygen >/dev/null 2>&1 && [ -f Doxyfile ]; then
    log "Generating docs with Doxygen"
    doxygen Doxyfile || log "doxygen failed"
  else
    log "Doxygen not fully configured. Provide a Doxyfile to enable."
  fi
fi

log "Done."