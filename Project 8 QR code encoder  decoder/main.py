import streamlit as st
from PIL import Image
import io

# App Title and Instructions
st.title("🔎QR Code Customizer: Apply Colors & Download👩‍💻")
st.write("First, select the colors you'd like to apply to the QR Code image, then upload the image, and we'll apply your color choices.")

# ----------------------------
# Step 1: Let user select QR Code colors
# ----------------------------
st.subheader("📌Step 1: Select Colors for QR Code:")
fg_color = st.color_picker("Select QR Code Color (Foreground)", "#000000")  # User selects color for QR code blocks
bg_color = st.color_picker("Select Background Color", "#FFFFFF")  # User selects background color

# ----------------------------
# Step 2: Let user upload a QR code image
# ----------------------------
st.subheader("📌Step 2: Upload Your QR Code Image:")
uploaded_file = st.file_uploader("Upload QR Code Image", type=["png", "jpg", "jpeg"])  # Accept only image files

# ----------------------------
# Step 3: Process the uploaded image and apply custom colors
# ----------------------------
if uploaded_file is not None:
    img = Image.open(uploaded_file).convert("RGB")  # Convert uploaded image to RGB mode
    st.image(img, caption="Uploaded QR Code", use_container_width=True)  # Display the uploaded image

    st.subheader("📌Step 3: Apply Custom Colors:")

    # Convert selected hex colors to RGB format for processing
    fg_rgb = tuple(int(fg_color[i:i+2], 16) for i in (1, 3, 5))
    bg_rgb = tuple(int(bg_color[i:i+2], 16) for i in (1, 3, 5))

    # Convert image to grayscale to identify black and white areas
    grayscale = img.convert("L")

    # Use thresholding to convert grayscale image to black & white
    bw = grayscale.point(lambda x: 0 if x < 128 else 255, '1')

    # Create a new blank image in RGB where we'll apply new colors
    new_img = Image.new("RGB", img.size)

    # Loop through each pixel and apply the selected foreground or background color
    for y in range(img.height):
        for x in range(img.width):
            pixel = bw.getpixel((x, y))
            new_img.putpixel((x, y), fg_rgb if pixel == 0 else bg_rgb)

    # Show the color-customized QR code
    st.image(new_img, caption="Modified QR Code", use_container_width=True)

    # ----------------------------
    # Step 4: Allow user to download the color-customized image
    # ----------------------------
    st.subheader("📌Step 4: Download the Modified QR Code:")

    # Save the modified image to a BytesIO buffer
    img_buffer = io.BytesIO()
    new_img.save(img_buffer, format="PNG")
    img_buffer.seek(0)

    # Create a download button
    st.download_button(
        label="Download Modified QR Code",
        data=img_buffer,
        file_name="custom_qr_code.png",
        mime="image/png"
    )

# ----------------------------
# Footer
st.write("------")
st.write("© 2023 QR Code Customizer. All rights reserved.")

#Footer
st.write("------")
st.write("📌Created by 🙋‍♀️ Muskan Irfan Ahmed.")