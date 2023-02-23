import streamlit as st
from keras.models import load_model
from tensorflow_addons.metrics import F1Score
import cv2 as cv
import numpy as np
import os
from convertdicom import dicom_to_img









model = load_model("BrainTumorMGMT.h5")








st.sidebar.subheader ("Tumor -- Tries To Minimize Tumor!")
st.sidebar.image("Brain animated 1.gif")
st.sidebar.progress(50)









st.title('Tumor --')
st.subheader ("Detects The Presence Of MGMT Promoter Methylation")
st.progress(50)








st.image ("brain tumor animated 2.gif", width = 700)
st.progress(50)










st.image ("brain_tumor_anitmatd 3.gif", width = 700)
st.progress (50)












st.subheader ("What is MGMT Promoter Methylation?")
st.video("MGMT Promoter Testing for Patients With GBM.mp4", start_time = 18, format = "video/mp4")
st.progress(50)









st.image ("temozolomide.PNG", width = 700)
st.progress(50)







st.write (">A malignant tumor in the brain is a life-threatening condition. Known as glioblastoma, it's both the most common form of brain cancer in adults and the one with the worst prognosis, with median survival being less than a year. The presence of a specific genetic sequence in the tumor known as MGMT promoter methylation has been shown to be a favorable prognostic factor and a strong predictor of responsiveness to chemotherapy. Currently, genetic analysis of cancer requires surgery to extract a tissue sample. Then it can take several weeks to determine the genetic characterization of the tumor. Depending upon the results and type of initial therapy chosen, a subsequent surgery may be necessary. If an accurate method to predict the genetics of the cancer through imaging (i.e., radiogenomics) alone could be developed, this would potentially minimize the number of surgeries and refine the type of therapy required. Tumor -- application predicts the genetic subtype of glioblastoma using MRI (magnetic resonance imaging) scans to detect for the presence of MGMT promoter methylation. It helps brain cancer patients receive less invasive diagnoses and treatments. ")
st.progress(50)






st.image("mgmt survival chart.PNG")
st.progress(50)





   
st.warning ("Please input the patient info and upload brain MRI image. We will provide your report as a PDF file.")







patient_name = st.text_input ("Patient's Full Name: ","", 100, placeholder = "For Example Ahmad Sabiri", help = "Input patient's full name")
st.progress(50)





patient_contact = st.text_input ("Patient's Contact: ", "", 10, help="Input patient's mobile number", placeholder = "Like 0790xxxxxx")
st.progress(50)





patient_age = st.number_input("Age", 1, 150, 18)
st.progress(50)





patient_gender = st.radio('Gender', ['Male', 'Female'])
st.progress(50)








surgery = st.radio("Surgery In The Past?", ["Yes", "No"])
if surgery == 'Yes':
    st.text_area ("Details & Results Of Surgery", placeholder="Please provide info about the patient's past surgeries.", help = "Please provide info about the patient's past surgeries.", max_chars = 250)
st.progress(50)








former_treatments = st.radio("Past Treatments & Drugs", ["Yes", "No"])
if former_treatments == 'Yes':
    st.text_area ("Details & Drugs", placeholder="Please provide info about recent drugs of the patients.", help = "info of recent drugs.", max_chars=250) 
st.progress(50)








tumor_type = st.selectbox("Type Of Tumor", ["Other", "Gliomas", "Meningiomas", "Pituitary", "Medulloblastomas", "Primary CNS lymphomas", "Craniopharyngiomas", "Pineoblastoma", "Germinomas", "Pineocytoma"])
if tumor_type == 'Other':
    st.text_area ("Details Of Tumor Type", help = "What type of tumor the patient has? Please provide a brief info about it.", max_chars=100, placeholder = "What kind of tumor your patient has? Please provide a bried info." )
st.progress(50)










if os.path.exists("Brain Tumor Images") is None:
    os.mkdir("Brain Tumor Images")

       
       
       
       
       
            
            
def main ():
    
    date_of_appointment = st.sidebar.date_input("Date of Appointment", help = "date of appointment! when the patient came to the doctor for treatment?")
    st.sidebar.progress(50)
    time_of_appointment = st.sidebar.time_input("Time", help = "The exact time of the appointment!")
    st.sidebar.progress(50)
    patient_doctor = st.sidebar.text_input("Doctor ", help = "Who is the patient's doctor?")
    st.sidebar.progress(50)
    patient_address = st.sidebar.text_input("Address ", help = "the address of the patient")
    
    
    
    
    
    
    
    
    # Uploading the image
    file = st.file_uploader("*Please Upload Your Image:", type = ['dcm'], help = "Upload a MRI image of the patient.")
    show_file = st.empty()
    
    
    
    
    
    
    if not file:
        show_file.info("Your image will appear here!")
        return
        
    
    
    
    
    
    
    
    input_img = file
    output_img, instance_number = dicom_to_img(input_img)
    output_img = cv.imwrite(str(f"Brain Tumor Images\{patient_name} {patient_contact} {instance_number - 1}").zfill(4) + '.jpg', output_img)
    file = output_img
    st.image(str(f"Brain Tumor Images\{patient_name} {patient_contact} {instance_number - 1}").zfill(4) + '.jpg')








    
    detect_button = st.button("Detect", help = "Click on the button for the result.")
    if detect_button:
        img = cv.imread(str(f"Brain Tumor Images\{patient_name} {patient_contact} {instance_number - 1}").zfill(4) + '.jpg')
        img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        height = 300
        width = 300
        resized_img = cv.resize (img, (height, width))
        img = np.expand_dims(resized_img, axis = 0)
        result_main = model.predict (img)
        
        
        
        
        
        
        
        
        
        
        
        
        
        st.subheader ('Patient Details')
        
        st.write(f"> Patient name: {patient_name}")
        
        st.write(f"> Patient contact: {patient_contact}")
        
        st.write(f"> Age: {patient_age}")
        
        st.write(f"> Gender: {patient_gender}")
        
        st.write(f"> Doctor: {patient_doctor}")
        
        st.write(f"> Date of Appointment: {date_of_appointment}")
        
        st.write(f"> Time of Appointment: {time_of_appointment}")
        
        st.write(f"> Address: {patient_address}")
        
        st.subheader ("Result")
        result = round(float(result_main * 100), 3)
        st.warning(f"The Prbability For Being Methylated is: {result} %")
        if result >= 50:
            st.success ("Probability > 50 %. Result = Methylated.")
            
            
        else:
            st.warning ("Probability < 50 %. Result = Unmethylated.")
            
        st.sidebar.subheader ("Result")
        st.sidebar.warning(f"The Prbability For Being Methylated is : {round(float(result_main * 100), 3)} %")
 
 
       
       
       
       
       
       
       
       
       
       
       
       
       
    

            










    
main()

    
    
