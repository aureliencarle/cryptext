import os

from cryptext.password import PasswordData, PasswordDataIO

# @dataclass
# class PasswordData:
#    label: str
#    url: str
#    com: str
#    user: str
#    passwd: str


with open('test/test.txt', 'r') as file:
    lines = file.read().splitlines()

content = [{}]

for l in lines:
    c = [x.strip() for x in l.split('=')]

    if len(c) == 1:
        content.append({})
    else:
        content[-1][c[0]] = c[1]


pass_list = [PasswordData(**kwargs) for kwargs in content]

imp_session = 'test_du_plug_in'
imp_pass = pass_list
