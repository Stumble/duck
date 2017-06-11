


with open("build-ndns.log") as f:
    content = f.readlines()
    for line in content:
        components = line.split()
        if 'runner' in components[1]:
            mystr = line[line.find(" [") + 2: line.find("]") ]
            parameters = mystr.split(',')
            trimed_parameter = [x[x.find("'") + 1 : -1] for x in parameters]
            trimed_parameter.append("-emit-ast")
            ans = " ".join(trimed_parameter)
            print ans
            print ""
