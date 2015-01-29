import itertools

def uniqify(seq):
   # order preserving
   checked = []
   for e in seq:
       if e not in checked:
           checked.append(e)
   return checked

def flatten(lst):
    return itertools.chain.from_iterable(lst)
