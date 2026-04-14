#!/bin/bash
# VLUXGEN v3.0 Installation Script
# Developed by Sriram (Cyber Pasanga)

RED='\033[0;31m'
GREEN='\033[0;32m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${CYAN}--------------------------------------------------${NC}"
echo -e "${GREEN}      VLUXGEN v3.0 - Installer Started          ${NC}"
echo -e "${CYAN}--------------------------------------------------${NC}"

# Check for Python
if ! command -v python3 &> /dev/null
then
    echo -e "${RED}[!] Python3 not found. Please install it first.${NC}"
    exit 1
fi

# Check for pip
if ! command -v pip3 &> /dev/null
then
    echo -e "${YELLOW}[*] pip3 not found. Trying to install...${NC}"
    sudo apt update && sudo apt install python3-pip -y
fi

echo -e "${YELLOW}[*] Installing dependencies...${NC}"
pip3 install -r requirements.txt

if [ $? -eq 0 ]; then
    echo -e "${GREEN}[✓] Dependencies installed successfully!${NC}"
else
    echo -e "${RED}[!] Failed to install dependencies. Check your connection.${NC}"
    exit 1
fi

echo -e "${YELLOW}[*] Setting permissions...${NC}"
chmod +x vluxgen.py

echo -e "${CYAN}--------------------------------------------------${NC}"
echo -e "${GREEN}      VLUXGEN v3.0 Installed Successfully!       ${NC}"
echo -e "${YELLOW}      Usage: python3 vluxgen.py                  ${NC}"
echo -e "${CYAN}--------------------------------------------------${NC}"
