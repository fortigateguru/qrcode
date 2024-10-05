import streamlit as st
import qrcode
from PIL import Image, ImageDraw
import io

# Set page title
st.title("AI-Enhanced QR Code Generator")

# Sidebar for user inputs
st.sidebar.header("QR Code Customization")

# Input text for QR code content
qr_content = st.sidebar.text_input("Enter the content for the QR Code", "https://example.com")

# Upload logo
logo_file = st.sidebar.file_uploader("Upload your logo (optional)", type=["png", "jpg", "jpeg"])

# Input for color
qr_color = st.sidebar.color_picker("Pick a QR code color", "#000000")

# Input for background color
background_color = st.sidebar.color_picker("Pick a background color", "#ffffff")

# Button to generate QR code
if st.sidebar.button("Generate QR Code"):
    # Generate QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4
    )
    qr.add_data(qr_content)
    qr.make(fit=True)

    # Create an image
    img = qr.make_image(fill_color=qr_color, back_color=background_color).convert('RGB')

    # Add logo if uploaded
    if logo_file is not None:
        # Open logo image
        logo = Image.open(logo_file)
        logo.thumbnail((100, 100))

        # Calculate position for logo
        img_w, img_h = img.size
        logo_w, logo_h = logo.size
        position = ((img_w - logo_w) // 2, (img_h - logo_h) // 2)

        # Paste the logo onto the QR code
        img.paste(logo, position, mask=logo)

    # Display QR code
    st.image(img)

    # Provide a download button
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    byte_im = buf.getvalue()
    st.download_button(
        label="Download QR Code",
        data=byte_im,
        file_name="qr_code.png",
        mime="image/png"
    )
