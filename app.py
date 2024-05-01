import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai
import io
from io import BytesIO
from PIL import Image

def generate_content(img=None):
    load_dotenv()
    gemini_api_key = os.getenv('GEMINI_API_KEY')
    genai.configure(api_key=gemini_api_key)
    model = genai.GenerativeModel('gemini-1.0-pro-vision-latest')
    try:
        response = model.generate_content([img])
        # analysis model
        model_ana = genai.GenerativeModel('gemini-1.5-pro-latest')
        prompt_ana = f'''if this text is a medical report, X-Ray, MRI (Magnetic Resonance Imaging), CT (Computed Tomography), Ultrasound, PET (Positron Emission Tomography), SPECT (Single Photon Emission Computed Tomography), Mammography, Fluoroscopy, DEXA (Dual-Energy X-ray Absorptiometry) analysis: \n"{response.text}" \n\n give me more explain for the results and sure to say "الرجاء التواصل مع طبيب لمعلومات أكثر" Answer ONLY in Arabic.
        else (The given Text not related to any medical information) then reponse "لا يمكنني المساعدة بذلك"'''
        response_ana = model_ana.generate_content([prompt_ana])
        return response_ana.text 
    except Exception as e:
        st.error("Failed to generate content: {}".format(e))
        return None

def main():
    st.title("🔬🧪MedA👩🏻‍🔬🗜️")
    st.markdown("##### Skip the Wait, Not the Detail: Fast AI Lab Analysis")
    
    # Sidebar with larger font size
    st.sidebar.header("Imaging Types 📋")
    st.sidebar.markdown("""
    <style>
    .font-large {font-size:18px;}
    </style>
    <div class='font-large'>
    - Medical report 📄<br>
    - X-Ray ☠️<br>
    - MRI (Magnetic Resonance Imaging) 🧲<br>
    - CT (Computed Tomography) 🌀<br>
    - Ultrasound 🔊<br>
    - PET (Positron Emission Tomography) 💠<br>
    - SPECT (Single Photon Emission Computed Tomography) 🔅<br>
    - Mammography 🎀<br>
    - Fluoroscopy 💡<br>
    - DEXA (Dual-Energy X-ray Absorptiometry) ⚖️
    </div>
    """, unsafe_allow_html=True)
    st.sidebar.markdown("### Note")
    st.sidebar.info("Please note that this model's accuracy depends on the accuracy of the given image, estimated at 90%. Always consult a doctor for more detailed and recommended medical advice.")

    img_file_buffer = st.file_uploader("Upload an image (jpg, png, jpeg):", type=["jpg", "png", "jpeg"])
    img = None
    if img_file_buffer is not None:
        img = Image.open(io.BytesIO(img_file_buffer.getvalue()))

    if st.button("Analysis"):
        if img:
            processed_text = generate_content(img)
            st.markdown(f"<div style='direction: rtl; text-align: lest;'>{processed_text}</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
