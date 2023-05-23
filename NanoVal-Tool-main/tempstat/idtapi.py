from base64 import b64encode
import json
from urllib import parse, request
import requests
import time, datetime
from pathlib import Path

class IDTOligoAnalyzer:
    def __init__(self):
        self.creds_path = Path(__file__).parent / "Data/idt_api_credentials.json"
        self.id, self.secret, self.username, self.password = self.initialize()
        self.url = "https://www.idtdna.com/Restapi/v1/OligoAnalyzer/Analyze"
        self.access_token = self.find_access_token_cache()

    def initialize(self) -> list:
        with open(self.creds_path, 'r') as credentials:
            credentials = json.loads(credentials.read())
        _id = credentials['client_id']
        _secret = credentials['client_secret']
        _username = credentials['idt_username']
        _password = credentials['idt_password']

        return _id, _secret, _username, _password

    def get_access_token(self) -> dict:
        """
        **Taken from IDT**
        Create the HTTP request, transmit it, and then parse the response for the 
        access token.
        
        The body_dict will also contain the fields "expires_in" that provides the 
        time window the token is valid for (in seconds) and "token_type".
        """
        client_id = self.id
        client_secret = self.secret
        idt_username = self.username
        idt_password = self.password
        # Construct the HTTP request
        authorization_string = b64encode(bytes(client_id + ":" + client_secret, "utf-8")).decode()
        request_headers = { "Content-Type" : "application/x-www-form-urlencoded",
                            "Authorization" : "Basic " + authorization_string }
                        
        data_dict = {   "grant_type" : "password",
                        "scope" : "test",
                        "username" : idt_username,
                        "password" : idt_password }
        request_data = parse.urlencode(data_dict).encode()

        post_request = request.Request("https://www.idtdna.com/Identityserver/connect/token", 
                                        data = request_data, 
                                        headers = request_headers,
                                        method = "POST")

        # Transmit the HTTP request and get HTTP response
        response = request.urlopen(post_request)

        # Process the HTTP response for the desired data
        body = response.read().decode()
        
        # Error and return the response from the endpoint if there was a problem
        if (response.status != 200):
            raise RuntimeError(f"Request failed with error code: {response.status} \nBody:\n {body}")
            #raise RuntimeError("Request failed with error code:" + response.status + "\nBody:\n" + body)
        
        body_dict = json.loads(body)
        return body_dict

    def post_analyzer_request(self, sequence:str, Na:int, Mg:int, olig_conc:int, dNTP:int) -> dict:
        token = self.access_token
        payload = json.dumps({
            "Sequence": sequence,
            "NaConc": Na,
            "MgConc": Mg,
            "DNTPsConc": dNTP,
            "OligoConc": olig_conc,
            "NucleotideType": "DNA"
        })
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {token}',
            'Cookie': 'ARRWestffinity=ba40cc5de3760d56c7d5bda31309fd0f34ac4ddd6a11aaa1f1aa3943af5c5db2'
        }

        response = requests.request("POST", self.url, headers=headers, data=payload)
        # print(response.text)
        output = json.loads(response.text)

        return output

    def find_access_token_cache(self) -> str:
        idt_api_creds_path = Path(__file__).parent / "Data/idt_api_credentials.json"
        with open(idt_api_creds_path) as creds_file:
            creds_file_dict = json.loads(creds_file.read())
        try:
            # If access_token is not expired
            if creds_file_dict['expires_in'] + creds_file_dict['timestamp'] < time.time():
                api_dict = self.get_access_token()
                access_token = api_dict['access_token']
                expiration_time = api_dict['expires_in']
                creds_file_dict['access_token'] = access_token
                creds_file_dict['expires_in'] = expiration_time
                creds_file_dict['timestamp'] = time.time()
                creds_file_dict['datestamp'] = datetime.datetime.fromtimestamp(creds_file_dict['timestamp']).strftime('%c')
                creds_file_dict['date_expire'] = datetime.datetime.fromtimestamp((creds_file_dict['expires_in'] + creds_file_dict['timestamp'])).strftime('%c')

                with open(idt_api_creds_path, "w") as cache_write:
                    cache_write.write(json.dumps(creds_file_dict, indent=4))
            
                return access_token

            else:
                access_token = creds_file_dict['access_token']

                return access_token
        
        except:
            api_dict = self.get_access_token()
            access_token = api_dict['access_token']
            expiration_time = api_dict['expires_in']
            creds_file_dict['access_token'] = access_token
            creds_file_dict['expires_in'] = expiration_time
            creds_file_dict['timestamp'] = time.time()
            with open(idt_api_creds_path, "w") as cache_write:
                cache_write.write(json.dumps(creds_file_dict, indent=4))

            return access_token

if __name__ == "__main__":
    idt_api = IDTOligoAnalyzer()
    idt_api.post_analyzer_request("ATAAAGATCGATCGATCGATCGATCGATCAAAAA", 50, 12, 0.25, 0)