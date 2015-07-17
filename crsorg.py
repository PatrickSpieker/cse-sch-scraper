

class Course:
    "Template for course using data from text file"
    def __init__(self, prereqs, coreqs, off_w, course_id, desc, name):
        self.name = name
        self.course_id = course_id
        self.prereqs = prereqs
        self.coreqs = coreqs
        self.off_w = off_w
        self.desc = desc

#opening file
with open("raw-data.txt", "r") as f:
    objects = []
    for line in f:
        #finding lines with title of course 
        if line[0:3] == "CSE":
            #index of "("-1 is index of space after name
            name = line[8:line.find("(")-1]
            course_id = line[0:7]
            #setting description
            desc = next_line[:index_resp]


            #access line after name, with description
            prereq = []
            next_line = next(f)
            #stripping line to after prerequisite
            index_resp = next_line.find("Prerequisite:")
            
            len_prereq = len("Prerequisite:")
            #if no prerequisite found
            if index_resp == -1:
                prereqs = None
            else:
                #stripping out word "prerequisite"
                piece = next_line[index_resp+len_prereq:]
                if "either" in piece:
                    #after "either"'s index
                    index_piece = piece.find("either")+len("either")+1
                    #semi-colon (signal of next prereq) index
                    end_index_piece = piece.find(";", index_piece)
                    prereq.append(piece[index_piece:end_index_piece].strip(".\r, ").split(" "))
            
            objects.append(Course(prereq, course_id, desc, name))

            
            





        
            

