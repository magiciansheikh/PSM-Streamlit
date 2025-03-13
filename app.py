import re
import streamlit as st
import random
import string

#-------------------
# Strength checking
#-------------------
def check_password_strength(password):
    score = 0
    feedback = []
    
    #-----------------
    # Length checking
    #-----------------
    if len(password) >= 12:
        score += 2
    elif len(password) >= 8:
        score += 1
    else:
        feedback.append("Use at least 8 characters (12+ recommended)")
    
    #---------------------
    # Characters checking
    #---------------------
    checks = [
        (r'[A-Z]', "Add uppercase letter"),
        (r'[a-z]', "Add lowercase letter"),
        (r'\d', "Include digit"),
        (r'[!@#$%^&*]', "Add special character"),
    ]
    
    for pattern, message in checks:
        if re.search(pattern, password):
            score += 1
        else:
            feedback.append(message)

    #----------------
    # Strength level
    #----------------
    if score <= 2:
        strength = "Weak"
    elif score <= 5:
        strength = "Moderate"
    else:
        strength = "Strong"
    
    return score, feedback, strength

#-----------
# Generator
#-----------
def generate_secure_password(length=12):
    if length < 8:
        raise ValueError("Password length should be at least 8 characters")
    
    #--------------------------------
    # Ensure for required characters
    #--------------------------------
    uppercase = random.choice(string.ascii_uppercase)
    lowercase = random.choice(string.ascii_lowercase)
    digit = random.choice(string.digits)
    symbol = random.choice('!@#$%^&*')
    
    #----------------------
    # Remaining characters
    #----------------------
    remaining = length - 4
    all_chars = string.ascii_letters + string.digits + '!@#$%^&*'
    rest = ''.join(random.choices(all_chars, k=remaining))

    #---------------------
    # Combine and shuffle
    #---------------------
    password = list(uppercase + lowercase + digit + symbol + rest)
    random.shuffle(password)
    return ''.join(password)

#----------------------------
# Streamlit UI Configuration
#----------------------------
st.set_page_config(
    page_title="Secure Password Manager",
    page_icon="🛡️",
    layout="centered"
)

#------------
# Custom CSS
#------------
st.markdown("""
    <style>
    .main-container {
        max-width: 1200px;
        margin: 0 auto;
        padding: 2rem;
    }
    .stTextInput input {
        padding: 12px;
        border-radius: 8px;
        border: 1px solid #ced4da;
        transition: border-color 0.3s;
    }
    .stTextInput input:focus {
        border-color: #80bdff;
        box-shadow: 0 0 0 2px rgba(0,123,255,0.25);
    }
    .stButton>button {
        background: #2c7be5;
        color: white;
        border-radius: 8px;
        padding: 12px 24px;
        transition: all 0.3s;
        border: none;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .stButton>button:hover {
        background: #1a64d1;
        transform: translateY(-2px);
    }
    .password-box {
        background: #0e1117;
        padding: 1.5rem;
        border-radius: 10px;
        border: 1px solid #e9ecef;
        transition: transform 0.2s;
    }
    .password-box:hover {
        transform: translateY(-3px);
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .footer {
        text-align: center;
        margin-top: 2rem;
        padding: 1rem;
        color: #6c757d;
    }
    .sidebar .stMarkdown {
        margin-bottom: 1.5rem;
    }
    .history-item {
        background: #262730;
        margin: 0.5rem 0;
        padding: 0.75rem;
        border-radius: 6px;
    }
    </style>
""", unsafe_allow_html=True)

#--------------------
# Initialize session
#--------------------
if 'password_history' not in st.session_state:
    st.session_state.password_history = []
if 'pwd_input' not in st.session_state:
    st.session_state.pwd_input = ""

#----------
# Callback
#----------
def update_password():
    gen_length = st.session_state.gen_length
    generated_pwd = generate_secure_password(gen_length)
    st.session_state.pwd_input = generated_pwd

#------------
# App layout
#------------
st.markdown('<div class="main-container">', unsafe_allow_html=True)
st.title("🛡️ Secure Password Manager")
st.markdown("### Enhance your digital security with strong passwords")

#--------------
# Layout split
#--------------
col1, col2 = st.columns([3, 1], gap="medium")

with col1:
    with st.form("password_form", clear_on_submit=False):
        password = st.text_input(
            "Enter password to check:",
            type="password",
            help="Enter a password to check its strength",
            value=st.session_state.pwd_input,
            key="pwd_input"
        )
        submitted = st.form_submit_button("Analyze Password")

with col2:
    with st.expander("🛠 Generate Password", expanded=True):
        st.number_input(
            "Length:", 
            min_value=8, 
            max_value=32, 
            value=12,
            key="gen_length"
        )
        st.button(
            "Generate Password",
            on_click=update_password,
            help="Generate a secure random password"
        )
        if st.session_state.pwd_input:
            with st.container():
                st.success("Password Generated")
                st.code(st.session_state.pwd_input, language="text")

#------------------
# Analysis results
#------------------
if submitted and password:
    score, feedback, strength = check_password_strength(password)
    st.session_state.password_history = [password] + st.session_state.password_history[:4]
    
    with st.container():
        st.subheader("Security Analysis")
        progress = min(score / 6, 1.0)
        
        # Progress bar styling
        st.markdown(f"""
        <div class="password-box">
            <div style="display: flex; justify-content: space-between; margin-bottom: 1rem;">
                <span>Password Strength:</span>
                <span>{strength}</span>
            </div>
            <div style="background: #e9ecef; border-radius: 6px; height: 8px;">
                <div style="
                    width: {progress*100}%;
                    height: 100%;
                    background: {'#dc3545' if strength == 'Weak' else '#ffc107' if strength == 'Moderate' else '#28a745'};
                    border-radius: 6px;
                    transition: width 0.5s;
                "></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if feedback:
            st.markdown("#### Improvement Suggestions:")
            for item in feedback:
                st.markdown(f"- {item}")

#---------
# Sidebar
#---------
with st.sidebar:
    # Section 1: Action Panel
    st.markdown("### Action Center")
    st.markdown("""
    <div class="action-buttons">
        <button onclick="window.location.href='#generate-password'" 
            class="action-btn generate-btn">Generate Password</button>
        <button onclick="window.location.href='#requirements'" 
            class="action-btn requirements-btn">Security Checklist</button>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Section 2: Password History
    st.markdown("### Recent Passwords")
    if st.session_state.password_history:
        st.markdown('<div class="history-grid">', unsafe_allow_html=True)
        for pwd in st.session_state.password_history:
            st.markdown(f"""
            <div class="history-card">
                <span>••••••••</span>
                <span>{pwd[-4:]}</span>
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="empty-state">No recent passwords</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Section 3: Security Requirements
    st.markdown("### Security Standards")
    st.markdown("""
    <div class="requirements-grid">
        <div class="requirement-item length">12+ Characters</div>
        <div class="requirement-item case">Upper & Lowercase</div>
        <div class="requirement-item number">At Least One Number</div>
        <div class="requirement-item symbol">Special Characters</div>
        <div class="requirement-item unique">Unique Combinations</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Custom CSS for Sections
    st.markdown("""
    <style>
    .sidebar-section {
        margin: 1.5rem 0;
        padding: 1rem;
        background: #ffffff;
        border-radius: 12px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    
    .action-buttons {
        display: flex;
        gap: 0.5rem;
        flex-direction: column;
    }
    
    .action-btn {
        width: 100%;
        padding: 12px;
        border: none;
        border-radius: 8px;
        cursor: pointer;
        font-weight: 500;
        transition: all 0.2s;
        margin: 0.25rem 0;
    }
    
    .generate-btn {
        background: #2c7be5;
        color: white;
    }
    
    .generate-btn:hover {
        background: #1a64d1;
        transform: translateY(-1px);
    }
    
    .requirements-btn {
        background: #e2e3e5;
        color: #343a40;
    }
    
    .requirements-btn:hover {
        background: #ced4da;
        transform: translateY(-1px);
    }
    
    .history-grid {
        display: grid;
        gap: 0.5rem;
    }
    
    .history-card {
        display: flex;
        justify-content: space-between;
        padding: 0.75rem;
        background: #262730;
        border-radius: 6px;
        align-items: center;
    }
    
    .history-mask {
        color: #6c757d;
    }
    
    .history-suffix {
        font-weight: 600;
        color: #212529;
    }
    
    .requirements-grid {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 0.75rem;
    }
    
    .requirement-item {
        padding: 0.75rem;
        border-radius: 6px;
        background: #f8f9fa;
        text-align: center;
        font-weight: 500;
    }
    
    .length { background: #d4edda; color: #155724; }
    .case { background: #fff3cd; color: #856404; }
    .number { background: #d1ecf1; color: #0c5460; }
    .symbol { background: #f8d7da; color: #721c24; }
    .unique { background: #e2e3e5; color: #343a40; }
    
    .empty-state {
        text-align: center;
        padding: 1rem;
        color: #6c757d;
    }
    </style>
    """, unsafe_allow_html=True)

#------------
# Disclaimer
#------------
st.markdown('<div class="footer">Developed with ❤️ by Muhammad Salman Hussain</div>', unsafe_allow_html=True)
st.caption("<div class='footer'>Security Note: Passwords are not stored permanently and are cleared when you refresh the page. Always use a password manager for secure storage.</div>", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)