import streamlit as st
from dbConnector import connect

def main(loggedinuser):
    st.title('sent messages')
    conn = connect()
    selecteduser = conn.selectuser()
    s_username, s_userid = selecteduser
    sentmessages = conn.getsentmessages(loggedinuser, s_userid)
    
    st.write("Sent Messages")
    for message in sentmessages:
        st.write(message)
    text = st.text_input(f'hey {conn.getusername(loggedinuser)} write message to {s_username}', key='lollypopmessaage')
    

    if st.button('send', key='sentto'):
        conn.composemessage(loggedinuser, s_userid, text)

if __name__ == '__main__':
    loggedinuser = 1
    main(loggedinuser)
