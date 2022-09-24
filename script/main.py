import sys
sys.path.append("../")
import time

from config.config import Config
from src.utils import read_address
from src.address_watching import ChaseBot

if __name__ == "__main__":
    agent = ChaseBot()
    file_name = Config.file_path
    address_list = read_address(file_name)

    while True:
        print("chasing nft wallet....")
        for address in address_list:
            print("address = {}".format(address))
            try:
                agent.get_nft_data_by_address(address)
            except:
                print("something wrong happened")
            time.sleep(2)
        print("sleeping....")
        time.sleep(Config.sleep_time)
