#!/usr/bin/env bash
# Fetch the exact native Debian adapter packages required by ring ABI major 2.
set -euo pipefail

if [[ $# -ne 4 ]]; then
    printf '%s\n' "usage: $0 REPOSITORY TAG ARCHITECTURE DESTINATION" >&2
    exit 2
fi

repository=$1
tag=$2
architecture=$3
destination=$4

case "$architecture" in
    amd64 | arm64) ;;
    *)
        printf 'unsupported Debian architecture: %s\n' "$architecture" >&2
        exit 2
        ;;
esac

rm -rf "$destination"
mkdir -p "$destination"

gh release download "$tag" --repo "$repository" --dir "$destination" \
    --pattern "librptadv-samplerate-adapter1_*_${architecture}.deb" \
    --pattern "librptadv-samplerate-adapter-dev_*_${architecture}.deb"

runtime=("$destination"/librptadv-samplerate-adapter1_*_"$architecture".deb)
development=("$destination"/librptadv-samplerate-adapter-dev_*_"$architecture".deb)

if [[ ${#runtime[@]} -ne 1 || ! -f ${runtime[0]} ]]; then
    printf 'expected exactly one runtime adapter package for %s from %s %s\n' \
        "$architecture" "$repository" "$tag" >&2
    exit 1
fi

if [[ ${#development[@]} -ne 1 || ! -f ${development[0]} ]]; then
    printf 'expected exactly one development adapter package for %s from %s %s\n' \
        "$architecture" "$repository" "$tag" >&2
    exit 1
fi
