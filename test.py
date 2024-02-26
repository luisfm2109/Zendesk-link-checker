def sort_upper(x):
    return x.isupper() if not x.isnumeric() else 1

def sort_numeric(x):
    return x.isnumeric()

def sort_odd(x):
    return x%2

S = [*input()]
S.sort()
S.sort(key=sort_upper)
S.sort(key=sort_numeric)
S.sort(key= lambda x: int(x)%2==0 if x.isnumeric() else 0)
S = ''.join(S)

print(S)