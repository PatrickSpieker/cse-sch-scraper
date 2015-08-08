import re
from pprint import pprint
import networkx as nx
import matplotlib.pyplot as plt

class Course:
    """Template for course using data from text file"""
    def __init__(self, name, desc, course_id, prereqs, off_w, level):
        self.name = name
        self.course_id = course_id
        self.prereqs = prereqs
        self.off_w = off_w
        self.desc = desc
        self.level = level

#empty list for all Course objects
courses = []

#opening file
with open("raw-data.txt", "r") as f:
    for line in f:
        #finding lines with title of course 
        if line[0:3] == "CSE":
            #index of "("-1 is index of space after name
            name = line[8:line.find("(")-1]
            course_id = line[0:7]

            #access line after line containing name; next line has description
            next_line = next(f)

            #finding index of character after "Prerequisite"
            prereq_ind = next_line.find("Prerequisite: ")
            len_prereq = len("Prerequisite: ")
            
            #finding and assigning description
            desc = next_line[:prereq_ind]
            
            #assigning level
            level = line[4:5]
            
            #starting search for prereqs
            prereqs = []
            #checking to see if any prereq's exist
            #no they don't
            if prereq_ind == -1:
                prereqs = None
                off_w = None
            #yes they do
            else:
                final_part = next_line[prereq_ind+len_prereq:]
                final_part_list = final_part.split("Offered")
                #all of these now must have prereq's
                prereq_raw = final_part_list[0]
                if len(final_part_list) == 2: 
                    #only some will have joint classes
                    off_w_raw = final_part_list[1]
                    off_re = re.compile("[A-Z].[A-Z]{1,3}\s\d\d\d")
                    off_w = off_re.findall(off_w_raw)
                else:
                    #if they don't, connect this with correct variable
                    off_w = None
                #splitting into each seperate prereq
                prereq_split = prereq_raw.split(";")
                #iterating through and regexing out excess
                for i in prereq_split:
                    if "or" in i:
                        p = re.compile("[A-Z].[A-Z]{1,3}\s\d\d\d")
                        #append the ENTIRE list of options to the prereq list
                        prereqs.append(p.findall(i))
                    else:
                        p = re.compile("[A-Z].[A-Z]{1,3}\s\d\d\d")
                        #append EACH ITEM from the list of options
                        for j in p.findall(i):
                            prereqs.append(j)

            courses.append(Course(name, desc, course_id, prereqs, off_w, level))            

G = nx.Graph()
g = {}
for course in courses:
    if course.prereqs == None:
        #g[course.course_id] = []
        #adding a node for each course w/o prereq
        G.add_node(course.course_id)
    else:
        #g[course.course_id] = course.prereqs
        #adding a node for each course w/ prereq
        G.add_node(course.course_id)
        for prereq in course.prereqs:
            #catching unhashable list error
            try:
                G.add_edge(course.course_id, prereq)
            except:
                pass

nx.draw(G)
plt.show()




        
            

