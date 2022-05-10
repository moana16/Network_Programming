from sys import stdin

def set_bit (x):
    return bin (x).count ("1")

def solve (l, r, k):
    sbl = set_bit (l)
    if 2 ** k - 1 > r: return -1
    if sbl == k: return l
    lbit = l.bit_length ()
    if k > sbl:
        df = k - sbl
        if lbit > k:
            for i in range (65):
                i2 = 2 ** i
                if not (i2 & l):
                    df -= 1
                    l += i2
                if not df: return l if l <= r else -1
        else:
            return 2 ** k - 1
    else:
        df = sbl - k + 1
        abc = 0  # additional bit count
        for i in range (65):
            i2 = 2 ** i
            if not df and not (i2 & l):
                l += i2 + 2 ** abc - 1
                #print ("k < sbl", i, bin (l))
                return l if l <= r else -1
            if i2 & l:
                l -= i2
                if df: df -= 1
                else: abc += 1
    
    while 2 ** lbit - 1 <= l:
        lbit += 1



def main ():
    read = stdin.readline
    t = int (read ())
    for t_ in range (t):
        l, r, k = map (int, read ().split ())
        print (solve (l, r, k))

if __name__ == "__main__": main ()