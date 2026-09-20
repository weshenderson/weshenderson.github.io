#!/usr/bin/env bash
# Quick & Dirty visual check for all build metadata artifacts.

echo '** Pulling main **'
git pull origin main
echo -e '\n'

echo '** Querying buildData -- Website (html) **'
head -n8 public/index.html
read -p "Press [Enter] to continue..."
echo

echo '** Querying buildData -- Website (css) **'
head -n8 public/assets/css/main.css
read -p "Press [Enter] to continue..."
echo

echo '** Querying buildData -- Resume (html) **'
head -n8 public/resumes/resume.html
read -p "Press [Enter] to continue..."
echo

echo '** Querying buildData -- Resume (json) **'
jq .meta.buildData ./public/resumes/resume.json
read -p "Press [Enter] to continue..."
echo

echo '** Querying buildData -- Resume (md) **'
head -n8 public/resumes/resume.md
read -p "Press [Enter] to continue..."
echo

echo '** Querying buildData -- Resume (docx) **'
./tools/metadata_viewer_docx.py | awk '/Comments/ {print $2,$3,$4,$5,$6,$7}'
read -p "Press [Enter] to continue..."
echo

echo '** Querying buildData -- Resume (pdf) **'
./tools/metadata_viewer_pdf.py | awk '/Keywords/ {print $2,$3,$4,$5,$6,$7}'
read -p "Press [Enter] to continue..."
echo
