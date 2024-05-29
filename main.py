import requests
import time
import webbrowser
import os

email = input("Email: ")
password = input("Password: ")
bearer = ""

host = "http://api.ifunny.mobi"

def generateBasicAuth():
	
	from secrets import token_hex
	from hashlib import sha1
	from base64 import b64encode
	client_id = "JuiUH&3822"
	client_secret = "HuUIC(ZQ918lkl*7"
	device_id = token_hex(32)
	hashed = sha1(f"{device_id}:{client_id}:{client_secret}".encode('utf-8')).hexdigest()
	basic = b64encode(bytes(f"{f'{device_id}_{client_id}'}:{hashed}", 'utf-8')).decode()
	return basic

basic = generateBasicAuth()

def login():

	paramz = {'grant_type':'password',
		  'username': email,
		  'password': password }
	
	header = {'Host': 'api.ifunny.mobi','Applicationstate': '1','Accept': 'video/mp4, image/jpeg','Content-Type': 'application/x-www-form-urlencoded; charset=utf-8','Authorization': 'Basic '+ basic,'Content-Length':'77','Ifunny-Project-Id': 'iFunny','User-Agent': 'iFunny/8.41.11(24194) iPhone/16.3.1 (Apple; iPhone12,5)','Accept-Language': 'en-US','Accept-Encoding': 'gzip, deflate'}
	userheader = {'Host': 'api.ifunny.mobi','Accept': 'video/mp4, image/jpeg','Applicationstate': '1','Accept-Encoding': 'gzip, deflate','Ifunny-Project-Id': 'iFunny','User-Agent': 'iFunny/8.41.11(24194) iPhone/16.3.1 (Apple; iPhone12,5)','Accept-Language': 'en-US;q=1','Authorization': 'Basic '+ basic,}
	index = 0

	while True:
		
		login = requests.post(host + "/v4/oauth2/token", headers=header, data=paramz).json()
		
		if "error" in login:

			if login["error"] == "captcha_required":
				print("Captcha required, Please solve the captcha, then enter \"Done\" in this terminal: ")
				time.sleep(3)
				captcha_url = login["data"]["captcha_url"]
				webbrowser.open_new(captcha_url)
				input()					
				print("Logging in...")
				continue

			if login["error"] == "unsupported_grant_type":

				time.sleep(10)
				continue

			if login["error"] == "too_many_user_auths":
				raise input("auth rate succeeded, try again later")
			
			if login["error"] == "forbidden":
				index += 1
				if index > 1:
					raise input("Your email or password is incorrect! Please check your credentials and try again.")
				requests.get(host+"/v4/counters", headers=userheader)
				print("Priming one time use basic auth token (10 seconds)...")
				time.sleep(10)
				continue

			if login["error"] == "invalid_grant":
				raise input("Your email or password is incorrect! Please check your credentials and try again.")
				
		break

	bearer = login["access_token"]
	acctheader = {"Host":"api.ifunny.mobi","Accept":"video/mp4, image/jpeg","Applicationstate":"1","Ifunny-Project-Id":"iFunny",'User-Agent': 'iFunny/8.41.11(24194) iPhone/16.3.1 (Apple; iPhone12,5)',"Accept-Language": "en-US;q=1","Authorization":"Bearer " + bearer}
	Account = requests.get(host + "/v4/account", headers = acctheader).json()
	user_id = Account["data"]["id"]
	username = Account["data"]["original_nick"].replace("\n", "\\n")

	print(f"Userdata: {username} [{user_id}]")
	
	print(f"Bearer: {bearer}")

	input("Press enter to dump to a text file. (May not work if you right clicked this file and selected \"Open with python\")")

	fd = os.open("bearer.txt", os.O_RDWR|os.O_CREAT)
	os.write(fd, str.encode(bearer))
	os.close(fd)

	print("Sucessfully dumped. Press enter to exit")
	return

if __name__ == "__main__":
	login()
	input()
	exit()
