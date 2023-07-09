import os
import openai
import datetime
import streamlit as st
from image_generator import ImageGenerator
import boto3


# read in the environment variable with the API value

openai.api_key = os.getenv('OPENAIKEY')
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
prompt = 'illustration of' + prompt

# When the 'Generate' button is clicked, the image is generated and displayed
if st.button('Generate'):
    image_url = image_gen.generate_an_image(prompt)
    id = image_gen.generate_id()
    image_gen.save_image_to_collection(id, image_url, prompt)
    s3_file_name=add_timestamp(image_gen.collection_file)
    upload_to_s3(file_name=image_gen.collection_file, bucket=BUCKET, object_name=s3_file_name )

    # Display the image
    st.image(image_url)
