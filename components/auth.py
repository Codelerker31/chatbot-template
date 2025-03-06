import streamlit as st
import extra_streamlit_components as stx

def render_auth(supabase):
    """Render authentication UI and handle login/signup process"""
    
    if "user" in st.session_state and st.session_state.user is not None:
        # Show logout option if user is logged in
        email = getattr(st.session_state.user, 'email', 'Unknown')
        st.sidebar.write(f"Logged in as: {email}")
        
        if st.sidebar.button("Logout"):
            del st.session_state.user
            st.rerun()
        return st.session_state.user
    
    # Create tabs for login and signup
    auth_tab1, auth_tab2 = st.tabs(["Login", "Sign Up"])
    
    with auth_tab1:
        with st.form("login_form"):
            email = st.text_input("Email", key="login_email")
            password = st.text_input("Password", type="password", key="login_password")
            submit = st.form_submit_button("Login")
            
            if submit:
                try:
                    response = supabase.auth.sign_in_with_password({"email": email, "password": password})
                    st.session_state.user = response.user
                    st.rerun()
                except Exception as e:
                    st.error(f"Login failed: {str(e)}")
                    if "Email not confirmed" in str(e):
                        st.info("Please check your email and confirm your account before logging in.")
    
    with auth_tab2:
        with st.form("signup_form"):
            email = st.text_input("Email", key="signup_email")
            password = st.text_input("Password", type="password", key="signup_password")
            confirm_password = st.text_input("Confirm Password", type="password")
            submit = st.form_submit_button("Sign Up")
            
            if submit:
                if password != confirm_password:
                    st.error("Passwords do not match")
                else:
                    try:
                        redirect_url = st.secrets.get("SITE_URL", "https://your-streamlit-app-url.com")
                        
                        response = supabase.auth.sign_up({
                            "email": email, 
                            "password": password,
                            "options": {
                                "email_redirect_to": redirect_url
                            }
                        })
                        
                        st.success("Account created! Please check your email to confirm your account.")
                        st.info("After confirming your email, you can log in using the Login tab.")
                    except Exception as e:
                        st.error(f"Signup failed: {str(e)}")
    
    return None  # No user logged in 