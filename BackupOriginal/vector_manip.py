import pixy
import operator
from math import sqrt, acos, degrees
from ctypes import *
from pixy import *
import numpy as np
import matplotlib.pyplot as plt

def get_angle(line):
    return acos(line[0] / get_line_distance(line)) # angle in radians

def print_vectors(vectors):
    equiv_vector = add_vectors(vectors)
    plt.ion()
    plt.xlim(0,78)
    plt.ylim(51,0)

    for vector in vectors:
        plt.plot([vector.m_x0, vector.m_x1],[vector.m_y0, vector.m_y1],marker = 'o')
    plt.plot([78/2, 78/2 - equiv_vector[0]],[51, 51 - equiv_vector[1]], marker='x')

    plt.draw()
    plt.pause(0.000001)
    plt.clf()
    print ("ANGLE", degrees(get_angle(equiv_vector)))

def get_line_distance(line):
    return sqrt(line[0]**2 + line[1]**2)

def get_distance(vector):
    return sqrt(vector.m_x0**2 + vector.m_y0**2)

def get_longest_vectors(vectors, v_count, number_of_vectors=5):
    ## returns a list (vector, distance) of the 5 longest vectors
    distances = {}
    number_of_vectors = v_count if v_count < number_of_vectors else number_of_vectors
    for i in range(v_count):
        distances[vectors[i]] = get_distance(vectors[i])

    return list(sorted(distances, key=distances.get, reverse=False)[:number_of_vectors]), number_of_vectors

def filter_straight_roi(vectors, v_count):
    roi = {"x0":0 ,"y0":31 , "x1":78, "y1":51} ## top left and right bottom points of a rectangle
    vectors_in_roi = []
    for i in range(v_count):
        if ((roi["x0"] <= vectors[i].m_x0 <= roi["x1"] and
            roi["y0"] <= vectors[i].m_y0 <= roi["y1"]) or
            (roi["x0"] <= vectors[i].m_x1 <= roi["x1"] and
            roi["y0"] <= vectors[i].m_y1 <= roi["y1"])):
            vectors_in_roi.append(vectors[i])
    return list(vectors_in_roi)
            
def filter_vectors(vectors, v_count):
    longest_vectors, number_of_vectors = get_longest_vectors(vectors, v_count)
    return longest_vectors    

    #print_vectors(longest_vectors)

    #filtered_vectors = filter_straight_roi(longest_vectors, longest_vectors_dist[1])
    #print_vectors(filtered_vectors)
    #return filtered_vectors

def add_vectors(vectors_dist):
    equiv_vector = [0,0]
    #print (vectors_dist)
    for vector in vectors_dist:
        #print (vector)
        equiv_vector[0] += (vector.m_x0 - vector.m_x1)
        equiv_vector[1] += abs(vector.m_y0 - vector.m_y1)
    print (78/2 - equiv_vector[0], 51 - equiv_vector[1])
    return equiv_vector
