#!/usr/bin/python3
import re
import operator
import csv

per_user = {}
err_count = {}

with open("syslog.log") as f:
    lines = [x.strip() for x in f.readlines()]

    for line in lines:
        error_found = re.search(r"ticky: ERROR ([\w ']*) ", line)

        if error_found != None:
            temp = err_count.get(error_found[1], 0)
            temp += 1
            err_count[error_found[1]] = temp
            username = re.search(r" \(([\w.]*)\)$", line)
            x = list(per_user.get(username[1], (0, 0)))
            x[1] += 1
            per_user[username[1]] = tuple(x)
        
        else:
            username = re.search(r" \(([\w.]*)\)$", line)
            x = list(per_user.get(username[1], (0, 0)))
            x[0] += 1
            per_user[username[1]] = tuple(x)
    
    per_user = sorted(per_user.items(), key = operator.itemgetter(0))
    err_count = sorted(err_count.items(), key = operator.itemgetter(1), reverse = True)

    per_user_labels = {"Username" : ("INFO", "ERROR")}
    per_user_labels.update(per_user)

    err_count_labels = {"Error" : "Count"}
    err_count_labels.update(err_count)

with open("error_message.csv", "w") as f:
    writer = csv.writer(f)
    for key, value in err_count_labels.items():
        writer.writerow([key, value])

with open("user_statistics.csv", "w") as f:
    writer = csv.writer(f)
    for key, value in per_user_labels.items():
        value = list(value)
        writer.writerow([key, value[0], value[1]])
