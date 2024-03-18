import json
import sys

res = {}
with open(sys.argv[1], "r") as f:
    for line in f:
        tokens = " ".join(line.split()).split(" ")
        name = tokens[0]
        snr = float(tokens[6])
        tokens = name.split(".")
        chan = f"{tokens[4]}.{tokens[5]}"
        # print(f"{name} / {chan}: {snr}")
        if not chan in res:
            res[chan] = {
                "count": 1,
                "snr": snr,
            }
        else:
            res[chan]["snr"] += snr
            res[chan]["count"] += 1

# print(json.dumps(res, indent=2))

for k, v in res.items():
    avg = v["snr"] / v["count"]
    print(f"{k}, {avg}")
