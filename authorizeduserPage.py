import streamlit as st
from streamlit_option_menu import option_menu
from userDashboard import dashboard
from post import main as userFeed
from recievedmessages import main as recievedmain
from sentMessages import main as sentmain
from dbConnector import connect

loggedinchanged = False
loggedinuser = 0

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
            userprofile = dashboard(loggedinuser)
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
        st.write('Under Working')

def signin():
    st.title("Login Page")
    username = st.text_input('Username', key='username')
    password = st.text_input('Password', key='password', type='password')
    ids = None

    if st.button("Login"):
        if username and password:
            person = connect()
            if person.signin(username, password):
                global loggedinuser
                global loggedinchanged
                llu = person.getulogeduserid(username, password)
                if loggedinchanged == False:
                    if llu is not None:
                        loggedinchanged = True
                        print('loggedinchange is updated to ', loggedinchanged)
                        loggedinuser = llu
                        print("loggedinuser is updated to ",loggedinuser)
                        if loggedinuser is not None:
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
    st.title("Sign Up Page")
    # Add signup form elements here

def main():
    selected_page = sidebar()
    global loggedinuser
    print("the value of lu in main ",loggedinuser)
    if loggedinuser:
        main_content(selected_page, loggedinuser)
    else:
        print('cant process loggedinuser')

def getit():
    userid_logedin = None
    flag = False
    st.write('getit called')
    if "page" not in st.session_state:
        st.session_state.page = "signin"

    if st.session_state.page == "signin":
        signin()
        global loggedinuser
        if loggedinuser is not None:
            if flag == False:
                userid_logedin = loggedinuser
                print('come out of signin with userid' , loggedinuser)
                print('set userid_logedin to ', userid_logedin)

    elif st.session_state.page == "signup":
        signup()
    
    elif st.session_state.page == "main":
        # global loggedinuser
        global loggedinchanged
        print('got to main with userid_logedin ',userid_logedin)
        print('got to main session')
        if loggedinchanged == True:
            print('main called')
            main()

if __name__ == "__main__":
    getit()
