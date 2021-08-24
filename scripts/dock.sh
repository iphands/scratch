#!/bin/bash

_do_docked() {
  defaults write .GlobalPreferences com.apple.mouse.scaling -1
  exit 0
}

_do_undocked() {
  defaults write .GlobalPreferences com.apple.mouse.scaling 1.5
  exit 0
}

[[ "$1" == "docked" ]] && _do_docked
[[ "$1" == "undocked" ]] && _do_undocked

echo "Error: Usage: $0 docked|undocked"
exit 1
