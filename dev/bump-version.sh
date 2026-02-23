#!/bin/bash

set -e

if [ $# -ne 1 ]; then
    echo "Usage: $0 <version>"
    echo "Example: $0 1.0.0"
    exit 1
fi

VERSION="$1"

# Update version in pyproject.toml
echo "Updating version in pyproject.toml to $VERSION..."
sed -i '' "s/^version = \"[0-9]*\.[0-9]*\.[0-9]*\"/version = \"$VERSION\"/" pyproject.toml

# Update version in manifest.yaml
echo "Updating version in manifest.yaml to $VERSION..."
sed -i '' "s/^version: [0-9]*\.[0-9]*\.[0-9]*/version: $VERSION/" manifest.yaml

# Update uv.lock
echo "Updating uv.lock..."
uv sync

echo "Version updated successfully to $VERSION"
echo ""
echo "Updated files:"
echo "- pyproject.toml"
echo "- manifest.yaml"
echo "- uv.lock"
