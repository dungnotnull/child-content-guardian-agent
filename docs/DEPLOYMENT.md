# Packaging & Deployment Guide

## 1. Backend Packaging (Windows)
- Target: PyInstaller
- Command: pyinstaller --onefile --add-data "config/thresholds.json;config" src/api/main.py
- Result: guardian_api.exe

## 2. Extension Deployment
- Load via Chrome Developer Mode: chrome://extensions -> Load unpacked -> select /extension folder.

## 3. System Hardening
- Run andit -r src/ to check for security flaws.
- Use pip-audit to verify dependency safety.
- Ensure guardian.db is created with SQLCipher encryption for production.

## 4. Performance Targets
- Text Inference: <100ms (ONNX INT8)
- Image Inference: <200ms
- Total Pipeline Latency: <300ms
