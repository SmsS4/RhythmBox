import json
data = {}
with open('data.json') as json_file:
    data = json.load(json_file)
#
# for i in data:
#      print(i)
# #     print(data[i])
# #     print("***")
def distance(i, j):
    n = len(data[i])
    ans = 0
    for t in range(n):
        ans += abs(data[i][t] - data[j][t])
    return ans

def get_close_songs(list_addr, num):
    dis = []
    for i in data:
        if i in list_addr:
            continue
        mn = 1e9
        for j in list_addr:
            mn = min(mn, distance(i, j))
        dis.append((mn, i))
    dis.sort()
    ans = []
    for i in range(num):
        ans.append(dis[i][1])
    return ans
x1 = '/Users/sasa/Desktop/all_mus/pop/11 Someone Like You.mp3'
x2 = '/Users/sasa/Desktop/all_mus/pop/01 Rolling In The Deep.mp3'
x3 = "/Users/sasa/Desktop/all_mus/pop/06 He Won't Go.mp3"
x4 = '/Users/sasa/Desktop/all_mus/pop/05 Set Fire To The Rain.mp3'
x5 = '/Users/sasa/Desktop/all_mus/classical/Ludwig van Beethoven Daniel Barenboim - Piano Sonata No23 In.mp3'
list_addrs = [x5]
print(get_close_songs(list_addrs, 1))
