import re

def translation(match):
    res = []
    numbers = match.group(2).split(",")
    for i,x in enumerate(match.group(1)):
        res += ["data-%s=%s" % (x,numbers[i])]

    return ' '.join(res)


def rotation(match):
    res = []
    numbers = match.group(2).split(",")
    for i,x in enumerate(match.group(1)[1:] if match.group(1) else ['z']):
        res += ["data-rotate-%s=%s" % (x,numbers[i])]

    return ' '.join(res)


TRANSLATION_TABLE=(
    (r'(?:^|(?<= ))([xyz]{1,3})=\(?((?:.*?,){0,2}(?:.*?))\)?(?:$|(?= ))', translation,),
    (r'(?:^|(?<= ))rot((?:-[xyz]{1,3})?)=\(?((?:.*?,){0,2}(?:.*?))\)?(?:$|(?= ))', rotation),
    (r'(?:^| )zoom=(.*?)(?:$| )', lambda m: "data-scale=%s" % m.group(1)),
)
