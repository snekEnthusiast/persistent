import persistent
persistent.init(globals())
persistent.declare(data=None)
# a torn/partial read would make declare() fall back to the default None
if data is None or len(set(data)) != 1 or len(data) != 200_000:  # type: ignore
    print("CORRUPT" if data is not None else "NONE")  # type: ignore
    data = [0] * 200_000
else:
    print("OK")
    data = [data[0] + 1] * 200_000  # type: ignore
