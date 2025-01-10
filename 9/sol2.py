from itertools import repeat

disk_map = input()

# i will just brute force part one
def p1_brute_force(disk_map):
    s, cur = [], 0
    empty = 0
    for i, c in enumerate(disk_map):
        if i % 2 == 0:
            s.extend(repeat(cur, int(c)))
            cur += 1
        else:
            s.extend(repeat(None, int(c)))
            empty += int(c)

    last = 0
    while empty > 0:
        last = s.index(None, last)
        s[last] = s.pop()
        empty -= 1
    return sum(i * n for i, n in enumerate(s))

def format(s):
    res = []
    for tt, nn in s:
        if tt is None:
            res.append("." * nn)
        else:
            res.append(str(tt) * nn)
    return "".join(res)

def get_space_target_index(s, need, target):
    si = ti = None
    for i, (t, c) in enumerate(s):
        if si is None and ti is None and t is None and c >= need:
            si = i
        if t == target:
            ti = i
    return si, ti

def block_checksum(s):
    res = total = 0
    for tt, nn in s:
        total += nn
        if tt is None:
            continue
        # TODO:
        # we can come up with some cheeky formula to improve 
        # (i * tt) + ((i+1) * tt) + ... + ((i + nn - 1) * tt) 
        res += sum(i * tt for i in range(total - nn, total))
    return res
            

def p2_brute_force(disk_map):
    s, cur = [], 0
    blocks = {}
    for i, c in enumerate(disk_map):
        if i % 2 == 0:
            s.append((cur, int(c)))
            # we can dispose of blocks
            # if we traverse from back
            # to end
            blocks[cur] = int(c) 
            cur += 1
        else:
            s.append((None, int(c)))

    for last in range(cur - 1, -1, -1):
        #print(f"{last}: starting loop s is now {s}")
        si, ti = get_space_target_index(s, blocks[last], last)
        #print(f"{s[ti]} fit into index={si}")
        if si is None:
            continue
        tt, tc = s[ti]
        st, sc = s[si]
        s[ti] = (None, tc)
        if sc == tc:
            s[si] = (last, sc)
        else:
            s[si] = (None, sc - tc)
            s.insert(si, (last, tc))
        #print(f"{last} ending loop s is now {s}")
        #print(f"{format(s)}")
    return block_checksum(s)

print(p1_brute_force(disk_map))
print(p2_brute_force(disk_map))
