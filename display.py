
import os, shutil
import subprocess

def parse_filename(fname):
    "break filename into tuple"
    '''
    This would have worked only with blackboard submission, but not with github submissions. so you can probably removed it.
    '''
    bname = os.path.basename(fname)
    _, file = os.path.split(fname)
    try:
        lst = file.split('_')
        task = lst[0]
        stname = lst[1]
        labfile = lst[-1]
        if stname == labfile:
            stname = ""
    except (ValueError, IndexError):
        task = ""
        stname = ""
        labfile = file
    return (bname, task, stname, labfile)

def make_str_uniq(target, comp):
    "strip out in common btw tar and comp"
    tl = target.split('/')
    cl = comp.split('/')
    out = ''
    for i, chunk in enumerate(tl):
        try:
            if chunk == cl[i]:  # any part of filepath in common to be removed
                tl.remove(chunk)
                cl.remove(chunk)
        except IndexError:
            pass
    for i, chunk in enumerate(tl):  # this should remove parts of each string
        try:  # not working yet tho
            out += chunk.replace(cl[i], '')
        except IndexError:
            pass 
    return out

def prettify(index, result, width=160):

    mid = 20
    col = int((width - mid) / 2)
    string = ''
    s, p, o = result.tup()
    l = make_str_uniq(str(s), str(o))
    r = make_str_uniq(str(o), str(s))
    string += f"{index:>5}. "
    string += f"{l:<{30}}"
    string += f"\033[1m{p:^10.2%}"
    string += f"\033[0m{r:>{30}}"
    #string += '\n'
    print(string)

def fancy_print_results(objlist, threshold):
    resultlist = []
    for r in objlist:
        if r.has_matches():
            #print(r.pretty_matches())
            for match in r.matches():
                resultlist.append(match)  # collate all matches
    resultlist.sort(reverse=True)  # hope this works!
    for i, r in enumerate(resultlist):
        prettify(i, r)
    return resultlist

def print_dict_results(rdict, threshold):
    "all that hard work pays off"
    global args
    width = shutil.get_terminal_size(fallback=(160, 24)).columns  # not using this, print relative paths instead
    middle = 20
    lr = int((width - middle) / 2)
    for index, w in enumerate(sorted(rdict, key=rdict.get, reverse=True), start=1):  # sort the dict by value (pcnt), hi to lo
        if rdict[w] >= threshold:
            common = os.path.commonpath([w[0], w[1]])
            lb = os.path.relpath(w[0], start=common)
            lfile = make_str_uniq(w[0], w[1]) # lb/rb are returning complete filename
            left = f"{lfile}"[lr * -1:]  # print just the filename
            rb = os.path.relpath(w[1], start=common)
            rfile = make_str_uniq(w[1], w[0])
            right = f"{rfile}"[lr * -1:]
            midstring = rdict[w]
            print(f"{index:>3}. {left : >30}\t{midstring : ^.1%}\t{right : <30}")

def call_diff_exec(results):
    "open the suspicious files using diff prog"
    prog = ['code', '--diff']
    user_choice = ''
    max = len(results)
    while user_choice != 'q':
        user_choice = input(f'Enter selection: 0-{max-1} or \'q\' to exit: ')
        if user_choice == 'q':
            break
        try:
            assert 0 <= int(user_choice) < max
        except (AssertionError, TypeError):
            print('Invalid!')
            continue
        user_choice = int(user_choice)
        s, p, o = results[user_choice].tup()
        cmd = prog + [str(s), str(o)]
        x = subprocess.run(cmd)
        #s.run()


if __name__ == "__main__":
    # testing
    t1 = 'assignment-1-upwinderjitsingh/code/assignment1.py'
    t2 = 'assignment-1-ArpinderKaur/assignment1.py'
    print(make_str_uniq(t1, t2))