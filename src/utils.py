def read_address(file):
    with open(file) as f:
        addresses = f.readlines()
        f.close()
    address_list = []
    for address in addresses:
        address_list.append(address.strip("\n"))
    return address_list

def wei2eth(value):
    return value / 1e18