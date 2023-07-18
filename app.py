import streamlit as st
import pandas as pd
import numpy as np
import math
from PIL import Image
from streamlit_image_coordinates import streamlit_image_coordinates

def get_data():
    if 'df' not in st.session_state:
        data = {
            'Point': ['Lightsource_Top_Point', 'Lightsource_Buttom_Point', 'Spectrum_Line_Mid_Point'],
            'X-Coordinate': [0, 0, 0],
            'Y-Coordinate': [0, 0, 0],
        }
        st.session_state.df = pd.DataFrame(data)
    return st.session_state.df

def main():
    df = get_data()

    st.title("เว็บไซต์คำนวณหาความยาวคลื่น")

    st.write("ใช้ได้กับ DIY Spectrometer ที่จัดทำขึ้นโดยกลุ่มของพวกเราเท่านั้น")

    st.header("จัดทำโดยนักเรียนชั้น ม.6/5")

    st.write("- น.ส.นัสวรรณ รุ่งฤทธิเดช เลขที่ 4")
    st.write("- น.ส.ปภาดา เจริญสิทธิ์ เลขที่ 6")
    st.write("- น.ส.พาขวัญ บุญประกายแก้ว เลขที่ 7")
    st.write("- น.ส.อนัญญา ไชยนพกุล เลขที่ 9")

    uploaded_image = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

    if uploaded_image is not None:
        image = Image.open(uploaded_image)
        st.image(image, caption="Uploaded Image", use_column_width=True)

        st.write("ค่อย ๆ กด จิ้มเลือกพิกัดจ้า:")

        clicked_coor = streamlit_image_coordinates(
            image,
            height=500,
            key="pil",
        )

        st.write(clicked_coor)

        st.write("---*---*---*---*---*---*---*---*---*---*---")

        if st.button("Submit : Coordinate of the top of the light source"):
            if clicked_coor:
                df.loc[df['Point'] == 'Lightsource_Top_Point', 'X-Coordinate'] = clicked_coor.get("x")
                df.loc[df['Point'] == 'Lightsource_Top_Point', 'Y-Coordinate'] = clicked_coor.get("y")
                st.write(f"You submitted: {clicked_coor}")

        st.write("---*---*---*---*---*---*---*---*---*---*---")

        if st.button("Submit : Coordinate of the buttom of the light source"):
            if clicked_coor:
                df.loc[df['Point'] == 'Lightsource_Buttom_Point', 'X-Coordinate'] = clicked_coor.get("x")
                df.loc[df['Point'] == 'Lightsource_Buttom_Point', 'Y-Coordinate'] = clicked_coor.get("y")
                st.write(f"You submitted: {clicked_coor}")

        st.write("---*---*---*---*---*---*---*---*---*---*---")
        
        if st.button("Submit : Coordinate of the midpoint of the spectrum line"):
            if clicked_coor:
                df.loc[df['Point'] == 'Spectrum_Line_Mid_Point', 'X-Coordinate'] = clicked_coor.get("x")
                df.loc[df['Point'] == 'Spectrum_Line_Mid_Point', 'Y-Coordinate'] = clicked_coor.get("y")
                st.write(f"You submitted: {clicked_coor}")

        st.write(df)

        st.write("---*---*---*---*---*---*---*---*---*---*---")
        
        if st.button("Calculate the wavelength of the selected spectrum line"):
            if clicked_coor:
                length_of_light_source = math.sqrt((df.loc[0, 'X-Coordinate']-df.loc[1, 'X-Coordinate'])**2 + (df.loc[0, 'Y-Coordinate']-df.loc[1, 'Y-Coordinate'])**2)
                midpoint_of_light_source_x = (df.loc[0, 'X-Coordinate'] + df.loc[1, 'X-Coordinate'])/2
                midpoint_of_light_source_y = (df.loc[0, 'Y-Coordinate'] + df.loc[1, 'Y-Coordinate'])/2
                distance_to_spectrum = math.sqrt((df.loc[2, 'X-Coordinate'] - midpoint_of_light_source_x)**2 + (df.loc[2, 'Y-Coordinate'] - midpoint_of_light_source_y)**2)
                constant_val = 1/(10000*11)
                y_val = 2*distance_to_spectrum/length_of_light_source
                lambda_val = int(y_val*constant_val*10000000)
                st.write(f"Wavelength: {lambda_val} nm")




if __name__ == "__main__":
    main()
