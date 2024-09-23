import plotly

# Function to calculate the intersection of two lines
def line_intersection(point11, point12, point21, point22):
    """
    Calculate the intersection point of two lines.
    Line 1 is from (x1[0], y1[0]) to (x1[1], y1[1])
    Line 2 is from (x2[0], y2[0]) to (x2[1], y2[1])
    Returns (x, y) of the intersection point.
    """
    # Line 1: (x1_1, y1_1) to (x1_2, y1_2)
    x1_1, y1_1 = point11[0], point11[1]
    x1_2, y1_2 = point12[0], point12[1]
    
    # Line 2: (x2_1, y2_1) to (x2_2, y2_2)
    x2_1, y2_1 = point21[0], point21[1]
    x2_2, y2_2 = point22[0], point22[1]
    
    # Line 1 represented as a1*x + b1*y = c1
    a1 = y1_2 - y1_1
    b1 = x1_1 - x1_2
    c1 = a1 * x1_1 + b1 * y1_1

    # Line 2 represented as a2*x + b2*y = c2
    a2 = y2_2 - y2_1
    b2 = x2_1 - x2_2
    c2 = a2 * x2_1 + b2 * y2_1

    # Determinant
    determinant = a1 * b2 - a2 * b1

    if determinant == 0:
        # Lines are parallel
        return None
    else:
        # Solve the system of linear equations
        x = (b2 * c1 - b1 * c2) / determinant
        y = (a1 * c2 - a2 * c1) / determinant
        return (x, y)

import numpy as np

def calculate_vector(point1, point2):
    """Calculate the vector from point1 to point2."""
    return np.array(point2) - np.array(point1)

def move_point(point, vector, distance):
    """Move a point along a vector by a specified distance."""
    # Normalize the vector
    length = np.linalg.norm(vector)
    if length == 0:
        return point  # No movement if the vector is zero

    normalized_vector = vector / length
    # Calculate the new point
    new_point = point + normalized_vector * distance
    return new_point


def add_text(fig, text, xPosition, yPosition, textSize):
    fig.add_annotation(dict(font=dict(size=textSize, color = "black"),
                                            x = xPosition,
                                            y = yPosition,
                                            showarrow=False,
                                            text=text,
                                            textangle=0,
                                            xanchor='left',
                                            xref="x",
                                            yref="y"))
