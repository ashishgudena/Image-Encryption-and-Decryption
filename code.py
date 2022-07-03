import streamlit as st
import random as rd
import numpy as np
import os
import cv2

keys=[]

def encryption(image_name):
    global keys
    image_input = cv2.imread(image_name)
    h,w,c=image_input.shape
    image = []
    for i in range(h):
        arr = []
        subkeys=[]
        for j in range(w):
            color = image_input[i,j]
            key = [rd.randrange(0, 255, 2), rd.randrange(0, 255, 2), rd.randrange(0, 255, 2)]
            pixel_encrypted = [color[0]^key[0],color[1]^key[1],color[2]^key[2]]
            arr.append(pixel_encrypted)
            subkeys.append(key)
        image.append(arr)
        keys.append(subkeys)
    img = np.asarray(image)
    name = './enc.png'
    cv2.imwrite(name, img)
    st.write("Successfully Encrypted!")
    st.image('./enc.png',caption='Encrypted Image')
    keys = np.array(keys)
    np.save("nparr.npy", keys)

def decryption(image_name):
    keys = np.load("nparr.npy")
    image_input = cv2.imread(image_name)
    h,w,c = image_input.shape
    image = []
    for i in range(h):
        arr = []
        for j in range(w):
            color = image_input[i][j]
            pixel_decrypted = [color[0]^keys[i][j][0],color[1]^keys[i][j][1],color[2]^keys[i][j][2]]
            arr.append(pixel_decrypted)
        image.append(arr)
    img = np.array(image)
    name = './dec.png'
    cv2.imwrite(name, img)
    st.write("Successfully Decrypted!")
    st.image('./dec.png',caption='Decrypted Image')

if __name__ == '__main__':
    st.markdown("<h1 style='text-align: center; color: red;'>IMAGE</h1>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center; color: red;'>Encryption & Decryption</h1>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader('FILE UPLOAD')
    if uploaded_file:
        st.image(uploaded_file)
    col1, col2, col3, col4, col5, col6, col7 = st.columns(7)
    encrypt = col1.button("ENCRYPT")
    col2.write("                           ")
    col3.write("                           ")
    col4.write("                           ")
    col5.write("                           ")
    col6.write("                           ")
    decrypt = col7.button("DECRYPT")
    if encrypt:
        encryption(uploaded_file.name)
    if decrypt:
        decryption('./enc.png')