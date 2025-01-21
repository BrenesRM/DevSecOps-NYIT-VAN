#!/bin/bash

# Check if curl is installed
if command -v curl >/dev/null 2>&1; then
  echo "curl is already installed"
else
  echo "curl is not installed. Installing curl..."
  sudo apt update && sudo apt install -y curl
  echo "curl has been installed"
fi
