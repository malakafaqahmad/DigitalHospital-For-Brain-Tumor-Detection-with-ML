import streamlit as st
from kerasXModel import predict



def UploadedImage():
    st.title("Upload Xray")
    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
    
    if uploaded_file is not None:
        p = predict(uploaded_file)
        st.write("Prediction:", p.prediction_result)
        st.write("Confidence Score:", p.confidence_score)


if __name__ == "__main__":
    UploadedImage()