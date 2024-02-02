from dotenv import load_dotenv          # load_dotenv will help to load all environment varaibles
load_dotenv()                           # import environment variables 
import streamlit as st                  # for making a front end page so we can take input from user
import os                               # for calling environment variable
from PIL import Image                   # To work with input image 
import  google.generativeai as genai    # To use google generativeai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))          # configring api key

def get_gemini_response(input,image,prompt):                  # writing a functon to gemini pro vision model
    # image = input image
    # input = telling gemini pro model how behave while processing the inputs
    # promt =  with image 
    model=genai.GenerativeModel('gemini-pro-vision')          # loading the gemini model
    response=model.generate_content([input,image[0],prompt])  # getting response from model
    return response.text                                      # there is a parameter in response that we need (text)

def input_image_setup(uploaded_file):                         # This func will covert image into bites(aspected input by 'gemini-pro-vision')
    if uploaded_file is not None:
        bytes_data=uploaded_file.getvalue()

        image_parts=[
            {
                "mime_type": uploaded_file.type,
                "data":bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")
    

st.set_page_config(page_title="Medicale reports  summary")

st.header("Get details abaut your medicle report")
input="""Give a summary and tell is it normall or not"""              # input prompt to send with image
#input=st.text_input("input_prompt:",key="input")
uploaded_file=st.file_uploader("chose an image....", type=["jpg","jpeg","png"]) # taking input as image
image=""
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.",use_column_width=True)  # Showing uploaded image


submit=st.button("Tell me about the Report")                          # submit button

input_prompt="""
you are an expert in understanding the medical reports. you will 
recive input images and you will have give a summary of the report to the patient
"""                                                                   # a input propt that tell geminiai what it is suppose to be while seeing this inputs(image and prompt)

if submit:
    image_data=input_image_setup(uploaded_file)                       # calling the function if button is pressed
    response=get_gemini_response(input_prompt,image_data,input)       

    st.subheader("The response is ")
    st.write(response)




