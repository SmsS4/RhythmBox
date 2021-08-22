# import json
# import statistics
# data = {}
# with open('data.json') as json_file:
#     data = json.load(json_file)
# #
# for i in data:
#      print(i)
# # #     print(data[i])
# # #     print("***")
# variences = []
#
# for i in range(20):
#     a = []
#     for j in data:
#         a.append(data[j][i])
#     variences.append(statistics.stdev(a))
# print(variences)
# def distance(i, j):
#     n = len(data[i])
#     ans = 0
#     for t in range(n):
#         ans += abs(data[i][t] - data[j][t]) / (t + 1)
#     return ans
#
# def get_close_songs(list_addr, num):
#     dis = []
#     for i in data:
#         if i in list_addr:
#             continue
#         mn = 1e9
#         for j in list_addr:
#             mn = min(mn, distance(i, j))
#         dis.append((mn, i))
#     dis.sort()
#     ans = []
#     for i in range(num):
#         ans.append(dis[i])
#     return ans
# x1 = '/Users/sasa/Desktop/all_mus/pop/11 Someone Like You.mp3'
# x2 = '/Users/sasa/Desktop/all_mus/pop/01 Rolling In The Deep.mp3'
# x3 = "/Users/sasa/Desktop/all_mus/pop/06 He Won't Go.mp3"
# x4 = '/Users/sasa/Desktop/all_mus/pop/05 Set Fire To The Rain.mp3'
# x5 = '/Users/sasa/Desktop/all_mus/classical/Ludwig van Beethoven Daniel Barenboim - Piano Sonata No23 In.mp3'
# x6 = '/Users/sasa/Desktop/all_mus/pop/Sia – Soon We’ll Be Found.mp3'
# x7 = '/Users/sasa/Desktop/all_mus/rock/Nothing Else Matters.mp3'
# list_addrs = [x7]
# print(get_close_songs(list_addrs, 10))
# import requests
# req = """
# curl https://api.mainnet-beta.solana.com -X POST -H "Content-Type: application/json" -d '
#   {"jsonrpc":"2.0", "id":1, "method":"getBalance", "params":["83astBRguLMdt2h5U1Tpdq5tjFoJ6noeGwaY3mDLVcri"]}
# '
# """

#r = requests.post(req)
#print(r)

import solana
from solana.rpc.api import Client
str = "http://192.168.1.88:8899"
str2 = "https://api.devnet.solana.com"
str3 = "https://api.mainnet-beta.solana.com"
solana_client = Client(str3)


x = solana_client.get_balance("7eaa3nUWNC2UwE539Wc7h4cH1LC7dTkhiFKfy9BXo38g")
print(x)
print(x['result']['value'])

8988016840