import streamlit as st
import smtplib
from email.mime.text import MIMEText
from datetime import datetime

# --- Configuration (from Streamlit Secrets) ---
SENDER_EMAIL = st.secrets["email_sender"]["email"]
SENDER_PASSWORD = st.secrets["email_sender"]["password"]

# List of recipient emails
RECIPIENT_EMAILS = [
    st.secrets["survey_recipients"]["email1"],
    st.secrets["survey_recipients"]["email2"]
]
# Add more recipients if you configured them in secrets
# RECIPIENT_EMAILS.append(st.secrets["survey_recipients"]["email3"])


# --- Function to send email ---
def send_survey_email(name, email, rating, feedback):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    subject = f"New Survey Response from {name} ({email})"
    body = f"""
    New Survey Response:
    --------------------
    Timestamp: {timestamp}
    Name: {name}
    Email: {email}
    Service Rating: {rating}
    Feedback:
    {feedback}
    --------------------
    """

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = SENDER_EMAIL

    success = False
    for recipient in RECIPIENT_EMAILS:
        try:
            msg["To"] = recipient # Set recipient for each individual email
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp: # Use SMTP_SSL for secure connection
                smtp.login(SENDER_EMAIL, SENDER_PASSWORD)
                smtp.send_message(msg)
            st.success(f"Response sent to {recipient} successfully!")
            success = True # At least one email sent successfully
        except Exception as e:
            st.error(f"Error sending email to {recipient}: {e}")
            st.warning("Please check your sender email/app password and recipient emails in Streamlit secrets.")

    return success # Return True if at least one email was sent successfully

# --- Streamlit App UI ---
st.set_page_config(layout="centered", page_title="Email Survey App")
st.title("My Simple Survey App (Emailing Responses)")
st.write("Please fill out the survey below. Your response will be emailed.")

with st.form("survey_form"):
    name = st.text_input("Your Name:", key="name_input") # Added keys for better input management
    email = st.text_input("Your Email:", key="email_input")
    rating = st.slider("Rate our service (1-5):", 1, 5, key="rating_slider")
    feedback = st.text_area("Any additional feedback?", key="feedback_area")

    submitted = st.form_submit_button("Submit Survey")

    if submitted:
        if not name or not email:
            st.warning("Please fill in your Name and Email.")
        else:
            if send_survey_email(name, email, rating, feedback):
                st.info("Your response has been sent via email. Check your inbox!")
                # Optional: Clear form inputs after successful submission
                st.session_state.name_input = ""
                st.session_state.email_input = ""
                st.session_state.rating_slider = 3 # Reset slider to a default
                st.session_state.feedback_area = ""
            else:
                st.error("Failed to send response. Please check the error messages above.")

st.markdown("---")
st.markdown("Developed with ❤️ by Streamlit User")
