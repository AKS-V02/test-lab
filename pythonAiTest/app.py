import streamlit as st

# Dummy user data for login
USER_CREDENTIALS = {"user": "password"}

# Function for the login page
def login_page():
    st.title("Login Page")
    username = st.text_input("Username")
    password = st.text_input("Password", type='password')

    if st.button("Login", key="login", help="Login", on_click=login(username, password)):
       pass 

def login(username, password):
    # Check credentials immediately when the button is clicked
    if username in USER_CREDENTIALS and USER_CREDENTIALS[username] == password:
        # Set session state for logged in user
        st.session_state.logged_in = True
        st.session_state.username = username
        st.session_state.page = "dashboard"
    else:
        st.error("Invalid credentials")

# Function for the dashboard page
def dashboard_page():
    st.title("Dashboard")
    st.write(f"Welcome, {st.session_state.username}!")
    st.write("Here is your dashboard with user-specific content.")

# Function for the user details page
def user_details_page():
    st.title("User Details")
    st.write(f"Here are your details, {st.session_state.username}:")
    st.write(f"Username: {st.session_state.username}")
    # Add more details here if needed

# Function to render the header with logout
def render_header():
    if st.session_state.logged_in:
        st.sidebar.title("Navigation")
        # Create clickable buttons in the sidebar for navigation
        if st.sidebar.button("Dashboard"):
            st.session_state.page = "dashboard"

        if st.sidebar.button("User Details"):
            st.session_state.page = "user_details"
        col1, col2, col3 = st.columns([10, 1, 10])
        with col1:
            st.markdown(f"### Welcome, {st.session_state.username}")
        with col3:
            if st.button("Logout", key="logout", help="Logout", on_click=logout):
                pass

def logout():
    # Log out by resetting session state
    st.session_state.logged_in = False
    st.session_state.username = None
    st.session_state.page = "login"
    
# Function to render the footer
def render_footer():
    st.markdown("---")
    st.markdown("### Footer")
    st.markdown("This is a simple app built with Streamlit.")
    st.markdown("Contact: example@domain.com")
    st.markdown("© 2025 Streamlit App")

# Main app logic
def main():
    # Ensure the session state variables exist
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if "page" not in st.session_state:
        st.session_state.page = "login"

    if "username" not in st.session_state:
        st.session_state.username = ""

    # Render header
    render_header()

    # Render appropriate content based on login state
    if st.session_state.logged_in:
        # Show the selected page based on session state
        if st.session_state.page == "dashboard":
            dashboard_page()
        elif st.session_state.page == "user_details":
            user_details_page()
    else:
        login_page()

    # Render the footer
    render_footer()

if __name__ == "__main__":
    main()
