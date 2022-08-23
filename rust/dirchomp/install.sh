#!/bin/bash
set -e
# cargo build --release -Z strip=symbols
mkdir -p ~/bin
cargo build --release
strip ./target/release/dirchomp
rm ~/bin/dirchomp
cp ./target/release/dirchomp ~/bin/
