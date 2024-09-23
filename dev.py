fig.add_trace(go.Scatter(
        x=[rect1_D[0], rect1_C[0], rect1_B[0], rect1_A[0]], 
        y=[rect1_D[1], rect1_C[1], rect1_B[1], rect1_A[1]], 
        mode='markers+text',  # This adds both markers and text
        marker=dict(color='green', size=10), 
        text=["rect1_D", "rect1_C", "rect1_B", "rect1_A"],  # Text label for the marker
        textposition="top right",  # Position of the text relative to the marker
        name='Lower Intersection'
    ))

    ## points of plate 2
    fig.add_trace(go.Scatter(
        x=[rect2_D[0], rect2_C[0], rect2_B[0], rect2_A[0]], 
        y=[rect2_D[1], rect2_C[1], rect2_B[1], rect2_A[1]], 
        mode='markers+text',  # This adds both markers and text
        marker=dict(color='red', size=10), 
        text=["rect2_D", "rect2_C", "rect2_B", "rect2_A"],  # Text label for the marker
        textposition="top right",  # Position of the text relative to the marker
        name='Lower Intersection'
    ))

    ## intersection points
    fig.add_trace(go.Scatter(x=[intersection_upper[0]], y=[intersection_upper[1]], 
                            mode='markers', marker=dict(color='blue', size=10), name='Lower Intersection'))
    fig.add_trace(go.Scatter(x=[intersection_lower[0]], y=[intersection_lower[1]], 
                            mode='markers', marker=dict(color='yellow', size=10), name='Lower Intersection'))