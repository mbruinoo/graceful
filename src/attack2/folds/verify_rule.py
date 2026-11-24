# verify_rule.py -- does a build (list of steps from lib.replay) obey RULE=R ?  Used by verify.py and rulecheck.py.
def obeys(n,steps,R):
    age={}                      # hole cell -> creation time; gap cells are the unused cells not in `age`
    for i,s in enumerate(steps):
        x,y=s['x'],s['y']; used_before=None
        if x in age:            # F: fill a hole
            others=[h for h in age if h!=x]
            if R&8 and any(age[h]<age[x] for h in others): return False,'fifo'
            if R&16 and any(age[h]>age[x] for h in others): return False,'lifo'
            if R&32 and any(h<x for h in others) and any(h>x for h in others): return False,'ends'
            del age[x]; continue
        # x is in the gap: the gap is the run containing x minus nothing (holes are isolated single cells, never adjacent to the gap by construction; checked)
        lo,hi=s['own']
        if any(lo<=h<=hi for h in age): return False,'hole inside gap run'
        r=(x-lo) if y>x else (hi-x); c=(hi-lo)-r
        if r>=1 and c>=1:
            if r==1: hole=x-1 if y>x else x+1
            elif c==1:
                if R&2: return False,'back skip'
                hole=x+1 if y>x else x-1
            else: return False,'split into two long runs'
            age[hole]=i+1
        elif c==0 and r>=1:
            if R&4: return False,'back step'
    return True,''
