import streamlit as st
from dotenv import load_dotenv
import os
import google.generativeai as genai
from senemail import send_email
from screenshot_agent import capture_gmail_screenshots
from PIL import Image

# Load environment
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

st.title("📬 AI Email Agent - Internship Mail Sender (Gmail OAuth)")

prompt = st.text_input("🔍 What do you want to do?", "Send an internship email to Insurebuzz")

if st.button("🚀 Generate and Send Email"):
    with st.spinner("Generating email content..."):
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(
            f"Write a professional internship email for this prompt: {prompt}. Include a subject line and body."
        )
        generated_text = response.text
        lines = generated_text.split("\n")
        subject = lines[0].replace("Subject:", "").strip() if "Subject" in lines[0] else "Internship Application"
        body = "\n".join(lines[1:]).strip()

        st.subheader("✍️ Subject")
        st.write(subject)
        st.subheader("📄 Body")
        st.write(body)

    with st.spinner("Sending email securely using Gmail API..."):
        try:
            result = send_email(subject, body)
            st.success(f"✅ Email sent successfully! Message ID: {result['id']}")

            # Capture screenshots of Gmail steps (manual login needed)
            st.info("Launching browser to capture email sending journey screenshots. Please complete manual login if prompted.")
            screenshot_paths = capture_gmail_screenshots(os.getenv("TO_EMAIL"), subject, body)

            st.subheader("📸 Email Sending Journey Screenshots")
            for img_path in screenshot_paths:
                st.image(img_path, caption=os.path.basename(img_path), use_column_width=True)

        except Exception as e:
            st.error(f"Failed to send email: {str(e)}")
