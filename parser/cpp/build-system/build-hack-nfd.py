


with open("build-nfd.log") as f:
    content = f.readlines()
    for line in content:
        if 'runner' not in line:
            continue
        (before, kw, after) = line.partition('clang++')
        ans = kw + " -emit-ast " + after
        print ans
        print ""
