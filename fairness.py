
def jainsall(List):
     
    top = (sum(List))**2
    bun = len(List)*sum(x**2 for x in List)

    jfi = top/bun

    return jfi

print(jainsall([7.33,7.18,8.73,8.04]))
