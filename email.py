import requests
import smtplib
import ssl
import os
import datetime
import zipfile
import shutil 

from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders

SENDER_EMAIL = "rsomanchi@tns.org"
RECEIVER_EMAIL = "ksuneha@tns.org"
#SENDER_PASS = "TNS_SAKSHAM@2025" 

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
RESPONSES_DIR = "responses"
PHOTOS_DIR = "photos"
OUTPUT_ZIP_FILENAME = "all_survey_data.zip"

def create_local_zip_archive(output_zip_name, responses_folder, photos_folder):
    """
    Creates a zip archive of the responses CSV and photos folder.
    """
    if not os.path.exists(responses_folder) and not os.path.exists(photos_folder):
        print(f"Error: Neither '{responses_folder}' nor '{photos_folder}' found. No data to zip.")
        return None

    # Ensure the main responses CSV exists
    csv_file_path = os.path.join(responses_folder, "all_survey_responses_persistent.csv")
    if not os.path.exists(csv_file_path):
        print(f"Warning: CSV file '{csv_file_path}' not found. Zipping photos only if available.")

        with open(csv_file_path, 'w') as f:
            f.write("Timestamp,Surveyor Name,Question 1,...\n") 

    
    temp_zip_content_dir = "temp_zip_content"
    os.makedirs(temp_zip_content_dir, exist_ok=True)

    try:
        
        if os.path.exists(csv_file_path):
            shutil.copy(csv_file_path, os.path.join(temp_zip_content_dir, os.path.basename(csv_file_path)))

       
        if os.path.exists(photos_folder):
            shutil.copytree(photos_folder, os.path.join(temp_zip_content_dir, "photos"), dirs_exist_ok=True)
            print(f"Copied '{photos_folder}' to temporary directory.")
        else:
            print(f"'{photos_folder}' directory not found. No photos to include in zip.")

        
        shutil.make_archive(output_zip_name.replace(".zip", ""), 'zip', temp_zip_content_dir)
        print(f"Successfully created '{output_zip_name}'.")
        return output_zip_name
    except Exception as e:
        print(f"Error creating zip archive: {e}")
        return None
    finally:
        
        if os.path.exists(temp_zip_content_dir):
            shutil.rmtree(temp_zip_content_dir)
            print(f"Cleaned up temporary directory '{temp_zip_content_dir}'.")


def send_email(attachment_path):
    """
    Sends an email with the specified attachment.
    """
    if not os.path.exists(attachment_path):
        print(f"Attachment file not found: {attachment_path}")
        return False

    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECEIVER_EMAIL
    msg['Subject'] = "Daily Cotton Survey Responses and Photos"

    body = "Attached are the latest survey responses and photos from the Cotton Farming Questionnaire."
    msg.attach(MIMEText(body, 'plain'))

    try:
        with open(attachment_path, "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header(
            "Content-Disposition",
            f"attachment; filename= {os.path.basename(attachment_path)}",
        )
        msg.attach(part)
    except Exception as e:
        print(f"Error attaching file {attachment_path}: {e}")
        return False

    context = ssl.create_default_context()
    try:
        with smtplib.SMTP_SSL(SMTP_SERVER, 465, context=context) as server: # Use 465 for SSL directly
            # server.starttls(context=context) # For port 587
            server.login(SENDER_EMAIL, SENDER_PASS)
            server.send_message(msg)
            print("Email sent successfully!")
            return True
    except smtplib.SMTPAuthenticationError:
        print("SMTP Authentication Error: Check your sender email and app password.")
        print("If you have 2FA enabled, you MUST use an app-specific password.")
        return False
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

def main():
    print(f"Starting data collection and email process at {datetime.datetime.now()}")

    
    zipped_file_name = OUTPUT_ZIP_FILENAME
    archive_path = create_local_zip_archive(zipped_file_name, RESPONSES_DIR, PHOTOS_DIR)

    if archive_path:
       
        if send_email(archive_path):
            print("Process completed successfully.")
        else:
            print("Failed to send email.")
        try:
            os.remove(archive_path)
            print(f"Cleaned up temporary zip file: {archive_path}")
        except OSError as e:
            print(f"Error removing temporary zip file {archive_path}: {e}")
    else:
        print("Skipping email send due to no archive being created.")

if __name__ == "__main__":
    main()
