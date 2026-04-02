# Password Strength & Entropy Analyzer

## Overview
A lightweight, desktop-based utility designed to evaluate password resilience in real-time. Unlike basic regex validators, this tool implements a custom scoring algorithm based on **Shannon Entropy** and pattern recognition to provide actionable security feedback.

Built as part of a broader initiative to understand authentication vulnerabilities and secure input handling, this project bridges the gap between theoretical cryptography concepts and practical application development.

## Key Features
- **Real-Time Analysis**: Instant feedback on password strength as the user types.
- **Entropy-Based Scoring**: Calculates bits of entropy to determine cryptographic strength, rather than relying solely on character presence.
- **Pattern Detection**: Identifies and penalizes common weak patterns (e.g., sequential numbers, keyboard walks, repeated characters).
- **Actionable Feedback**: Provides specific recommendations for improvement (e.g., "Increase length to 12+ chars," "Avoid dictionary words").
- **Secure Design**: Implements memory-safe practices; passwords are processed in volatile memory and never logged or persisted.

## Tech Stack
- **Language**: Python 3.10+
- **GUI Framework**: Tkinter (Standard Library)
- **Architecture**: MVC-inspired separation of UI and business logic for modularity and testability.

## Installation & Usage
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/py-password-audit-tool.git
   cd py-password-audit-tool
