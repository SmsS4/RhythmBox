import json
import os

import librosa

dir = "/home/smss/Downloads/all_mus"  # pylint:disable=redefined-builtin
track = []
for root, dirs, files in os.walk(dir):
    for file in files:
        if file.endswith(".mp3"):
            x = os.path.join(root, file)
            track.append(x)

# for i in range(5):
#     print(track[i])
n = len(track)
means = {}
for id in range(n):  # pylint:disable=redefined-builtin
    print(id, "out of", n)
    x, sr = librosa.load(track[id])
    mfcc = librosa.feature.mfcc(x, sr=sr)

    row_means = mfcc.mean(axis=1)
    print(row_means.shape)
    # print(row_means)
    means[track[id]] = row_means.tolist()

with open("data.json", "w") as fp:
    json.dump(means, fp)
