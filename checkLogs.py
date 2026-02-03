import os
import csv
from collections import defaultdict

print("script started")
logDir = "logs"
validIPStart = 121
validIPEnd = 100

rogueIPusers = set()
userDayCount = defaultdict(int)

def isValidIP(ip):

    parts = ip.split(".")

    if len(parts)!=3:
        return False
    
    if int(parts[0])!=10:
        return False
    
    if int(parts[1])>1 or int(parts[1])<0:
        return False
    
    if int(parts[2])>121 or int(parts[2])<100:
        return False
    
    return True


for file in os.listdir(logDir):

    if not file.endswith(".log"):
        continue

    filePath = os.path.join(logDir,file)

    with open(filePath,"r") as f:
        for line in f:
            line = line.strip()

            if not line:
                continue

            parts = line.split("-")

            day=parts[0]
            month=parts[1]
            year=parts[2]

            date=f"{day}-{month}-{year}"

            username=parts[7]
            ip=parts[-1]

            if not isValidIP(ip):
                rogueIPusers.add(username)
            
            key = (username,date)
            userDayCount[key] += 1

susUsers=set()

for (user,date),count in userDayCount.items():

    if count>5:
        susUsers.add(user)

with open("Report.csv","w",newline="") as file:

    writer = csv.writer(file)

    writer.writerow(["username","roguereason"])

    for user in rogueIPusers:
        writer.writerow([user,"RogueIPAccess"])

    for user in susUsers:
        writer.writerow([user,"SuspiciousAttempt"])

print("csv file generated.")