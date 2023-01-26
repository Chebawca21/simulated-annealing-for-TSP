def insert(s, i, j):
    '''
    Insert operation for solution s and indexes i and j.
    '''
    copy = s.copy()
    a = max(i, j)
    b = min(i, j)
    diff = a - b + 1
    copy[b] = s[a]
    for k in range(1, diff):
        copy[b + k] = s[b + k - 1]
    return copy


def swap(s, i, j):
    '''
    Swap operation for solution s and indexes i and j.
    '''
    copy = s.copy()
    copy[i], copy[j] = copy[j], copy[i]
    return copy


def inverse(s, i, j):
    '''
    Inverse operation for solution s and indexes i and j.
    '''
    copy = s.copy()
    a = max(i, j)
    b = min(i, j)
    diff = a - b + 1
    for k in range(diff):
        copy[b + k] = s[a - k]
    return copy
