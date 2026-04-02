from flask import Flask, render_template, request, jsonify
import math
import string

app = Flask(__name__)

class PasswordAnalyzer:
    """Security Engineer's custom entropy and pattern analyzer."""
    
    COMMON_PATTERNS = [
        "123456", "password", "qwerty", "admin", "welcome", "login",
        "12345678", "123456789", "abcdef", "asdfgh"
    ]

    @staticmethod
    def analyze(password: str):
        if not password:
            return {"raw_entropy": 0, "effective_entropy": 0, "suggestions": ["Waiting for input..."], "status": "Empty"}

        length = len(password)
        pool_size = 0
        found_pools = set()

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
            pool_size += 33
            found_pools.add('special')

        if pool_size == 0: pool_size = 10

        raw_entropy = length * math.log2(pool_size) if pool_size > 0 else 0
        effective_entropy = raw_entropy
        suggestions = []

        # Logic & Penalties
        if length < 8:
            effective_entropy *= 0.5
            suggestions.append("⚠️ Length is critically low (min 8).")
        elif length < 12:
            suggestions.append("💡 Increase length to 12+ for better security.")
        
        missing = []
        if 'uppercase' not in found_pools: missing.append("uppercase")
        if 'digits' not in found_pools: missing.append("numbers")
        if 'special' not in found_pools: missing.append("symbols")
        if missing: suggestions.append(f"🔒 Add {', '.join(missing)}.")

        unique_chars = len(set(password.lower()))
        if length > 3 and unique_chars / length < 0.3:
            effective_entropy *= 0.4
            suggestions.append("⚠️ High repetition detected.")

        for pattern in PasswordAnalyzer.COMMON_PATTERNS:
            if pattern in password.lower():
                effective_entropy *= 0.2
                suggestions.append(f"❌ Common pattern found: '{pattern}'.")
                break

        effective_entropy = max(0, effective_entropy)
        
        status = "Weak"
        if effective_entropy >= 60: status = "Strong"
        elif effective_entropy >= 28: status = "Medium"

        if not suggestions and effective_entropy > 60:
            suggestions.append("✨ Perfectly secure!")

        return {
            "raw_entropy": round(raw_entropy, 1),
            "effective_entropy": round(effective_entropy, 1),
            "suggestions": suggestions,
            "status": status
        }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def api_analyze():
    data = request.get_json()
    password = data.get('password', '')
    result = PasswordAnalyzer.analyze(password)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
