# 아래 사이트에서 random password 를 생성한다.
# 그리고, api_key.txt 에 작성한다.
# https://www.atatus.com/tools/password-generator

api_keys = []

with open("db/api_key.txt", "r") as f:
    for line in f.readlines():
        line = line.replace("\n", "")
        if line != '':
            api_keys.append(line)