with open("raw-data.txt", "r") as f:
    objects = []
    for line in f:
        #finding lines with title of course 
        if line[0:3] == "CSE":
            #index of "("-1 is index of space after name
            name = line[8:line.find("(")-1]
            course_id = line[0:7]
           

            #access line after name, with description
            prereq = []
            next_line = next(f)
            #stripping line to after prerequisite
            index_resp = next_line.find("Prerequisite:")
            if index_resp == -1:
                reqs = None
            else:
                len_prereq = len("Prerequisite:")
                #cutting line to end of "Prerequisite", stripping escape chars 
                #and "either"
                reqs = next_line[index_resp+len_prereq+1:].strip("\r\n.").\
                        replace("either", "")

                list = reqs.split("Offered")
                print list
                                
            #setting description
            desc = next_line[:index_resp]

            #print reqs

