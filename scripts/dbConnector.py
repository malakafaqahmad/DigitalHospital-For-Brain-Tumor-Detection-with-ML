import time
import streamlit as st
import psycopg2
import io
from PIL import Image
import datetime

class connect:
    def __init__(self):
        self.conn = psycopg2.connect(host='localhost', dbname='hmsdummy2', user='postgres',
                                password='root')
        self.cur = self.conn.cursor()
        print('connected')

    def get_cursor(self):
        return self.conn, self.cur

    def signup(self, name, password, email, designation):
        try:
            # Insert user data into the database
            self.cur.execute("INSERT INTO users (name, password_hash, email, designation) VALUES (%s, %s, %s, %s)",
                             (name, password, email, designation))
            self.conn.commit()
            self.cur.execute("SELECT user_id FROM users WHERE name = %s", (name,))
            userid = self.cur.fetchone()[0]
            current_date = datetime.date.today()
            if designation == 'doctor':
                self.cur.execute("INSERT INTO DOCTORS (user_id, doctor_name,email)  VALUES (%s, %s, %s)",
                            (userid, name, email))
                self.conn.commit()

            elif designation == 'patient':
                self.cur.execute("INSERT INTO PATIENTS (user_id, name, email, registration_date) values(%s,%s,%s,%s)",
                                    (userid, name, email,current_date))
                self.conn.commit()
            st.success("User signed up successfully!")
        except Exception as e:
            st.error(f"Error occurred: {e}")

    def signin(self, username, password):
        try:
            # Query user data from the database
            self.cur.execute("SELECT password_hash FROM users WHERE name = %s", (username,))
            user_data = self.cur.fetchone()
            if user_data:
                stored_password = user_data[0]
                if password == stored_password:
                    container = st.empty()
                    container.success("Logged in successfully!")
                    time.sleep(2)
                    container.empty()
                    return True
                else:
                    st.warning("Incorrect password!")
            else:
                st.error("User not found!")
        except Exception as e:
            st.error(f"Error occurred: {e}")
        return False

    def userFeed(self, user_id):
        try:
            # Query user's feed from the database
            self.cur.execute('''
                SELECT p.text
                FROM posts p
                JOIN followers f ON p.doctor_id = f.doctor_id
                WHERE f.follower_id = %s
            ''', (user_id,))
            user_feed = self.cur.fetchall()

            return user_feed
        except Exception as e:
            st.error(f"Error occurred: {e}")
            return []

    def likesCount(self, postid):
        try:
            # Query likes count from the database
            self.cur.execute('''
                SELECT COUNT(*) AS total_likes
                FROM likes
                WHERE postid = %s;
            ''', (postid,))
            likes_count = self.cur.fetchone()[0]  
            return likes_count
        except Exception as e:
            st.error(f"Error occurred: {e}")
            return 0  

        
    def getPostid(self, post):
        try:

            self.cur.execute('''
                SELECT postid
                FROM posts
                WHERE text = %s;
            ''',(post,))
            postid = self.cur.fetchone()[0]
            return postid
        except Exception as e:
            st.error(f"Error occurred: {e}")
            return 0

    def isDoctor(self,user):
        try:
            self.cur.execute('''
                SELECT *
                FROM doctors
                WHERE user_id = %s;
            ''',(user,))
            if self.cur.fetchone() is not None:
                return True
            else:
                return False
        except Exception as e:
            st.error(f"Error occurred: {e}")
            return False

    def get_user_profile(self,user_id):
        try:
            self.cur.execute('''
                SELECT image_data
                FROM user_images
                WHERE user_id = %s;
            ''', (user_id,))
            # print('image')
            image = self.cur.fetchone()[0]
            if image is not None:
                img = Image.open(io.BytesIO(image))
                # print('ff')
                return img
            else:
                print('no profile picture')
                return None
        except Exception as e:
            # print('ff')
            st.error(f"Error occurred: {e}")
            return None

    def userinfo(self, userid):
        try:
            self.cur.execute('''
                SELECT name, email, designation
                FROM users
                WHERE user_id = %s;
            ''', (userid,))
            user = self.cur.fetchone()
            return user
        except Exception as e:
            st.error(f"Error occurred: {e}")
            return None

    def get_appointments(self, userid):
        try:
            # print('try')
            self.cur.execute('''
                SELECT patient_id
                FROM patients
                WHERE user_id = %s;
            ''', (userid,))
            patient_id = self.cur.fetchone()
            # print(patient_id)
            if patient_id is not None:
                self.cur.execute('''
                    SELECT *
                    FROM appointments
                    WHERE patient_id = %s;
                ''', (patient_id,))
                appointments = self.cur.fetchall()
                return appointments
            else:
                st.error("Patient ID not found for the given user ID.")
                return None
        except Exception as e:
            print('exception')
            st.error(f"Error occurred: {e}")
            return None



    def get_prescriptions(self, userid):
        try:
            self.cur.execute('''
                SELECT *
                FROM prescriptions
                WHERE user_id = %s;
            ''', (userid,))
            prescriptions = self.cur.fetchall()
            # print(prescriptions)
            return prescriptions
        except Exception as e:
            st.error(f"Error occurred: {e}")
            return None


    def getdoctorname(self, doctor_id):
        try:
            # Execute SQL query to retrieve doctor name
            self.cur.execute('''
                SELECT doctor_name
                FROM doctors
                WHERE doctor_id = %s;
            ''', (doctor_id,))
            
            # Fetch the doctor name from the result
            doctor_name = self.cur.fetchone()
            
            return doctor_name[0] if doctor_name else None
        except Exception as e:
            st.error(f"Error occurred: {e}")
            return None

    def getdoctorappointments(self,userid):
        try:
            self.cur.execute('''select doctor_id from doctors where
            user_id = %s
            ''',(userid,))
            doctor_name = self.cur.fetchone()
            self.cur.execute('''
                SELECT *
                FROM appointments
                WHERE doctor_id = %s;
            ''', (userid,))
            appointments = self.cur.fetchall()
            # print(appointments)
            return appointments
        except Exception as e:
            st.error(f"Error occurred: {e}")
            return None

    def pname(self,pid):
        # get patient name from patient id
        try:
            self.cur.execute('''select name from users where
            user_id = %s
            ''',(pid,))

            name = self.cur.fetchone()
            return name
        except Exception as e:
            st.error(f'error occured: {e}')
            return None

    def getids(self,pname,userid):
        try:
            self.cur.execute('''
                select patient_id from patients
                where name = %s
            ''',(pname,))
            patient_id = self.cur.fetchone()

            self.cur.execute('''
                select doctor_id from doctors
                where user_id = %s
            ''',(userid,))
            doctor_id = self.cur.fetchone()
            if patient_id and doctor_id:
                return patient_id,doctor_id

        except Exception as e:
            print('exceptin')
            st.error(f'error occured: {e}')
            return None     

    def set_appointments(self,patient_id, doctor_id, date, time, details):
        try:
            self.cur.execute('''
                    INSERT INTO appointments (patient_id, doctor_id, appointment_date, appointment_time, appointment_details)
                    VALUES (%s, %s, %s, %s, %s)''', (patient_id, doctor_id, date, time, details))
            self.conn.commit()
            return True
            
        except Exception as e:
            print('exceptin')
            st.error(f'error occured: {e}')
            return None


    def getsentmessages(self,senderid,recieverid):
        try:
            self.cur.execute('''SELECT messagetext,timestamp
                    FROM sentmessages
                    WHERE senderid = %s
                    AND receiverid = %s
                    ORDER BY timestamp DESC
                  ''',(senderid,recieverid))
            sendtmessages = self.cur.fetchall()
            return sendtmessages
        except Exception as e:
            print('exceptin')
            st.error(f'error occured: {e}')
            return None


    def composemessage(self,senderid,receiverid,text):
        try:
            # if but.button('send', key='sentto'):
            self.cur.execute('''
            INSERT INTO sentmessages (senderid, receiverid, messagetext)
            VALUES (%s, %s,%s)
            ''',(senderid,receiverid,text))
            self.conn.commit()
            self.cur.execute('''
            insert into receivedmessages (senderid, receiverid, messagetext)
            values (%s,%s,%s)
            ''', (senderid,receiverid,text))
            self.conn.commit()
            st.success('message sent')
            return True

        except Exception as e:
            print('ex')
            st.error(f'error occured: {e}')
            return None

        
    def getreceivedmessages(self, senderid, receiverid):
        try:
            self.cur.execute('''
                SELECT messagetext, timestamp
                FROM sentmessages
                WHERE senderid = %s
                AND receiverid = %s
                ORDER BY timestamp DESC
            ''', (senderid, receiverid))
            receivedmessages = self.cur.fetchall()


            return receivedmessages
        except Exception as e:
            print('exception')
            st.error(f'error occurred: {e}')
            return None

    def getusername(self, userid):
        self.cur.execute('''
            SELECT name
            FROM users
            WHERE user_id = %s
        ''', (userid,))
        username = self.cur.fetchone()
        return username

    def selectuser(self):
        self.cur.execute('''
        SELECT name FROM users
        ''')
        users = self.cur.fetchall()

        # Extract the user names from the fetched data
        user_names = [user[0] for user in users]

        selectuser = st.selectbox('Select user', user_names)

        # Retrieve the user_id corresponding to the selected user name
        self.cur.execute('''
        SELECT user_id FROM users
        WHERE name = %s
        ''', (selectuser,))
        user_id = self.cur.fetchone()[0]

        return selectuser, user_id


    def addtosave(self,post,userid):
        self.cur.execute('''
            select postid from posts where text = %s           
        ''', (post,))
        postid = self.cur.fetchone()[0]

        self.cur.execute('''
            INSERT INTO saves (user_id,postid)
                        VALUES (%s,%s)
        ''',(userid,postid))
        self.conn.commit()
        st.success('Post saved')
        # return true
        
    def getpostsaves(self, postid): #count
        self.cur.execute('''
            select count(*) from saves
            where postid = %s
        ''',(postid,))
        saves = self.cur.fetchone()[0]
        return saves


    def getmysaves(self, userid):
        self.cur.execute('''
            SELECT p.text, d.doctor_name
            FROM posts p
            JOIN saves s ON p.postid = s.postid
            JOIN doctors d ON p.doctor_id = d.doctor_id
            WHERE s.user_id = %s
        ''',(userid))

        mysaves = self.cur.fetchall()
        return mysaves



    def alreadysaved(self,userid,post):
        self.cur.execute('''
            select postid from posts where text = %s           
        ''', (post,))
        postid = self.cur.fetchone()[0]
        # print(st.write(postid))
        if postid is None:
            # st.write('not saved')
            # print('postid is',postid)
            return False
        else:
            # st.write('already saved')
            print('postid is',postid)

            return True

    
    def deletefromsave(self,userid,post):
        self.cur.execute('''
            select postid from posts where text = %s           
        ''', (post,))
        postid = self.cur.fetchone()[0]

        self.cur.execute('''
            DELETE FROM saves
            WHERE user_id = %s AND postid = %s;
        ''',(userid,postid))
        self.conn.commit()
        st.success('post removed from saves')


    def getulogeduserid(self, username, password):
        self.cur.execute('''
            select user_id from users where name = %s and password_hash = %s
        ''', (username,password))
        ids = self.cur.fetchone()[0]
        return ids

    def add_post(self, text, userid):
        self.cur.execute('''
            select doctor_id from doctors where user_id = %s
        ''', (userid))
        d_id = self.cur.fetchone()[0]
        self.cur.execute('''
            INSERT INTO posts (text, doctor_id)
            VALUES (%s, %s)
        ''', (text, d_id))
        self.conn.commit()

    def followdoctor_(self, userid, name):
        self.cur.execute("select doctor_id from doctors where doctor_name = %s", (name,))
        doctorid = self.cur.fetchone()[0]
        self.cur.execute('''
            insert into followers (follower_id, doctor_id) values
            (%s, %s)
        ''', (userid, doctorid))
        self.conn.commit()
        st.write('followed successfully')

    def uploadprofileimage(self, userid, image):
        self.cur.execute("insert into user_images (user_id, image_data) values (%s,%s)",
                (userid,  psycopg2.Binary(image.read())))
        self.conn.commit()
        st.write("profile image uploaded")

    def showdoctors_(self):
        self.cur.execute("select doctor_name from doctors")
        doctors = self.cur.fetchall()
        return doctors