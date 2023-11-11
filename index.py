import os
from openai import OpenAI
import datetime
import time
import streamlit as st
from image_generator import ImageGenerator
import boto3
from PIL import Image

# read in the environment variable with the API value
#openai.api_key = os.getenv('OPENAIKEY')
client = OpenAI(api_key = os.environ['OPENAIKEY'])
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
BUCKET=os.getenv('S3_BUCKET')




def upload_to_s3(file_name, bucket, object_name=None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = file_name

    # Upload the file
    s3_client = boto3.client('s3')
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True


def add_timestamp(filename: str) -> str:
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    base, extension = os.path.splitext(filename)
    return f"{base}_{timestamp}{extension}"

def add_s3_directory(file_name: str, directory_name: str = 'data_in') -> str:
    file_name=file_name.split('/')[-1]
    return f'{directory_name}/'+file_name


# load the logo in
logo = 'logo.png'
image_logo = Image.open(logo)
pencil ='pencil.png'
image_pencil = Image.open(logo)

# Use columns to place the title and image side by side
col1, col2 = st.columns([2, 1])  

# In the first column, put the title
with col1:
    st.title('Drawing Bot')
    # Create a text input for the image prompt
    st.subheader('What would you like?')
    prompt = st.text_input(label='draw this:',label_visibility="collapsed")
    if 'illustration' in prompt:
        prompt
    else:
        prompt = 'illustration of ' + prompt
    
# In the second column, put the image
with col2:
    st.image(image_logo, use_column_width=True)

# Define a function to inject custom CSS
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Inject the CSS
local_css("style.css")



# When the 'Generate' button is clicked, the image is generated and displayed
if st.button('✏️  Draw it!'):
    with st.spinner('drawing.. please wait'):
        time.sleep(8)
        # Create an instance of the ImageGenerator class
        image_gen = ImageGenerator()
        image_url = image_gen.generate_an_image_d3(client=client,prompt=prompt)

        # Display the image
        st.image(image_url)
        # Save data 
        image_gen.save_image_to_collection('1')
        # download the image 

        s3_file_name=add_s3_directory(add_timestamp(image_gen.collection_file))
        upload_to_s3(file_name=image_gen.collection_file, bucket=BUCKET, object_name=s3_file_name )

    #upload image file to s3
    #s3_file_name=add_s3_directory(image_gen.image_name, 'data_in/images')
    #upload_to_s3(file_name=image_gen.image_name, bucket=BUCKET, object_name=s3_file_name )

    # if image liked, save to S3
    # TODO: add a flag to json 

