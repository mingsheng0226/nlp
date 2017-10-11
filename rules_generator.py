
# coding: utf-8

# In[74]:

import sys, fileinput, collections
import tree


# In[95]:

rules = collections.defaultdict(int)
heads = collections.defaultdict(int)


# In[96]:

def rule(node, rules):
    if len(node.children) > 0:
        rules[node.label, ' '.join(c.label for c in node.children)] += 1
        for child in node.children:
            rule(child, rules)
    else:
        return None


# In[97]:

def head(node, heads):
    if None:
        return None
    else:
        heads[node.label] += 1
        for child in node.children:
            head(child, heads)


# In[86]:

for line in fileinput.input():
    t = tree.Tree.from_str(line)
    _, _ = rule(t.root,rules), head(t.root,heads)


# In[87]:

result = []
pcfg = {}
for k in rules:
    pcfg[k] = float(rules[k])/heads[k[0]]
    result.append(' -> '.join(k)+' # %.3f' % (pcfg[k]))


# In[98]:

print '\n'.join(result)


# In[94]:

#for k,v in pcfg.iteritems():
#    if v == max(pcfg.values()):
#        print k, rules[k]

