# DigitalHospital: Brain Tumor Detection with ML

DigitalHospital is a comprehensive end-to-end web application built using **Streamlit**. The platform integrates Machine Learning for brain tumor detection, a PostgreSQL database for managing patient and doctor data, and features for patient-doctor interaction, such as chat and appointment scheduling.

---

## Features

### 1. **Brain Tumor Detection**
- Utilizes a trained Machine Learning model to detect brain tumors from MRI scans.
- Patients can upload MRI images and receive instant diagnostic feedback.

### 2. **Patient and Doctor Management**
- A PostgreSQL database is used to securely store patient and doctor information.
- Doctors can manage their profiles, view patient history, and provide recommendations.
- Patients can view their medical history and assigned doctor details.

### 3. **Patient-Doctor Interaction**
- Real-time chat feature allows patients and doctors to communicate.
- Patients can schedule appointments with doctors through an integrated calendar.

### 4. **User Authentication**
- Secure login and signup for both patients and doctors.
- Role-based access control ensures proper segregation of patient and doctor functionalities.

---

## Technologies Used

### Backend:
- **Streamlit**: For creating an intuitive and interactive web interface.
- **Machine Learning**: Trained model for brain tumor detection using Python (e.g., TensorFlow/Keras or PyTorch).
- **PostgreSQL**: For storing user data (patients and doctors), medical records, and appointment details.

### Frontend:
- Streamlit's built-in capabilities for designing a user-friendly interface.

### Database:
- **PostgreSQL**: Ensures robust data storage and retrieval.

### Additional Libraries:
- **pandas**: For data manipulation.
- **numpy**: For numerical computations.
- **streamlit-chat**: For real-time chat functionality.
- **sqlalchemy**: For database ORM.
- **matplotlib/seaborn**: For visualizing patient data trends.

---

## Installation

### Prerequisites:
- Python 3.8+
- PostgreSQL installed and configured
- Virtual environment (optional but recommended)

## Usage

### For Patients:
1. Register and log in to the platform.
2. Upload MRI scans for tumor detection.
3. View diagnostic results and medical history.
4. Chat with assigned doctors and schedule appointments.

### For Doctors:
1. Log in to view patient details.
2. Provide recommendations based on tumor detection results.
3. Chat with patients and manage appointments.


