import streamlit as st
from dbConnector import connect


def main(loggedinuser):
    st.title('recieved messages')
    conn = connect()
    selecteduser = conn.selectuser()
    s_username, s_userid = selecteduser
    messages = conn.getreceivedmessages(s_userid,loggedinuser)

    for message in messages:
        st.write(message)

    text = st.text_input(f'hey {conn.getusername(loggedinuser)} write message to {s_username}', key='lollypopmessaage')
    
    if st.button('send', key='sentto'):
        # st.write('wordk')
        conn.composemessage(s_userid, loggedinuser, text)


if __name__ == '__main__':
    loggedinuser = 6
    main(loggedinuser)