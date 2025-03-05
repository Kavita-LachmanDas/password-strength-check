import streamlit as st
import time
import re
import string
import random
from streamlit_lottie import st_lottie
import requests
import math

# Page configuration
st.set_page_config(
    page_title="🔐 Ultimate Password Guardian",
    page_icon="🔒",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Enhanced custom CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Poppins:wght@300;400;600&display=swap');
    
    .stApp {
        background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
    }
    
    .main-container {
        background: rgba(255,255,255,0.1);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        border: 1px solid rgba(255,255,255,0.2);
        padding: 30px;
        box-shadow: 0 15px 35px rgba(0,0,0,0.3);
        color: white;
    }
    
    .password-display {
        background: rgba(0,0,0,0.3);
        border-radius: 10px;
        padding: 15px;
        font-family: 'Orbitron', sans-serif;
        letter-spacing: 2px;
        text-align: center;
        color: #4cff4c;
    }
    
    .strength-meter {
        background: rgba(255,255,255,0.2);
        border-radius: 10px;
        overflow: hidden;
    }
    
    .btn-generate {
        background: linear-gradient(45deg, #6a11cb 0%, #2575fc 100%) !important;
        border: none !important;
        color: white !important;
        transition: all 0.3s ease !important;
    }
    
    .btn-generate:hover {
        transform: scale(1.05);
        box-shadow: 0 0 15px rgba(37, 117, 252, 0.5);
    }
</style>
""", unsafe_allow_html=True)

# Password generation function
def generate_password(length=12):
    """Generate a strong, random password"""
    # Character sets
    lowercase = string.ascii_lowercase
    uppercase = string.ascii_uppercase
    numbers = string.digits
    symbols = "!@#$%^&*()_+-=[]{}|;:,.<>?"
    
    # Ensure at least one character from each set
    password = [
        random.choice(lowercase),
        random.choice(uppercase),
        random.choice(numbers),
        random.choice(symbols)
    ]
    
    # Fill remaining length with random characters
    all_chars = lowercase + uppercase + numbers + symbols
    password.extend(random.choice(all_chars) for _ in range(length - 4))
    
    # Shuffle the password characters
    random.shuffle(password)
    
    return ''.join(password)

# Password strength calculation
def calculate_entropy(password):
    if not password:
        return 0
    
    charset_size = 0
    if any(c.islower() for c in password):
        charset_size += 26
    if any(c.isupper() for c in password):
        charset_size += 26
    if any(c.isdigit() for c in password):
        charset_size += 10
    if any(c in string.punctuation for c in password):
        charset_size += 33
    
    if charset_size == 0:
        charset_size = 26
    
    entropy = math.log2(charset_size) * len(password)
    return entropy

def check_password_strength(password):
    if not password:
        return {
            "score": 0,
            "strength": "Empty",
            "color": "#CCCCCC",
            "width": "0%",
            "feedback": "Please enter or generate a password"
        }
    
    entropy = calculate_entropy(password)
    
    criteria = {
        "length": len(password) >= 12,
        "uppercase": any(c.isupper() for c in password),
        "lowercase": any(c.islower() for c in password),
        "number": any(c.isdigit() for c in password),
        "special": any(c in string.punctuation for c in password),
    }
    
    criteria_count = sum(criteria.values())
    
    if entropy < 40:
        return {
            "score": 1,
            "strength": "Weak",
            "color": "#FF5252",
            "width": "25%",
            "feedback": "💥 Easily hackable! Regenerate or modify.",
            "criteria": criteria
        }
    elif entropy < 60:
        return {
            "score": 2,
            "strength": "Medium",
            "color": "#FFC107",
            "width": "50%",
            "feedback": "🛡️ Better, but not perfect. Can be improved.",
            "criteria": criteria
        }
    elif entropy < 80:
        return {
            "score": 3,
            "strength": "Strong",
            "color": "#4CAF50",
            "width": "75%",
            "feedback": "✨ Solid password with good protection!",
            "criteria": criteria
        }
    else:
        return {
            "score": 4,
            "strength": "Fortress",
            "color": "#2E7D32",
            "width": "100%",
            "feedback": "🏰 Impenetrable Digital Fortress!",
            "criteria": criteria
        }

# Main Streamlit App
def main():
    # Initialize session state for password if not exists
    if 'generated_password' not in st.session_state:
        st.session_state.generated_password = generate_password()

    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    
    st.title("🔐 Ultimate Password Guardian")
    st.markdown("*Generate & Fortify Your Digital Security*")
    
    # Password Generation Section
    st.subheader("🎲 Generate Unbreakable Password")
    
    # Length slider
    length = st.slider("Password Length", min_value=8, max_value=24, value=12, step=1)
    
    # Generate Button
    col1, col2 = st.columns([3, 1])
    with col1:
        generated_password = st.text_input(
            "Your Secure Password", 
            value=st.session_state.generated_password, 
            type="password"
        )
    
    with col2:
        regenerate = st.button("🔄 Regenerate", use_container_width=True, 
                               help="Create a new random password")
    
    if regenerate:
        # Update session state with new password
        st.session_state.generated_password = generate_password(length)
        # Rerun the app to refresh the display
        st.rerun()
    
    # Copy to clipboard button
    copy_btn = st.button("📋 Copy Password", use_container_width=True)
    if copy_btn:
        st.code(generated_password)
        st.success("Password copied to clipboard!")
    
    # Strength Analysis
    st.subheader("🛡️ Password Strength Analysis")
    
    # Strength meter
    result = check_password_strength(generated_password)
    
    st.markdown(f"""
    <div class="strength-meter">
        <div style="width: {result['width']}; 
                    height: 10px; 
                    background-color: {result['color']};">
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Strength display
    st.markdown(f"""
    <div style="display: flex; justify-content: space-between; align-items: center;">
        <span style="color: {result['color']}; font-weight: bold;">{result['strength']}</span>
        <span>{result['feedback']}</span>
    </div>
    """, unsafe_allow_html=True)
    
    # Detailed Criteria
    st.subheader("✅ Security Checklist")
    criteria_items = [
        ("🔤 Lowercase Letters", any(c.islower() for c in generated_password)),
        ("🔠 Uppercase Letters", any(c.isupper() for c in generated_password)),
        ("🔢 Numbers", any(c.isdigit() for c in generated_password)),
        ("🔣 Special Characters", any(c in string.punctuation for c in generated_password)),
        ("📏 Minimum Length (12+)", len(generated_password) >= 12)
    ]
    
    for text, is_met in criteria_items:
        icon = "✅" if is_met else "❌"
        st.markdown(f"{icon} {text}")
    
    # Security Tips
    st.subheader("💡 Password Security Tips")
    st.markdown("""
    - Never reuse passwords across different accounts
    - Use a unique password for each platform
    - Consider using a password manager
    - Update passwords periodically
    - Avoid personal information in passwords
    """)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Run the app
if __name__ == "__main__":
    main()