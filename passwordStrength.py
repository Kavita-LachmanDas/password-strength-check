import streamlit as st
import time
import re
import string
import random
import math

# Page configuration
st.set_page_config(
    page_title="🔐 Password Guardian",
    page_icon="🔒",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Poppins:wght@300;400;600&display=swap');
    
    .stApp {
        background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
        color: white;
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
    
    .strength-meter {
        background: rgba(255,255,255,0.2);
        border-radius: 10px;
        overflow: hidden;
        height: 15px;
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
            "color": "white",
            "width": "0%",
            "feedback": "Please enter a password"
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
            "strength": "Weak 🚨",
            "color": "white",
            "width": "25%",
            "feedback": "Easily hackable! Regenerate or modify.",
            "criteria": criteria
        }
    elif entropy < 60:
        return {
            "score": 2,
            "strength": "Medium 🛡️",
            "color": "white",
            "width": "50%",
            "feedback": "Better, but can be improved.",
            "criteria": criteria
        }
    elif entropy < 80:
        return {
            "score": 3,
            "strength": "Strong 💪",
            "color": "white",
            "width": "75%",
            "feedback": "Solid password with good protection!",
            "criteria": criteria
        }
    else:
        return {
            "score": 4,
            "strength": "Fortress 🏰",
            "color": "white",
            "width": "100%",
            "feedback": "Impenetrable Digital Fortress!",
            "criteria": criteria
        }

# Main Streamlit App
def main():
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    
    st.title("🔐 Password Guardian")
    st.markdown("*Your Ultimate Security Companion*")
    
    # Create tabs
    tab1, tab2 = st.tabs(["🎲 Password Generator", "🛡️ Strength Checker"])
    
    # Password Generator Tab
    with tab1:
        st.subheader("Generate Unbreakable Passwords")
        
        # Length slider
        length = st.slider("Password Length", min_value=8, max_value=24, value=12, step=1)
        
        # Generate Button
        col1, col2 = st.columns([3, 1])
        with col1:
            # Initialize session state for generated password
            if 'generated_password' not in st.session_state:
                st.session_state.generated_password = generate_password(length)
            
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
            st.rerun()
        
        # Copy to clipboard button
        copy_btn = st.button("📋 Copy Password", use_container_width=True)
        if copy_btn:
            st.code(generated_password)
            st.success("Password copied to clipboard!")
        
        # Show password strength in generator tab
        result = check_password_strength(generated_password)
        
        st.subheader("🔍 Password Strength")
        # Strength meter
        st.markdown(f"""
        <div class="strength-meter">
            <div style="width: {result['width']}; 
                        height: 100%; 
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
    
    # Strength Checker Tab
    with tab2:
        st.subheader("Check Your Password Strength")
        
        # User password input
        user_password = st.text_input("Enter your password", type="password", key="strength_check")
        
        if user_password:
            # Check password strength
            result = check_password_strength(user_password)
            
            # Strength meter
            st.markdown(f"""
            <div class="strength-meter">
                <div style="width: {result['width']}; 
                            height: 100%; 
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
                ("🔤 Lowercase Letters", any(c.islower() for c in user_password)),
                ("🔠 Uppercase Letters", any(c.isupper() for c in user_password)),
                ("🔢 Numbers", any(c.isdigit() for c in user_password)),
                ("🔣 Special Characters", any(c in string.punctuation for c in user_password)),
                ("📏 Minimum Length (12+)", len(user_password) >= 12)
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