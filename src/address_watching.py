import sys
sys.path.append("../")
import requests
import collections

from config.config import Config
from src.utils import wei2eth
from web3 import Web3
w3 = Web3(Web3.HTTPProvider(Config.mainnetProvider))

class ChaseBot(object):
    def __init__(self):
        self.eth_api = Config.etherscanApiKey
        self.provider_api = Config.mainnetProvider
        self.info = collections.defaultdict(dict)
        
    def get_nft_data_by_address(self, address):
        action = "tokennfttx"
        module = "account"
        url = "https://api.etherscan.io/api?module={}&action={}&address={}&apikey={}".format(module, action, address, self.eth_api)
        response = requests.get(url).json()
        status = response["status"]
        if status:
            datas = response["result"][-Config.length:]
        else:
            print(response["message"])
            return
        
        latest_block_num = w3.eth.get_block("latest")["number"]
        for data in datas:
            if data["to"].lower() != address.lower():
                continue
            if latest_block_num - int(data["blockNumber"]) < Config.max_block_interval:
                txhash = data["hash"]
                
                self.info[txhash]["address"] = address
                self.info[txhash]["blockNumber"] = data["blockNumber"]
                if "tokenInfo" not in self.info[txhash]:
                    self.info[txhash]["tokenInfo"] = [[data["tokenName"], data["tokenID"]]]
                else:
                    self.info[txhash]["tokenInfo"].append([data["tokenName"], data["tokenID"]])

        # get average value
        tx_hashs = self.info.keys()
        for txhash in tx_hashs:
            url = "https://api.etherscan.io/api?module=account&action=txlistinternal&txhash={}&apikey={}".format(txhash, self.eth_api)
            response = requests.get(url).json()
            if not response["status"]:
                self.info.clear()
                return
            result = response["result"]
            
            if len(result) == 0:
                continue
            for r in result:
                print(r)
            value = 0
            for detail in result:
                value += wei2eth(float(detail["value"]))
            
            value /= 2
            token_num = len(self.info[txhash]["tokenInfo"])
            avg_value = value / token_num

            for idx in range(token_num):
                self.info[txhash]["tokenInfo"][idx].append(avg_value)
        return self.info
    
    def clear(self):
        self.info.clear()

