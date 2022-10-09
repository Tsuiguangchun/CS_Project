# encoding:utf-8
# @CreateTime: 2022/9/20 23:53
# @Author: Xuguangchun
# @FlieName: web3_connect.py
# @SoftWare: PyCharm

import json
from web3 import Web3

"""
cmd下开启本地节点：
 geth --datadir data --syncmode fast --networkid 666 --http --http.corsdomain="*" --http.port 8545 --http.addr "0.0.0.0" --http.api db,web3,eth,debug,personal,net,miner,admin --allow-insecure-unlock --rpc.allow-unprotected-txs  --port 30303  2>./console.log

 geth --datadir data --networkid 666 --http --http.corsdomain="*" --http.port 8545 --http.addr "0.0.0.0" --http.api db,web3,eth,debug,personal,net,miner,admin --allow-insecure-unlock --rpc.allow-unprotected-txs  --port 30303  2>./console.log
geth --datadir data --syncmode fast --rpcapi eth,web3,personal --rpc --cache=2048  console 2>>test.log
"""

"""
with open(file='D:\cs_project\data\BNB_Abi', mode='r', encoding='utf-8') as f:
    BNB_ABI = json.loads(f.read())
    print(BNB_ABI)
BNB_contract = Web3.toChecksumAddress('0xB8c77482e45F1F44dE1745F52C74426C631bDD52')
w3 = Web3(Web3.HTTPProvider("http://localhost:8545"))


if w3.eth.getBlock(0) is None:
    print("failure")
elif w3.isConnected():
    print("successfully")
    print(w3.eth.accounts)
    token_contract = w3.eth.contract(BNB_contract, abi=BNB_ABI)
    print(token_contract)
    print(token_contract)

    ACC = '0xAdA556CcC02cc968579FF5294D52DC0eBf5eE328'  # 个人钱包地址我随便找的
    balance = token_contract.functions.balanceOf(ACC).call()  # 查询个人钱包地址的余额
    print(balance)
    # name = token_contract.functions.name().call()
    # totalSupply = token_contract.functions.totalSupply().call()
    # print(name)
    # print(totalSupply)
# print(web3.fromWei(token_contract.functions('totalSupply'),'ether'))
"""
from web3 import Web3


w3 = Web3(Web3.HTTPProvider("https://cloudflare-eth.com"))
sand_token_addr = '0x3845badAde8e6dFF049820680d1F14bD3903a5d0'
dai_token_addr = "0x6B175474E89094C44Da98b954EedeAC495271d0F"     # DAI
weth_token_addr = "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2"    # Wrapped ether (WETH)

acc_address = "0xA478c2975Ab1Ea89e8196811F51A7B7Ade33eB11"        # Uniswap V2: DAI 2
acc_address2 = '0x69786AA4d272872D40233ee49B2DE6DB5b475a50'

# This is a simplified Contract Application Binary Interface (ABI) of an ERC-20 Token Contract.
# It will expose only the methods: balanceOf(address), decimals(), symbol() and totalSupply()
simplified_abi = [
    {
        'inputs': [{'internalType': 'address', 'name': 'account', 'type': 'address'}],
        'name': 'balanceOf',
        'outputs': [{'internalType': 'uint256', 'name': '', 'type': 'uint256'}],
        'stateMutability': 'view', 'type': 'function', 'constant': True
    },
    {
        'inputs': [],
        'name': 'decimals',
        'outputs': [{'internalType': 'uint8', 'name': '', 'type': 'uint8'}],
        'stateMutability': 'view', 'type': 'function', 'constant': True
    },
    {
        'inputs': [],
        'name': 'symbol',
        'outputs': [{'internalType': 'string', 'name': '', 'type': 'string'}],
        'stateMutability': 'view', 'type': 'function', 'constant': True
    },
    {
        'inputs': [],
        'name': 'totalSupply',
        'outputs': [{'internalType': 'uint256', 'name': '', 'type': 'uint256'}],
        'stateMutability': 'view', 'type': 'function', 'constant': True
    }
]

dai_contract = w3.eth.contract(address=w3.toChecksumAddress(sand_token_addr), abi=simplified_abi)
symbol = dai_contract.functions.symbol().call()
decimals = dai_contract.functions.decimals().call()
totalSupply = dai_contract.functions.totalSupply().call() / 10**decimals
addr_balance = dai_contract.functions.balanceOf(acc_address2).call() / 10**decimals

#  DAI
print("===== %s =====" % symbol)
print("Total Supply:", totalSupply)
print("Addr Balance:", addr_balance)

weth_contract = w3.eth.contract(address=w3.toChecksumAddress(weth_token_addr), abi=simplified_abi)
symbol = weth_contract.functions.symbol().call()
decimals = weth_contract.functions.decimals().call()
totalSupply = weth_contract.functions.totalSupply().call() / 10**decimals
addr_balance = weth_contract.functions.balanceOf(acc_address).call() / 10**decimals

#  WETH
print("===== %s =====" % symbol)
print("Total Supply:", totalSupply)
print("Addr Balance:", addr_balance)
