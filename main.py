import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import math
import numpy as np
from utils import line_intersection, calculate_vector, move_point, add_text

st.markdown('''
<style>
.katex-html {
    text-align: left;
}
</style>''',
unsafe_allow_html=True
)

# Title of the app
st.title("Welding Designer")

# select mode
col1, col2, col3 = st.columns(3)
with col1:
    designMode = st.selectbox("Select the design mode", ["Single Weld", "Multiple Welds"])

st.subheader("Input Paremeter")

# TABLE
if designMode == "Multiple Welds":
    df = pd.DataFrame(
        [
            {"Select": True, "Title": "Weld1", "Grade 1": "S235", "Thk 1": 40, "Angle 1": 90, "Grade 2": "S235", "Thk 2": 50, "Angle 2": 0, "Intersection Type": "Straight", "Weld on Plate": 1, "Weld Type": "HY", "Throat": 15, "Leg": 20},
            {"Select": True, "Title": "Weld2", "Grade 1": "S235", "Thk 1": 30, "Angle 1": 110, "Grade 2": "S235", "Thk 2": 40, "Angle 2": 20, "Intersection Type": "Straight", "Weld on Plate": 2,"Weld Type": "HY", "Throat": 10, "Leg": 20},
            {"Select": True, "Title": "Weld3", "Grade 1": "S235", "Thk 1": 20, "Angle 1": 135, "Grade 2": "S235", "Thk 2": 20, "Angle 2": 10, "Intersection Type": "Angled", "Weld on Plate": 1,"Weld Type": "HY", "Throat": 7, "Leg": 8},

    ])

    edited_df = st.data_editor(df, hide_index=True, num_rows="dynamic") 

    # get index of the selected table
    ListIndex = [x for x in edited_df["Select"]]
    ListIndexFiltered = [n for n,bool in enumerate(ListIndex) if bool == True]
    index = 0 if not ListIndexFiltered else ListIndexFiltered[0]


    title = [x for x in edited_df["Title"]][index]
    grade1 = [y for y in edited_df["Grade 1"]][index]
    thk1 = [y for y in edited_df["Thk 1"]][index]
    angle1 = [y for y in edited_df["Angle 1"]][index]
    grade2 = [y for y in edited_df["Grade 2"]][index]
    thk2 = [y for y in edited_df["Thk 2"]][index]
    angle2 = [y for y in edited_df["Angle 2"]][index]      
    # weldOnPlate = [y for y in edited_df["Weld on Plate"]][index]
    # intersectionType = [y for y in edited_df["Intersection Type"]][index]
    # weldType = [y for y in edited_df["Weld Type"]][index]
    # weldThickness = [y for y in edited_df["Throat"]][index]
    # weldDepth = int([y for y in edited_df["Leg"]][index])

# SINGLE 
if designMode == "Single Weld":
    col1, col2, col3 = st.columns(3)
    with col1:
        grade1 = st.selectbox("Grade", ["S235"])
        thk1 = int(st.text_input("thickness [mm]", 20) )   # Width of Rectangle 1 in mm
        angle1 = st.slider("Select angle for Line 1 (degrees)", 0, 180, 45)

    with col2:
        grade2 = st.selectbox("Grade ", ["S235"])
        thk2 = int(st.text_input("thickness [mm] ", 20) )   # Width of Rectangle 1 in mm
        angle2 = st.slider("Select angle for Line 2 (degrees)", 0, 180, 45)

    with col3:
        weldType = st.selectbox("Chose Weld", [1, 2])
        weldThickness = int(st.text_input("weld thickness [mm]", 20) )   # Width of Rectangle 1 in mm
        weldDepth = int(st.text_input("weld depth [mm]", 15) )   # Width of Rectangle 1 in mm

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.subheader("Weld Paremeter")
    intersectionType = st.selectbox("Intersection Type", ["Straight", "Angled"])
    weldType = st.selectbox("Weld Type", ["HY", "HV"])
    weldOnPlate = st.selectbox("Weld on Plate", [1, 2])
    if weldType == "HV":
        weldDir = st.selectbox("Weld Direction", [1, 2])
    weldThickness = int(st.text_input("weld thickness [mm]", 20) )   # Width of Rectangle 1 in mm
    if weldType == "HY":
        weldDepth = int(st.text_input("weld depth [mm]", 15) )   # Width of Rectangle 1 in mm

with col2:
    # Set length and individual widths of the rectangles in mm
    length = 150  # Length of each rectangle in mm
    scaling_factor = 1  # Convert mm to plot units (1 unit = 100 mm)
    # Create a Plotly figure
    fig = go.Figure()

    # Convert mm to plot units
    length = length * scaling_factor  
    thk1 = thk1 * scaling_factor
    thk2 = thk2 * scaling_factor

    # Calculate the center line for Line 1
    x1_line = [0, (length + 20) * np.cos(np.radians(angle1))]
    y1_line = [0, (length + 20) * np.sin(np.radians(angle1))]

    # Calculate the center line for Line 2
    x2_line = [0, (length + 20) * np.cos(np.radians(angle2))]
    y2_line = [0, (length + 20) * np.sin(np.radians(angle2))]

    # Calculate the corners of Rectangle 1 (centered around the center line)
    # Calculate the corners of Rectangle 1 (centered around the center line)
    rect1_A = (thk1 / 2 * np.sin(np.radians(angle1)), 
                        -thk1 / 2 * np.cos(np.radians(angle1)))
    rect1_B = (length * np.cos(np.radians(angle1)) + thk1 / 2 * np.sin(np.radians(angle1)), 
                        length * np.sin(np.radians(angle1)) - thk1 / 2 * np.cos(np.radians(angle1)))
    rect1_C = (length * np.cos(np.radians(angle1)) - thk1 / 2 * np.sin(np.radians(angle1)), 
                        length * np.sin(np.radians(angle1)) + thk1 / 2 * np.cos(np.radians(angle1)))
    rect1_D = (-thk1 / 2 * np.sin(np.radians(angle1)), thk1 / 2 * np.cos(np.radians(angle1)))

    # Calculate the corners of Rectangle 2 (centered around the center line)
    rect2_A = (thk2 / 2 * np.sin(np.radians(angle2)), 
                        -thk2 / 2 * np.cos(np.radians(angle2)))
    rect2_B = (length * np.cos(np.radians(angle2)) + thk2 / 2 * np.sin(np.radians(angle2)), 
                        length * np.sin(np.radians(angle2)) - thk2 / 2 * np.cos(np.radians(angle2)))
    rect2_C = (length * np.cos(np.radians(angle2)) - thk2 / 2 * np.sin(np.radians(angle2)), 
                        length * np.sin(np.radians(angle2)) + thk2 / 2 * np.cos(np.radians(angle2)))
    rect2_D = (-thk2 / 2 * np.sin(np.radians(angle2)), thk2 / 2 * np.cos(np.radians(angle2)))

    # Add center lines to the figure
    fig.add_trace(go.Scatter(x=x1_line, y=y1_line, mode='lines', name='Line 1', 
                            line=dict(color='black', dash='dash', width=1)))
    fig.add_trace(go.Scatter(x=x2_line, y=y2_line, mode='lines', name='Line 2', 
                            line=dict(color='black', dash='dash', width=1)))

    # INTERSECTION
    if intersectionType == "Angled":

        # Calculate the intersection of the lower lines (bottom edges)
        intersection_upper = line_intersection(rect1_A, rect1_B, rect2_D, rect2_C)
        intersection_lower = line_intersection(rect1_C, rect1_D, rect2_A, rect2_B)

        # adjust rectangle corners to intersection
        rect1_A = (intersection_upper[0], intersection_upper[1])
        rect2_D = (intersection_upper[0], intersection_upper[1])

        rect1_D = (intersection_lower[0], intersection_lower[1])
        rect2_A = (intersection_lower[0], intersection_lower[1])

        # weld on plate 1
        if weldOnPlate == 1:

            point_W1B = rect1_C
            point_W2B = rect1_B

        # weld on plate 2
        elif weldOnPlate == 2:

            point_W1B = rect2_B
            point_W2B = rect2_C

    elif intersectionType == "Straight": 
        # weld on plate 1
        if weldOnPlate == 1:
            intersection_upper = line_intersection(rect1_A, rect1_B, rect2_D, rect2_C)
            intersection_lower = line_intersection(rect1_D, rect1_C, rect2_D, rect2_C)

            rect1_D = (intersection_lower[0], intersection_lower[1])
            rect2_D = (intersection_lower[0], intersection_lower[1])

            rect1_A = (intersection_upper[0], intersection_upper[1])
            rect2_A = (rect2_A[0] - thk1/2, rect2_A[1])

            point_W1B = rect1_C
            point_W2B = rect1_B

        # weld on plate 2
        elif weldOnPlate == 2:
            intersection_upper = line_intersection(rect1_A, rect1_B, rect2_D, rect2_C)
            intersection_lower = line_intersection(rect1_A, rect1_B, rect2_A, rect2_B)

            rect1_D = (rect1_D[0], rect1_D[1] - thk2/2)
            rect2_D = (intersection_upper[0], intersection_upper[1])

            rect1_A = (intersection_lower[0], intersection_lower[1])
            rect2_A = (intersection_lower[0], intersection_lower[1])

            point_W1B = rect2_B
            point_W2B = rect2_C


    # Visualization for developing
    ## points of plate 1
    # """ 
    # here dev.py
    # """

    # Define rectangles
    # Define lists for Rectangle 1
    x_rect1 = [rect1_A[0], rect1_B[0], rect1_C[0], rect1_D[0]]
    y_rect1 = [rect1_A[1], rect1_B[1], rect1_C[1], rect1_D[1]]

    # Define lists for Rectangle 2
    x_rect2 = [rect2_A[0], rect2_B[0], rect2_C[0], rect2_D[0]]
    y_rect2 = [rect2_A[1], rect2_B[1], rect2_C[1], rect2_D[1]]

    # Add rectangles to the figure
    fig.add_trace(go.Scatter(x=x_rect1 + [x_rect1[0]], y=y_rect1 + [y_rect1[0]], mode='lines', fill='toself', 
                            name='Rectangle 1', fillcolor='rgba(128, 128, 128, 0.5)', 
                            line=dict(color='black', width=1)))
    fig.add_trace(go.Scatter(x=x_rect2 + [x_rect2[0]], y=y_rect2 + [y_rect2[0]], mode='lines', fill='toself', 
                            name='Rectangle 2', fillcolor='rgba(128, 128, 128, 0.5)', 
                            line=dict(color='black', width=1)))

    # WELD VISUAL
    if weldType == "HY":
        ## weld 1
        vector_lower_line = calculate_vector(intersection_lower, point_W1B)
        weld_point_B = move_point(intersection_lower, vector_lower_line, weldThickness)
        vector_lower_line = calculate_vector(intersection_lower, intersection_upper)
        weld_point_C = move_point(intersection_lower, vector_lower_line, weldDepth)
        weld_1_x = [intersection_lower[0], weld_point_B[0], weld_point_C[0]]
        weld_1_y = [intersection_lower[1], weld_point_B[1], weld_point_C[1]]

        ## weld 2
        vector_lower_line = calculate_vector(intersection_upper, point_W2B)
        weld_point_B = move_point(intersection_upper, vector_lower_line, weldThickness)
        vector_lower_line = calculate_vector(intersection_upper, intersection_lower)
        weld_point_C = move_point(intersection_upper, vector_lower_line, weldDepth)
        weld_2_x = [intersection_upper[0], weld_point_B[0], weld_point_C[0]]
        weld_2_y = [intersection_upper[1], weld_point_B[1], weld_point_C[1]]

        fig.add_trace(go.Scatter(x=weld_2_x, y=weld_2_y, mode='lines', fill='toself', 
                            name='Rectangle 2', fillcolor='rgba(255, 0, 0, 0.5)',  # Blue color, 
                            line=dict(color='black', width=1)))

    elif weldType == "HV":
        if weldDir == 1:
            ## weld 1
            vector_lower_line = calculate_vector(intersection_lower, point_W1B)
            weld_point_B = move_point(intersection_lower, vector_lower_line, weldThickness)
            weld_1_x = [intersection_lower[0], weld_point_B[0], intersection_upper[0]]
            weld_1_y = [intersection_lower[1], weld_point_B[1], intersection_upper[1]]
        
        else:
            ## weld 1
            vector_lower_line = calculate_vector(intersection_lower, point_W1B)
            weld_point_B = move_point(intersection_upper, vector_lower_line, weldThickness)
            weld_1_x = [intersection_lower[0], weld_point_B[0], intersection_upper[0]]
            weld_1_y = [intersection_lower[1], weld_point_B[1], intersection_upper[1]]


    fig.add_trace(go.Scatter(x=weld_1_x, y=weld_1_y, mode='lines', fill='toself', 
                            name='Rectangle 2', fillcolor='rgba(255, 0, 0, 0.5)',  # Blue color, 
                            line=dict(color='black', width=1)))

    


    #fig.add_trace(go.Scatter(x=[rect1_C[0]], y=[rect1_C[1]], 
    #                        mode='markers', marker=dict(color='green', size=10), name='Lower Intersection'))

    # text
    textSize = 22
    x1 = 200
    y1 = 150
    add_text(fig, f"<b>Plate 2", x1, y1, textSize)
    add_text(fig, str(grade2), x1, y1-15, textSize)
    add_text(fig, "thk = " + str(thk2) + "mm", x1, y1-30, textSize)
    add_text(fig, "angle = " + str(angle2) + "°", x1, y1-45, textSize)

    x2 = 200
    y2 = 50
    add_text(fig, f"<b>Plate 1", x2, y2, textSize)
    add_text(fig, str(grade1), x2, y2-15, textSize)
    add_text(fig, "thk = " + str(thk1) + "mm", x2, y2-30, textSize)
    add_text(fig, "angle = " + str(angle1) + "°", x2, y2-45, textSize)

    # Update layout to keep axes the same size
    fig.update_layout(
        xaxis_title="X (mm)",
        yaxis_title="Y (mm)",
        width=600,
        height=500,
        xaxis=dict(scaleanchor="y", scaleratio=1, fixedrange=False, visible=False),
        yaxis=dict(scaleanchor="x", scaleratio=1, fixedrange=False, visible=False),
        xaxis_scaleanchor="y",  # Link x and y axis scales
        yaxis_scaleanchor="x",  # Link y and x axis scales
        showlegend=False,    
        margin=dict(t=20, b=40, l=40, r=40) 
    )

    st.subheader("Weld Sketch")

    # Show the plot in Streamlit
    st.plotly_chart(fig)

with st.expander("Expand"):


    # Title for the Streamlit app
    st.title("Fillet Weld Design According to Eurocode")

    # Input values from the user
    st.subheader("Input Parameters")
    # f_u = st.number_input("Tensile strength of the weld metal \(f_u\) [N/mm²]", value=430, step=10)
    # a = st.number_input("Weld throat thickness \(a\) [mm]", value=5, step=1)
    # gamma_Mw = st.number_input("Partial safety factor \( \gamma_{Mw} \)", value=1.25, step=0.01)
    f_u = 490
    a = 20
    gamma_Mw = 1.25


    # Calculate design weld strength
    sqrt_3 = math.sqrt(3)
    f_vw_Rd = f_u / (sqrt_3 * gamma_Mw)

    # Display the design strength formula in LaTeX
    st.subheader("Design strength of the fillet weld:")
    st.latex(r'''
    f_{vw,Rd} = \frac{f_u}{\sqrt{3} \cdot \gamma_{Mw}}
    ''')

    st.latex(f"\\textbf{{Tensile strength of the weld metal }} f_u = {f_u} \\, \\text{{N/mm²}}")
    st.latex(f"\\textbf{{Partial safety factor }} \\gamma_{{Mw}} = {gamma_Mw}")

    # Show calculation result in LaTeX
    st.latex(r"\textbf{Design weld strength} \, f_{vw,Rd}:")
    st.latex(f"f_{{vw,Rd}} = {f_vw_Rd:.2f} \, \text{{N/mm}}^2")

    # Further explanations
    st.latex(r"""
    \text{The design strength } f_{vw,Rd} \text{ determines the maximum stress the weld can safely handle. It depends on the tensile strength of the material and the partial safety factor.}
    """)

    # Calculate resultant stress (example)
    st.subheader("Resultant weld stress")
    st.latex(r"\text{Here we provide an example of the resultant weld stress } \sigma_w.")
    sigma_w_perp = st.number_input("Normal stress \( \sigma_\perp \) [N/mm²]", value=50, step=1)
    tau_w = st.number_input("Shear stress \( \tau_w \) [N/mm²]", value=30, step=1)

    # Resultant stress formula
    sigma_w = math.sqrt(sigma_w_perp**2 + 3 * tau_w**2)

    st.latex(r'''
    \sigma_w = \sqrt{\sigma_\perp^2 + 3 \tau_w^2}
    ''')

    # Display result
    st.latex(f"\\textbf{{Normal stress }} \\sigma_{{\\perp}} = {sigma_w_perp} \\, \\text{{N/mm²}}")
    st.latex(f"\\textbf{{Shear stress }} \\tau_w = {tau_w} \\, \\text{{N/mm²}}")

    # Show the result in LaTeX
    st.subheader("Resultant stress:")
    st.latex(f"\\sigma_w = {sigma_w:.2f} \, \\text{{N/mm²}}")

    # Final verification
    st.subheader("Verification condition:")
    st.latex(r'''
    \sigma_w \leq f_{vw,Rd}
    ''')

    # Comparison
    if sigma_w <= f_vw_Rd:
        st.success(f"The weld is sufficiently dimensioned: \( \sigma_w = {sigma_w:.2f} \leq f_{{vw,Rd}} = {f_vw_Rd:.2f} \, \text{{N/mm²}} \)")
    else:
        st.error(f"The weld is not sufficiently dimensioned: \( \sigma_w = {sigma_w:.2f} > f_{{vw_Rd}} = {f_vw_Rd:.2f} \, \text{{N/mm²}} \)")
