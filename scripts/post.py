import streamlit as st
from dbConnector import connect



def detectDoctor(user):
    conn = connect()
    if conn.isDoctor(user):
        return True
    else:
        return False

def get_posts(user):
    conn = connect()
    posts = conn.userFeed(user)
    posts_with_likes = get_likes(posts)
    return posts_with_likes


def get_likes(posts):
    conn = connect()
    combo_dict = {}
    for post in posts:
        postid = conn.getPostid(post)
        saves = conn.getpostsaves(postid)
        combo_dict[post] = saves
    return combo_dict


def addnewpost(userid):
        # Add new post section
    st.subheader('Add New Post')
    # new_author = st.text_input('Author')
    new_post = st.text_area('Post')
    st.markdown("---")
    if st.button('Add Post'):
        person = connect()
        person.add_post(new_post, userid)
        st.success('Post added successfully!')


def main(loggedinuser):
    conn = connect()
    val = detectDoctor(loggedinuser)
    if val:
        addnewpost(loggedinuser)
    posts = get_posts(loggedinuser)

    st.subheader("Posts")
    i = 0
    for post, likes in posts.items():
        st.write(f"**Post:** {post}")
        st.write(f"**Saves:** {likes}")
        button_key = f'likebut{i}'  # Unique key for each button
        print(conn.alreadysaved(loggedinuser, post))
        if conn.alreadysaved(loggedinuser, post) == False:       
            if st.button('Save', key=button_key):
                conn.addtosave(post,loggedinuser)  # Call a function to save the post to the user's profile
            print('save button created for false')
        else:
            if st.button('unsave', key= button_key):

                conn.deletefromsave(loggedinuser,post)
            print('unsavee button created for true')
        i += 1
        st.write("---")

if __name__ == '__main__':
    loggedinuser = 2
    main(loggedinuser)
    