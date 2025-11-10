import streamlit as st
import earthengine
import glob
import os
import rasterio
import numpy as np
import matplotlib.pyplot as plt
import request
import json




st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Analyze", "Get Data"])

if page == "Analyze":
    if "index" not in st.session_state:
        st.session_state.index="rgb"

    if "DISPLAY" not in st.session_state:
        st.session_state.DISPLAY=False



    def show_rgb():
        st.session_state.index="rgb"

    def show_ndvi():
        st.session_state.index="ndvi"

    def show_ndwi():
        st.session_state.index="ndwi"

    def show_ndmi():
        st.session_state.index="ndmi"

    list_main=[]

    classification_classes=[
        "Annual Crop",
        "Forest",
        "Herbaceous Vegetation",
        "Highway",
        "Industrial",
        "Pasture",
        "Permanent Crop",
        "Residential",
        "River",
        "Sealake"
    ]


        


    folders = glob.glob("gdrive/*.tif")
    folders = [os.path.basename(f) for f in folders]
    task=[]



    for i in folders:
        task.append(i.split(":")[0])

    task=list(set(task))
    task.insert(0,"--Select--")
    choice = st.selectbox("Select Your Task:",task,index=0)

    if choice != "--Select--":
        files = glob.glob(f"gdrive/*{choice}*.tif")
        files = [os.path.basename(f) for f in files]
        images=[]
        for i in files:
            images.append(i.split(":")[1])
        image=st.multiselect("Select Image",images)
        if image !=[]:
            for i in image:
                list_main.append(f"gdrive/{choice}:{i}")

            display=st.button("Display Image")
            classify=st.button("Classification")
            if display:
                st.session_state.DISPLAY=True

            
            if classify:
                st.session_state.DISPLAY=False
                value=request.list_(list_main)
                value=value.json()
               
                for i ,j in enumerate(list_main):
                    cell_num=0
                    with rasterio.open(j) as src:
                            array=src.read()
                    C,H,W=array.shape
                    if H!=W:
                       min_dim=min(H,W)
                       array=array[:,:min_dim,:min_dim]
                    t=array.shape[1]%64
                    if t!=0:
                       array=array[:,:-t,:-t]
                    array=np.stack((array[4,:,:],array[3,:,:],array[2,:,:]), axis=-1)
                    rows, cols = int(array.shape[0]/64), int(array.shape[1]/64)
                    fig, ax = plt.subplots()
                    ax.imshow(array/10000)

                    
                    h, w = array.shape[:2]
                    row_step = h / rows
                    col_step = w / cols

                    
                    for r in range(rows):
                        for c in range(cols):
                            ax.plot([c * col_step, c * col_step], [0, h], 'k-', linewidth=0.8)
                            ax.plot([0, w], [r * row_step, r * row_step], 'k-', linewidth=0.8)

                            x = c * col_step + col_step/2
                            y = r * row_step + 10
                            ax.text(x, y, classification_classes[int(f"{value[f"image_{i+1}"][cell_num]}")], color='white', ha='center', va='top', fontsize=10)
                            cell_num +=1
                   
                    ax.plot([w, w], [0, h], 'k-', linewidth=0.8)
                    ax.plot([0, w], [h, h], 'k-', linewidth=0.8)

                    ax.axis("off")
                    st.pyplot(fig)

            

            if st.session_state.DISPLAY:
                col_img, col_btn = st.columns([3, 1])
                with col_btn:
                    rgb_col=st.button("In RGB",on_click=show_rgb)
                    ndvi=st.button("Vegetation Index",on_click=show_ndvi)
                    ndwi=st.button("Water Bodies",on_click=show_ndwi)
                    ndmi=st.button("Moisture Index",on_click=show_ndmi)
                with col_img:
                    for i in list_main:
                        with rasterio.open(i) as src:
                                array=src.read()
                        t=array.shape[1]%64
                        array=array[:,:-t,:-t]
                        if st.session_state.index=="rgb":
                            rgb = np.stack((array[4,:,:],array[3,:,:],array[2,:,:]), axis=-1)# read first band
                            rgb=rgb/10000
                            fig, ax = plt.subplots()
                            ax.imshow(rgb)
                            ax.set_title("RGB Image")
                            ax.axis("off")

                            st.pyplot(fig)
                
            
                        elif st.session_state.index=="ndvi":
                            ndvi_ = (array[8,:,:]-array[4,:,:])/(array[8,:,:]+array[4,:,:])
                            fig, ax = plt.subplots()
                            ax.imshow(ndvi_,cmap="RdYlGn")
                            ax.set_title("Vegetation Index")
                            ax.axis("off")

                            st.pyplot(fig)

                        elif st.session_state.index=="ndwi":
                            ndwi_ = (array[3,:,:]-array[8,:,:])/(array[3,:,:]+array[8,:,:]+ 1e-9)
                            fig, ax = plt.subplots()
                            ax.imshow(ndwi_,cmap="RdBu")
                            ax.set_title("Water Bodies")
                            ax.axis("off")

                            st.pyplot(fig)

                        elif st.session_state.index=="ndmi":
                            ndmi_ = (array[8,:,:]-array[11,:,:])/(array[8,:,:]+ array[11,:,:] + 1e-9)
                            fig, ax = plt.subplots()
                            ax.imshow(ndmi_,cmap="RdBu")
                            ax.set_title("Moistur Index")
                            ax.axis("off")

                            st.pyplot(fig)
                

if page == "Get Data":
    if "script_ran" not in st.session_state:
        st.session_state.script_ran = False
    if "form_saved" not in st.session_state:
        st.session_state.form_saved = False
    if "num_images" not in st.session_state:
        st.session_state.num_images=0

    state={}
    with st.form(key="entry_form"):

        st.subheader("Define new Task Parameters")
        state["1"]=st.text_input("Define a task name")
        state["2"]=lon = st.number_input(
                                        "Enter longitude (e.g., 80.220000)",
                                        format="%.6f",
                                        step=0.000001
                                        )
        state["3"]=lon = st.number_input(
                                        "Enter latitude (e.g., 80.220000)",
                                        format="%.6f",
                                        step=0.000001
                                        )
        state["4"]=st.select_slider("Select to radius",options=[1,2,3,4,5])
        state["5"]=st.date_input("Enter start date")
        state["6"]=st.date_input("Enter end date")

        submit_button =st.form_submit_button(label="Save")
        if submit_button:
            if not all(state.values()):
                st.warning("Please fill in all enteries")
            elif not st.session_state.script_ran:
                st.session_state.saved_parameters = state
                st.session_state.form_saved = True
                st.markdown("#### **Saved Successfully**")
            elif st.session_state.script_ran:
                st.markdown(f"#### Task has been started!")
            
                


    if st.session_state.form_saved:
        confirm = st.button("START RETRIEVING DATA", disabled=st.session_state.script_ran)
        if st.session_state.script_ran:
            st.markdown(
        f"#### Your images are being downloaded.    \n"

        f"#### Estimated time: **{st.session_state.num_images * 0.67} minutes**"
    )



        if confirm and not st.session_state.script_ran:
            parameters = st.session_state.saved_parameters

            st.session_state.num_images = earthengine.get_image(
                parameters["1"], parameters["2"], parameters["3"],
                parameters["4"], str(parameters["5"]), str(parameters["6"])
            )
            if st.session_state.num_images > 0 :
                st.session_state.script_ran = True
            st.success(f"{st.session_state.num_images} found")
            if st.session_state.num_images != 0 :
                st.markdown(f"### Task started! Images loading... _Estimated time: {st.session_state.num_images*0.67} mins_")
    if not st.session_state.form_saved:
        st.info("Fill up the details to start retrieving data")
