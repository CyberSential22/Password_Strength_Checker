# 🛡️ CyberSential22 - Password Strength Checker

A professional-grade, entropy-based password analyzer for security engineers. This tool measures both mathematical **Shannon Entropy** and structural integrity to provide deep security feedback. Unlike basic validators, it bridges the gap between cryptographical theory and practical application.

## 🚀 Key Features
- **Real-Time Analysis**: Instant feedback on password resilience as the user types.
- **Entropy-Based Scoring**: Measures raw and effective bits to determine cryptographic strength.
- **Pattern Detection**: Identifies and penalizes sequential strings, common patterns (e.g., keyboard walks), and character repetition.
- **Actionable Feedback**: Provides specific, real-time suggestions to improve security (e.g., "Add symbols," "Avoid common patterns").
- **Dual Interfaces**: Support for both a modern **Flask Web Application** and a **Desktop GUI (Tkinter)**.
- **Secure Design**: Passwords are processed in volatile memory and are never persisted or logged.

---

## 🛠️ Installation

### 1. Requirements
Ensure you have **Python 3.10+** installed.

### 2. Setup (Automatic)
The project includes a server launcher that manages your environment for you. We recommend using it to install dependencies:
1. Run `run_server.bat`. 
2. This will automatically create a `.venv` virtual environment and install the required packages from `requirements.txt`.

### 3. Setup (Manual)
```ps1
# Create virtual environment
python -m venv .venv

# Activate (Windows)
.\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

---

## 💻 How to Run

### 🌐 Web Application (Flask)
- **Fast Launch**: Run `quick_server.bat` to skip initialization and jump straight into the server.
- **Full Refresh**: Run `run_server.bat` for dependency checks and full server initialization.
- The server will run at: `http://127.0.0.1:5000`

### 🖥️ Desktop UI (GUI)
Simply run the Python script directly:
```ps1
python password_checker.py
```

---

## 📦 Project Structure
- `app.py`: Flask backend and core analysis logic.
- `password_checker.py`: Standalone desktop GUI (Tkinter).
- `requirements.txt`: Project dependencies.
- `run_server.bat` & `quick_server.bat`: Utility scripts for environment management.
- `templates/`: HTML frontend for the Flask app.

---

## ⚖️ License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
