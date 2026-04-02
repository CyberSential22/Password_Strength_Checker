"""
Password Strength Analyzer - Security Engineer Edition
======================================================
A robust, GUI-based tool to evaluate password complexity and entropy.

Features:
- Real-time entropy calculation (bits).
- Pattern detection (sequences, repeats, common strings).
- Actionable security feedback.
- Visual strength indicator.
- Single-file, no external dependencies.

How to run:
1. Ensure Python 3.10+ is installed.
2. Run command: `python password_checker.py`
"""

import tkinter as tk
from tkinter import ttk
import math
import re
import string

class PasswordAnalyzer:
    """Business logic for password strength analysis and entropy calculation."""

    # Character sets for pool size calculation
    CHARSETS = {
        'lowercase': (string.ascii_lowercase, 26),
        'uppercase': (string.ascii_uppercase, 26),
        'digits': (string.digits, 10),
        'special': (string.punctuation, 32)
    }

    # Common keyboard/typical patterns to penalize
    COMMON_PATTERNS = [
        "123456", "password", "qwerty", "admin", "welcome", "login",
        "12345678", "123456789", "abcdef", "asdfgh"
    ]

    @staticmethod
    def calculate_entropy(password: str) -> tuple[float, float, list[str]]:
        """
        Calculates raw bits of entropy and adjusted strength based on patterns.
        Returns: (raw_entropy, effective_entropy, suggestions)
        """
        if not password:
            return 0.0, 0.0, ["Start typing to analyze..."]

        length = len(password)
        found_pools = set()
        pool_size = 0

        # Determine the total pool size based on character variety
        if any(c in string.ascii_lowercase for c in password):
            pool_size += 26
            found_pools.add('lowercase')
        if any(c in string.ascii_uppercase for c in password):
            pool_size += 26
            found_pools.add('uppercase')
        if any(c in string.digits for c in password):
            pool_size += 10
            found_pools.add('digits')
        if any(c in string.punctuation or c in " " for c in password):
            pool_size += 33 # 32 std punctuation + space
            found_pools.add('special')

        # Fallback for unknown characters (e.g., unicode)
        if pool_size == 0:
            pool_size = 10 # Minimal assumption

        # Raw Entropy Formula: log2(PoolSize ^ Length)
        raw_entropy = length * math.log2(pool_size) if pool_size > 0 else 0

        # Analysis for patterns and deductions
        effective_entropy = raw_entropy
        suggestions = []

        # 1. Length Penalties/Bonuses (Subjective adjustments to 'effective' bits)
        if length < 8:
            effective_entropy *= 0.5
            suggestions.append("⚠️ Critical: Length is too short (min 8 recommended).")
        elif length < 12:
            suggestions.append("💡 Tip: Increase length to 12+ for better security.")
        elif length > 16:
            suggestions.append("✅ Great: Password length is excellent.")

        # 2. Diversity Checks
        missing = []
        if 'uppercase' not in found_pools: missing.append("uppercase letters")
        if 'digits' not in found_pools: missing.append("numbers")
        if 'special' not in found_pools: missing.append("special characters")
        
        if missing:
            suggestions.append(f"🔒 Add {', '.join(missing)} to increase complexity.")

        # 3. Repeated Characters (e.g., "aaaaaaa")
        # If the same character makes up a large % of the password, reduce effective entropy
        unique_chars = len(set(password.lower()))
        if length > 3 and unique_chars / length < 0.3:
            effective_entropy *= 0.4
            suggestions.append("⚠️ Avoid repetitive characters.")

        # 4. Sequential Patterns (e.g., "123", "abc")
        sequential_count = 0
        for i in range(len(password) - 2):
            # Check ASCII sequence
            if (ord(password[i+1]) == ord(password[i]) + 1 and 
                ord(password[i+2]) == ord(password[i+1]) + 1):
                sequential_count += 1
        
        if sequential_count > 0:
            effective_entropy -= (sequential_count * 5) # Deduct roughly 5 bits per sequence
            suggestions.append("⚠️ Sequence detected (e.g., '123' or 'abc').")

        # 5. Common Strings
        for pattern in PasswordAnalyzer.COMMON_PATTERNS:
            if pattern in password.lower():
                effective_entropy *= 0.2
                suggestions.append(f"❌ Found common pattern: '{pattern}'.")
                break

        # Sanitize effective entropy
        effective_entropy = max(0, effective_entropy)
        
        if not suggestions and effective_entropy > 60:
            suggestions.append("✨ Perfectly balanced! Strong password.")

        return raw_entropy, effective_entropy, suggestions

class PasswordStrengthApp:
    """Tkinter UI Wrapper."""

    def __init__(self, root):
        self.root = root
        self.root.title("Antigravity Password Analyzer v1.0")
        self.root.geometry("500x550")
        self.root.resizable(False, False)
        
        # Configure Styles
        self.style = ttk.Style()
        self.style.theme_use('clam') # Using clam for better customization visibility
        
        # Color Palette
        self.bg_color = "#f5f7fa"
        self.card_color = "#ffffff"
        self.text_primary = "#2d3436"
        self.text_secondary = "#636e72"
        self.accent_red = "#e74c3c"
        self.accent_yellow = "#f1c40f"
        self.accent_green = "#27ae60"

        self.root.configure(bg=self.bg_color)
        
        self.setup_ui()
        self.analyzer = PasswordAnalyzer()

    def setup_ui(self):
        # Main Container
        main_frame = tk.Frame(self.root, bg=self.bg_color, padx=30, pady=30)
        main_frame.pack(fill="both", expand=True)

        # Header
        header = tk.Label(main_frame, text="Security Analyzer", 
                         font=("Segoe UI Semibold", 22), bg=self.bg_color, fg=self.text_primary)
        header.pack(pady=(0, 5))
        
        subtext = tk.Label(main_frame, text="Measure entropy and structural integrity",
                          font=("Segoe UI", 10), bg=self.bg_color, fg=self.text_secondary)
        subtext.pack(pady=(0, 20))

        # Input Card
        card = tk.Frame(main_frame, bg=self.card_color, padx=20, pady=20, 
                       highlightbackground="#dcdde1", highlightthickness=1)
        card.pack(fill="x")

        # Entry Label
        tk.Label(card, text="Enter Password", font=("Segoe UI", 10, "bold"), 
                 bg=self.card_color, fg=self.text_primary).pack(anchor="w")

        # Password Entry field
        self.password_var = tk.StringVar()
        self.password_var.trace_add("write", self.on_password_change)
        
        self.entry = tk.Entry(card, textvariable=self.password_var, show="●", 
                             font=("Consolas", 14), bd=0, highlightthickness=1,
                             highlightbackground="#dcdde1", highlightcolor="#3498db")
        self.entry.pack(fill="x", pady=(10, 10), ipady=8)
        self.entry.focus_set()

        # Visibility Toggle
        self.show_password = tk.BooleanVar(value=False)
        self.toggle_btn = tk.Checkbutton(card, text="Show password", variable=self.show_password,
                                        command=self.toggle_visibility, bg=self.card_color,
                                        activebackground=self.card_color, font=("Segoe UI", 9))
        self.toggle_btn.pack(anchor="w")

        # Strength Meter (Progress Bar)
        self.meter_frame = tk.Frame(main_frame, bg=self.bg_color)
        self.meter_frame.pack(fill="x", pady=(20, 0))
        
        tk.Label(self.meter_frame, text="Estimated Strength", font=("Segoe UI", 10, "bold"),
                 bg=self.bg_color, fg=self.text_primary).pack(side="left")
        
        self.strength_label = tk.Label(self.meter_frame, text="Awaiting input...", 
                                      font=("Segoe UI", 10, "bold"), bg=self.bg_color, fg=self.text_secondary)
        self.strength_label.pack(side="right")

        # Custom Progress Bar (Canvas for color control)
        self.canvas = tk.Canvas(main_frame, height=12, bg="#dfe6e9", 
                               highlightthickness=0, bd=0)
        self.canvas.pack(fill="x", pady=(5, 15))
        self.bar = self.canvas.create_rectangle(0, 0, 0, 12, fill=self.accent_red, width=0)

        # Entropy Info
        self.info_frame = tk.Frame(main_frame, bg=self.bg_color)
        self.info_frame.pack(fill="x")
        
        self.entropy_val = tk.Label(self.info_frame, text="Entropy: 0 bits", 
                                   font=("Segoe UI", 10), bg=self.bg_color, fg=self.text_secondary)
        self.entropy_val.pack(anchor="w")

        # Feedback Panel
        tk.Label(main_frame, text="Feedback & Suggestions", font=("Segoe UI", 11, "bold"),
                 bg=self.bg_color, fg=self.text_primary).pack(anchor="w", pady=(20, 5))
        
        self.feedback_box = tk.Text(main_frame, height=8, font=("Segoe UI", 10),
                                   bg="#fdfdfd", fg=self.text_primary, bd=0, 
                                   highlightthickness=1, highlightbackground="#dcdde1",
                                   padx=10, pady=10)
        self.feedback_box.pack(fill="both")
        self.feedback_box.config(state="disabled")

    def toggle_visibility(self):
        if self.show_password.get():
            self.entry.config(show="")
        else:
            self.entry.config(show="●")

    def on_password_change(self, *args):
        password = self.password_var.get()
        
        # Run Analysis
        raw_e, effective_e, suggestions = self.analyzer.calculate_entropy(password)
        
        # Update UI
        self.update_meter(effective_e)
        self.update_feedback(suggestions, raw_e, effective_e)
        
        # Security: don't let password sit in trace longer than needed
        # (Though StringVar handles this, we avoid deep copies)

    def update_meter(self, entropy):
        # Ensure canvas width is updated
        self.root.update_idletasks()
        
        # Progress logic (0 to 100 bits scale, most systems consider 80+ very strong)
        progress = min(entropy / 80.0, 1.0)
        width = self.canvas.winfo_width()
        
        if width <= 1: # Fallback if not yet rendered
            width = 440 
        
        color = self.accent_red
        classification = "Weak"
        
        if entropy < 28:
            color = self.accent_red
            classification = "Weak"
        elif 28 <= entropy < 60:
            color = self.accent_yellow
            classification = "Medium"
        else:
            color = self.accent_green
            classification = "Strong"

        if not self.password_var.get():
            progress = 0
            classification = "Empty"
            color = "#dfe6e9"
        
        # Update Canvas
        self.canvas.coords(self.bar, 0, 0, width * progress, 12)
        self.canvas.itemconfig(self.bar, fill=color)
        self.strength_label.config(text=classification, fg=color if classification != "Empty" else self.text_secondary)

    def update_feedback(self, suggestions, raw_e, effective_e):
        self.entropy_val.config(text=f"Entropy: {effective_e:.1f} bits (Raw: {raw_e:.1f})")
        
        self.feedback_box.config(state="normal")
        self.feedback_box.delete("1.0", tk.END)
        
        for s in suggestions:
            self.feedback_box.insert(tk.END, f"• {s}\n")
            
        self.feedback_box.config(state="disabled")

if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordStrengthApp(root)
    
    # Custom closure to clear password from memory on exit (best effort)
    def on_closing():
        app.password_var.set("")
        root.destroy()
        
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()
