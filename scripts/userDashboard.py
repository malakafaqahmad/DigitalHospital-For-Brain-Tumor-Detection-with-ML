import streamlit as st
from dbConnector import connect
from imageUploader import UploadedImage
import io
from PIL import Image
import pandas as pd
class dashboard():
    # def __init__(self, userid):
    #     pass
 
    def display_user_image(self, userid):
        conn = connect()
        ppic = conn.get_user_profile(userid)
        if ppic is not None:
            st.image(ppic, caption='User Image', use_column_width=True)
        else:
            st.warning('no image')

    def display_user_info(self, userid):
            conn = connect()
            uinfo = conn.userinfo(userid)
            print(uinfo)
            if uinfo is not None:
                name, email, designation = uinfo
                st.markdown(
                f"""
                <div class="profile-info">
                    <h2>Profile</h2>
                    <p><strong>Name:</strong> {name}<i class="user"></i></p>
                    <p><strong>Medical: {designation}</strong><i class="medical"></i></p>
                    <p><strong>email:</strong> {email} <i class= "email"></i></p>
                </div>
                """,
                unsafe_allow_html=True
            )
    def displayupper(self,userid):
        col1, col2 = st.columns(2)
        with col1:
            self.display_user_image(userid)
        with col2:
            self.display_user_info(userid)


    def display_prescriptions(self, prescriptions):
        conn = connect()
        st.subheader("Prescriptions")
        for prescription in prescriptions:
            doctorid = prescription[2]
            doctorname = conn.getdoctorname(doctorid)
            prescription_info = f'<div class="prescription-row">Doctor: {doctorname} - prescription: {prescription[3]} - Dated: {prescription[-1]}</div>'
            st.markdown(prescription_info, unsafe_allow_html=True)
    def display_appointments(self, appointments):
        st.subheader("Appointments")
        conn = connect()
        for appointment in appointments:
            doctor_id = appointment[2]
            Description = appointment[-1]
            doctor_name = conn.getdoctorname(doctor_id)
            if doctor_name:
                appointment_info = f'<div class="appointment-row">Doctor: {doctor_name} - Description: {Description}</div>'
                st.markdown(appointment_info, unsafe_allow_html=True)

    def gd_appointments_prescriptions(self,userid):
        conn = connect()
        appointments = conn.get_appointments(userid)
        Prescriptions = conn.get_prescriptions(userid)
        # print(appointments)
        if appointments:
            st.markdown("""
            <style>

            .appointment-row {
                padding: 10px;
                background-color: #006400; /* Dark green */
                margin-bottom: 5px;
                border-radius: 5px;
                color: #FFFFFF; /* White text */
            }
            .prescription-row {
                padding: 10px;
                background-color: #006400; /* Dark green */
                margin-bottom: 5px;
                border-radius: 5px;
                color: #FFFFFF; /* White text */
                width: 50%; /* Increase width */

            }
            </style>
            """, unsafe_allow_html=True)

            col01, col02 = st.columns(2)
            with col01:
                self.display_appointments(appointments)
            with col02:
                self.display_prescriptions(Prescriptions)
        
    def display_doctor_appointments(self, conn, docappointments):
        for appointment in docappointments:
            pid = appointment[1]
            Description = appointment[-1]
            doctor_name = conn.pname(pid)
            if doctor_name:
                appointment_info = f'<div class="appointment-row">Doctor: {doctor_name} - Description: {Description}</div>'
                st.markdown(appointment_info, unsafe_allow_html=True)

    def set_appointments(self, conn, userid):
        # st.header('search bar')
        search_name = st.text_input('Enter the patient name', key='patient_name_input')
        
        if st.button('Search', key='search_button'):
            if search_name != '':
                p = conn.getids(search_name, userid)
                if p:
                    pid, did = p
                    date = st.text_input("Date (YYYY-MM-DD)", key='appointment_date_input')
                    time = st.text_input('Time (HH:MM AM/PM)', key='appointment_time_input')
                    details = st.text_input('Details', key='appointment_details_input')
                    
                    if st.button('Post Appointment', key='post_appointment_button'):
                        conn.set_appointments(pid, did, date, time, details)


                else:
                    print('00')
                    st.write('no patient found for the given name')
            else:
                st.write('please enter a name')


    def displaydoc(self, userid):
        conn = connect()
        docappointments = conn.getdoctorappointments(userid)
        col1, col2 = st.columns(2)
        with col1:
            self.set_appointments(conn,userid)
        with col2:
            self.display_doctor_appointments(conn, docappointments)

    

    def displaypat(self, userid):
        # col1, col2 = st.columns(2, gap='large')
        # with col1:
        self.gd_appointments_prescriptions(userid)
     

    def displaylower(self, userid):
        conn = connect()
        if conn.isDoctor(userid):
            print('user is doctor')
            self.displaydoc(userid)
        else:
            self.displaypat(userid)
            print('user is patient')
            UploadedImage()


if __name__ == '__main__':
    userid = 8
    d = dashboard()
    d.displayupper(userid)
    d.displaylower(userid)
