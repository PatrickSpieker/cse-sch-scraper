import re
from pprint import pprint
import pygraphviz as pgv


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
with open("data/raw-data.txt", "r") as f:
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
                #off_w is offered with
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
                        #append the ENTIRE tuple of options to the prereq list
                        p_tup = tuple(p.findall(i))
                        prereqs.append(p_tup)
                        #the prereq list is tuple-ified at the end of the process
                    else:
                        p = re.compile("[A-Z].[A-Z]{1,3}\s\d\d\d")
                        #append EACH ITEM from the list of options
                        for j in p.findall(i):
                            prereqs.append(j)

                #making prereqs immutable via tuple
                prereqs = tuple(prereqs)

            courses.append(Course(name, desc, course_id, prereqs, off_w, level))            

#print testing
#for course in courses:
#    print course.course_id + ": " + str(course.prereqs)

#Use of constructed data below 
#==========================

#instantiating graph with pgv
G = pgv.AGraph(directed=True, overlap = False, splines="polyline",
                nodesep=2.0, sep = +0.25)


#connecting courses with prereqs
for course in courses:
    #checking for prereqs
    if course.prereqs:
        #setting up counter to change color of edge ->
        #(cont) if there are multiple sets of prereq options
        sets_option = 0

        for prereq in course.prereqs:
            #colors for different sets of prereq options
            colors = ["red", "green", "blue", "purple", "orange", "pink"]
            #determining whether there are prereq options (in a tuple)
            if type(prereq) is tuple:
                #looping through the ACTUAL prereq courses inside tuple
                for act_prereq in prereq:
                    #adding edge to graph
                    G.add_edge(act_prereq, course.course_id)
                    #formatting edge
                    e = G.get_edge(act_prereq, course.course_id)
                    #adding specific color to prereq options
                    e.attr["color"] = colors[sets_option]
                    for node in (act_prereq, course.course_id):
                        n = G.get_node(node)
                        n.attr["fontsize"] = 8.0
                #incrementing color option
                sets_option += 1
            else:
                #adding edge to graph
                G.add_edge(prereq, course.course_id)
                #formatting edge
                e = G.get_edge(prereq, course.course_id)
                e.attr["color"] = "black"
                #formatting both nodes
                for node in (prereq, course.course_id):
                    n = G.get_node(node)
                    n.attr["fontsize"] = 8.0
                    

G.layout(prog="neato")
G.draw("degree_graph.png")


