import os

from src.password import PasswordData


# @dataclass
# class PasswordData:
#    label: str
#    url: str
#    com: str
#    user: str
#    passwd: str


with open('test/test.txt', 'r') as file:
    lines = file.read().splitlines()

for l in lines:
    content = [x.strip() for x in l.split('=')]

    try:
        buffer = PasswordData
        setattr(buffer, content[0], content[1])

    except:
        print('format pas good')
