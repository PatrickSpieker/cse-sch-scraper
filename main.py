#importing:
#regex, pygraphviz, requests, urllib, argv, and beautiful soup
import re
import pygraphviz as pgv
import requests
import urllib
from sys import argv
from bs4 import BeautifulSoup

class Course:
    """Template for course using data from text file"""
    def __init__(self, name, course_id, prereqs, off_w):
        self.name = name
        self.course_id = course_id
        self.prereqs = prereqs
        self.off_w = off_w


dept = str(argv[1])

#empty list for all Course objects
courses = []
url = "http://www.washington.edu/students/crscat/" + dept.lower() + ".html"
#fetching HTML
urllib.urlretrieve(url, "test.html")
data = open("test.html","r").read()
soup = BeautifulSoup(data, "lxml")
#constructing regex pattern
patt = dept.lower()+"\d\d\d"


#opening file
with open("test.html", "r") as f:
    data = f.read()
    soup = BeautifulSoup(data, "lxml")
    for tag in soup.find_all("a", attrs={"name":re.compile(patt)}):
        for child in tag.children:

            #identifying where prereqs will be in text
            prereq_start = str(child).find("Prerequisite: ")
            len_prereq = len("Prerequisite: ")

            #empty prereq list
            prereqs = []
            #checking to see if prereqs exist
            if prereq_start == -1:
                #no they don't
                prereqs = None
                #off_w is offered with
                off_w = None
            else:
                #yes they do
                final_part = str(child)[prereq_start+len_prereq:]
                prereq_end = final_part.find("<br/>")
                final_part = final_part[:prereq_end]

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

            if child.b:
                #defining string with course info
                course_str = child.b.string
                #finding index of end of course string
                course_str_end = course_str.find("(")-1
                #finding length of course_id
                id_end = len(dept.lower())+4 #length of space and number
                #defining course id, ex: CSE 143
                course_id = course_str[0:id_end]
                #defining actual name of the course
                name = course_str[8:course_str.find("(")-1]
            #instantiate object
            courses.append(Course(name, course_id, prereqs, off_w))            


#instantiating graph with pgv
G = pgv.AGraph(directed=True, overlap = False, splines="polyline",
                nodesep=2.0, sep = +0.25)


#connecting courses with prereqs
for course in courses:
    print course.course_id
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
                    n.attr["fontsize"] = 7.0
                    

G.layout(prog="neato")
G.draw("degree_graph.png")

