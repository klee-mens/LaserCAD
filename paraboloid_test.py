# -*- coding: utf-8 -*-
"""
Created on Mon Dec 18 13:37:45 2023

@author: 12816
"""

import numpy as np
from sympy import symbols, Eq, solve, I
from sympy.abc import x, y, z, t
a = 1 

def find_paraboloid_line_intersections(paraboloid_vertex, paraboloid_axis, line_point, line_direction):
    """
    Find intersection points of a rotating paraboloid and a line in 3D space.
    
    :param paraboloid_vertex: Vertex (origin) of the paraboloid (tuple of 3 floats)
    :param paraboloid_axis: Axis direction of the paraboloid (tuple of 3 floats)
    :param line_point: A point on the line (tuple of 3 floats)
    :param line_direction: Direction vector of the line (tuple of 3 floats)
    :return: A list of intersection points (if any)
    """
    # Function to create a rotation matrix that aligns a vector with the y-axis
    def rotation_matrix_to_align_vector_with_y_axis(vector):
        vector = np.array(vector)
        vector = vector / np.linalg.norm(vector)
        axis = np.cross(vector, [0, 1, 0])
        axis = axis / np.linalg.norm(axis)
        angle = np.arccos(np.dot(vector, [0, 1, 0]))
        K = np.array([[0, -axis[2], axis[1]], [axis[2], 0, -axis[0]], [-axis[1], axis[0], 0]])
        R = np.eye(3) + np.sin(angle) * K + (1 - np.cos(angle)) * (K @ K)
        return R

    # Translate and rotate the line
    translated_line_point = np.array(line_point) - np.array(paraboloid_vertex)
    R = rotation_matrix_to_align_vector_with_y_axis(paraboloid_axis)
    rotated_translated_line_point = R @ translated_line_point
    rotated_translated_line_direction = R @ np.array(line_direction)

    # Update line equation in rotated and translated system
    line_eq_rotated_translated = {
        x: rotated_translated_line_point[0] + t * rotated_translated_line_direction[0],
        y: rotated_translated_line_point[1] + t * rotated_translated_line_direction[1],
        z: rotated_translated_line_point[2] + t * rotated_translated_line_direction[2]
    }

    # Paraboloid equation in the rotated system (axis aligned with y-axis)
    paraboloid_eq = Eq(y, a * (x**2 + z**2))

    # Solve for t
    substituted_eq = paraboloid_eq.subs({x: line_eq_rotated_translated[x], y: line_eq_rotated_translated[y], z: line_eq_rotated_translated[z]})
    t_values = solve(substituted_eq, t)
    t_values = [val.evalf() for val in t_values if val.is_real]

    # Calculate intersection points
    intersection_points = [tuple(line_eq_rotated_translated[var].subs(t, t_val) for var in (x, y, z)) for t_val in t_values]

    # Transform intersection points back to original coordinate system
    R_inv = np.linalg.inv(R)
    return [np.array(paraboloid_vertex) + R_inv @ np.array(point) for point in intersection_points]

# Example usage
paraboloid_vertex = (0, 0, 0)
paraboloid_axis = (1, 0, 0)
line_point = (-1, 0, 0)  # Example values
line_direction = (1, 0.01, 0)  # Example values

# Find intersection points
intersection_points = find_paraboloid_line_intersections(paraboloid_vertex, paraboloid_axis, line_point, line_direction)
print(intersection_points)

