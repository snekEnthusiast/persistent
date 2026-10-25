import persistent
persistent.init(globals())
persistent.declare(x=0)
x+=2
print(x)