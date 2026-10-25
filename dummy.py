import persistent
persistent.init(globals())
persistent.declare(x=0)
x+=1
print(x)