# UW Schedule Scraper

UW Schedule Scraper goes through University of Washington
course descriptions and visualizes course pathways in a
given UW department. 

Currently under development. 
###Features
 * Visualizes relationships between courses in a given UW department
 * Automatic prereq options set differentiation
 * Works for any department at UW
###Installation
######Dependancies
 * BeautifulSoup 4.4.0
 * GraphViz 0.4.6
 * pyGraphViz 1.3rc2
 * lxml 3.4.4
 * requests 2.7.0
 * wheel 0.24.0
   
###Usage
Takes uppercase department code after main.py.

Department codes can be found at:
http://www.washington.edu/about/academics/departments/
```bash
python main.py [dept-code]
```

Written in Python 2.


