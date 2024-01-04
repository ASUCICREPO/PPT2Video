import streamlit as st
import datetime
import requests
import json
import os
st.set_page_config(layout="centered")

st.markdown(
    """
    <style>
    body {
        color: white;
        background-color: #ffffff;
    }
    </style>
    """,
    unsafe_allow_html=True,
)
col1, col2,col3 = st.columns(3)

with col2:
	st.image("quality.png", width=350)

#Function_TO_Upload_File_Into_S3_Securely
def upload_object_via_presigned_url(files, url, res):
    print(url, res)
    response = requests.post(url, files=files, data=res)
    if response.status_code == 204:
        print("File uploaded successfully.")
    else:
        st.error("Error in Uploading file to S3 !!!")
        print(response.text)

st.markdown("""<medium><b>Disclaimer:</b></medium><br/>
<small><b><span style='color:red;'>Please do not upload any sensitive information here.</span></b></small><br/>
<small><b><span style='color:red;'>Download link will expire after 5 minutes.</span></b></small><br/>
<small><b><span style='color:red;'>We do not store any files, and all uploaded files will be automatically deleted after the Link Expiration.</span></b></small><br/><br/> 
""", unsafe_allow_html=True)

uploaded_file = st.file_uploader("Click or drag to upload a file.", type=["ppt", "pptx"])

st.sidebar.title("Settings")
# Language selection
language = st.sidebar.radio("Select Language.(It should be same as speaker notes)", options=["English", "Spanish"], index=0)

# Voice style selection
voice_style = st.sidebar.radio("Which style of voice would you like?", options=['Masculine', 'Feminine'], index=0)

# Video speed selection
video_speed = st.sidebar.radio("Choose the Video speed", ('Slow', 'Medium', 'Fast'), index=1)

st.sidebar.title('How to Use: ')
st.sidebar.video('lightning-talk-demo.mp4')

start_upload = st.button("Generate Video")
api_url = "https://3nteg8unj6.execute-api.us-west-2.amazonaws.com/v1/presignedurl"
download_api = "https://5cgyk37yob.execute-api.us-west-2.amazonaws.com/test/videolink"
bucket_name = os.environ.get('BUCKET_NAME')#'ppt2video-test'

if start_upload:
    if language is not None and uploaded_file is not None and voice_style is not None and video_speed is not None:
        with st.spinner("Uploading File ..."):
            #Get_Current_Time
            curr_time = datetime.datetime.now()
            tmstmp = curr_time.strftime("%Y%m%d_%H%M%S")
            #Get_Uploaded_FIle_Name
            if uploaded_file:
                file_name = uploaded_file.name
                if file_name != "" and file_name != " ":
                    pass
                else:
                    st.error("Error In Attaching File !!! Please Try Again")
                object_name = f"{tmstmp}_{file_name}"
                form_data = { "object_name": object_name }

                #Hit_API
                res = requests.get(api_url, data=form_data)
                if res.status_code==200:
                    stringData = res.content.decode('utf-8')
                    data = json.loads(stringData)

                    #Upload Object Into S3
                    files = { "file": (object_name, uploaded_file.read(), uploaded_file.type)}
                    upload_object_via_presigned_url(files, data['presigned_url']['url'], data["presigned_url"]["fields"])
        #st.success('File Uploaded')
        with st.spinner("Waiting for the Download link ..."):
            #Changing values according Backend
            if language == "English":
                language = "EN"
            elif language == "Spanish":
                language = "ES"

            if voice_style=="Masculine":
                voice_style = "male"
            elif voice_style=="Feminine":
                voice_style = "female"

            if video_speed=="Fast":
                speed = "fast"
            elif video_speed=="Medium":
                speed = "medium"
            elif video_speed=="Slow":
                speed = "slow"

            #Call API to convert PPT->Video. Returns an URL to download.
            details = {"object_name": object_name, "language": language , "speed": speed , "gender": voice_style }
            response = requests.get(download_api, data=details)
            returnedres = response.content.decode('utf-8')
            download_link = json.loads(returnedres)
            print(returnedres, download_link)
            download_link = download_link["downloadurl"]
        if download_link is None or 'downloadurl' not in download_link:
            st.error("Error in Receiving the Download link !!")
        file_content = requests.get(download_link)
        st.video(download_link)
        st.download_button(label="Download Video", data=file_content.content, file_name=file_name.split('.')[0]+".mp4")
    else:
        st.error("Please upload the file and Select all the options. !!")

# Run the app
if __name__ == '__main__':
    pass
