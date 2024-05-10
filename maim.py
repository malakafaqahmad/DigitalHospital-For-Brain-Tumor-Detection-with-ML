import streamlit as st
from streamlit_option_menu import option_menu
from userDashboard import dashboard
from post import main as userFeed
from recievedmessages import main as recievedmain
from sentMessages import main as sentmain
from dbConnector import connect
from settingspage import settingmain

def write_to_file(filename, content):
    with open(filename, 'w') as file:
        file.write(str(content))

def read_from_file(filename):
    with open(filename, 'r') as file:
        content = file.read()
    return content


def sidebar():
    with st.sidebar:
        selected = option_menu(
            menu_title='main menu',
            options=["My Profile", "Posts", "Received Messages", "Sent Messages", "Settings"]
        )
    return selected

def main_content(selected_page, loggedinuser):
    if selected_page == "My Profile":
        # global loggedinuser
        print('my profile loggedin user ', loggedinuser)
        if loggedinuser is not None:
            print('------_____________-----')
            userprofile = dashboard()
            userprofile.displayupper(loggedinuser)
            userprofile.displaylower(loggedinuser)

    if selected_page == "Posts":
        userFeed(loggedinuser)

    if selected_page == "Received Messages":
        recievedmain(loggedinuser)

    elif selected_page == "Sent Messages":
        sentmain(loggedinuser)

    elif selected_page == "Settings":
        st.title("Settings Page")
        settingmain(loggedinuser)


def signin():
    st.title("Login Page")
    username = st.text_input('Username', key='username')
    password = st.text_input('Password', key='password', type='password')
    ids = None

    if st.button("Login"):
        if username and password:
            person = connect()
            if person.signin(username, password):
                uid = person.getulogeduserid(username, password)
                st.warning(f"uid is {uid}")
                write_to_file('logboy.txt', uid)
                print('session state is set for main')
                st.session_state.page = "main"

            else:
                st.warning("Invalid username or password!")
        else:
            st.warning("Please enter both username and password!")

    if st.button("Go to Signup"):
        st.session_state.page = "signup"

    return ids

def signup():
    st.title("Signup Page")

    username = st.text_input("Username")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")

    designation_options = ['Doctor', 'Patient', 'Other Staff']
    designation = st.selectbox("Designation", designation_options)

    if st.button("Signup"):
        if username and email and password and confirm_password:  # Check if all fields are not empty
            if password == confirm_password:  # Check if password and confirm password match
                person = connect()
                person.signup(username, password, email, designation.lower())  # Lowercase designation
                print('designation is ', designation.lower())
                # st.success("Signup successful!")
                st.session_state.page = "login"
            else:
                st.warning("Passwords do not match!")
        else:
            st.warning("Please fill in all fields!")

    if st.button("Go to Login"):
        st.session_state.page = "login"
        st.empty()  # Clear the content of the current page

def main():
    # print('uid is ', uid)
    selected_page = sidebar()
    # loggedinuser = uid
    # print('loginuserid ', loggedinuser)
    loggedinuser = read_from_file('logboy.txt')
    print("logged in user", loggedinuser)
    if loggedinuser:
        main_content(selected_page, loggedinuser)
    else:
        print('cant process loggedinuser')

def getit():

    if "page" not in st.session_state:
        st.session_state.page = "signin"


    if st.session_state.page == "signin":
        signin()

    elif st.session_state.page == "signup":
        signup()
    
    elif st.session_state.page == "main":
        main()


if __name__ == "__main__":
    getit()






