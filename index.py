import os
import openai
import streamlit as st
from image_generator import ImageGenerator

# read in the environment variable with the API value

openai.api_key = os.getenv('OPENAIKEY')


# Create an instance of the ImageGenerator class
image_gen = ImageGenerator()

st.title("Drawing bot")

# Define a function to inject custom CSS
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Inject the CSS
local_css("style.css")

# Create a text input for the image prompt
prompt = st.text_input('What image would you like me to draw?')

# When the 'Generate' button is clicked, the image is generated and displayed
if st.button('Generate'):
    image_url = image_gen.generate_an_image(prompt)
    id = image_gen.generate_id()
    image_gen.save_image_to_collection(id, image_url, prompt)
    
    # Display the image
    st.image(image_url)
