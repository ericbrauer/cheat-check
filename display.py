
import os, shutil
import subprocess


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
                if match.pcnt >= threshold:  # filter out after auto
                    resultlist.append(match)  # collate all matches
    resultlist.sort(reverse=True)  # hope this works!
    for i, r in enumerate(resultlist):
        prettify(i, r)
    return resultlist


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