#!/bin/bash
set -e
# cargo build --release -Z strip=symbols
mkdir -p ~/bin
cargo build --release
strip ./target/release/dirchomp
cp ./target/release/dirchomp ~/bin/
