
# coding: utf-8

# In[688]:

import re, math, fileinput
import tree, bigfloat


# In[694]:

def parse(states, bps, best, line, length=1):
    if length == len(line)+1:
        return states, bps, best
    else:
        for s1 in states:
            for s2 in states:
                if s1[2]==s2[1] and s2[2]-s1[1]==length:       
                    with open('pcfg') as rules:
                        for rule in rules:
                            backptr = {}
                            if re.compile('.*->\s'+re.sub('\*','\*',s1[0])+' '+re.sub('\*','\*',s2[0])+r'\s#\s.*').match(rule):
                                logprob = best[s1]+best[s2]+bigfloat.log10(bigfloat.bigfloat(float(re.match(r'.*\s#\s(.*)\b', rule).group(1))))
                                new_state = (re.match(r'(.*)\s->.*', rule).group(1), s1[1], s2[2])
                                if new_state not in states:
                                    states.append(new_state)
                                    best[new_state]=logprob
                                    bps[new_state] = (re.match(r'(.*)\s#.*', rule).group(1),s1[2]) 
                                elif logprob > best[new_state]:
                                    best[new_state]=logprob
                                    bps[new_state] = (re.match(r'(.*)\s#.*', rule).group(1),s1[2])
        length += 1
        return parse(states, bps, best, line, length)


# In[695]:

def trees(parent, bps):
    childs = re.match('.*->\s(.*)$', bps[parent][0]).group(1).split(' ')
    if len(childs) == 1:
        return "(%s %s)" % (parent[0], " ".join(childs))
    if len(childs) > 1:
        child1 = (childs[0], parent[1], bps[parent][1])
        child2 = (childs[1], bps[parent][1], parent[2])
        return "(%s %s)" % (parent[0], " ".join([trees(child1, bps), trees(child2, bps)]))


# In[696]:

def parser(line):
    states = []
    bps = {}
    best = {}
    for i in xrange(len(line)):
        found = False
        pattern = '.*->\s'+re.sub('\?','\?',re.sub('\.','\.',line[i]))+r'\s#\s.*'
        with open('pcfg') as rules:
            for rule in rules:
                if re.match(pattern, rule):
                    X = re.match(r'(.*)\s->.*', rule).group(1)
                    logprob = bigfloat.log10(bigfloat.bigfloat(float(re.match(r'.*\s#\s(.*)\b', rule).group(1))))
                    states.append((X,i,i+1))
                    best[(X,i,i+1)]=logprob
                    bps[(X,i,i+1)] = (re.match(r'(.*)\s#.*', rule).group(1),)
                    found = True
        if found == False:
            unk_pattern = re.compile(r'.*<unk>.*')
            with open('pcfg') as rules:
                for rule in rules:
                    if unk_pattern.match(rule):
                        X = re.match(r'(.*)\s->.*', rule).group(1)
                        logprob = bigfloat.log10(bigfloat.bigfloat(float(re.match(r'.*\s#\s(.*)\b', rule).group(1))))
                        states.append((X,i,i+1))
                        best[(X,i,i+1)]=logprob
                        bps[(X,i,i+1)] = (re.match(r'(.*)\s#.*', rule).group(1),)
                        found = True
    states, bps, best = parse(states, bps, best, line)
    root = ('TOP', 0, len(line))
    try:
        return trees(root, bps)
    except:
        return ''

if __name__ == '__main__':
    results = ''
    for s in fileinput.input():
        line = s.rstrip().split(' ')
        results += parser(line)+'\n'
    print results

