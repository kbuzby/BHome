import os
import subprocess

ARPFILE="tmp"
Hosts=dict()
devnull=open(os.devnull, 'w')

class Host:
    def __init__(self, MAC, IP, track):
        self.MAC = MAC
        self.track = track
        if track=="yes":
            self.IP = IP
            self.Actions=set()
            self.status="dead"

    def addAction(self, action):
        if action not in self.Actions:
            self.Actions.add(action)
            return True
        else
            return False

    def updateStatus(self, stat):
        if stat=="alive":
            self.status = "alive"
        elif stat="dead"
            confirmed = False
            for i in range(1,3):
                if not hostAlive(self.IP):
                    break
                if i==3:
                    confirmed = True
            if confirmed:
                self.status = "dead"
                 

def yn(ans):
    if ans.lower() in ("yes","y","no","n"):
        if ans.lower() in ("yes","y"):
            return "yes"
        elif ans.lower() in ("no","n"):
            return "no"
    else:
        return False

def addKnown(MAC, IP):
    done = False
    while not done:
        ans=raw_input("Would you like to track "+MAC+" to known devices (yes/no)?")
        ans=yn(ans)
        if ans in ("yes","no"):
            Hosts[MAC] = Host(MAC, IP, ans)
            done = True
        else:    
            print "Please enter only yes or no"

def scanARP():
    os.system("arp | awk -v OFS='\t' '{print $1, $3}' > "+ARPFILE)

def checkARPhosts():
    with open(ARPFILE) as fileOBj:
        for line in fileObj.readlines():
            line=line.split()
            ip=line[0]
            MAC=line[1]
            if MAC not in Hosts:
                addKnown(MAC, ip)
            elif Hosts[MAC].track=="yes":
                if hostAlive(ip):
                    print MAC+" is alive"
                else:
                    print MAC+"is dead"

def hostAlive(IP):
    resp=subprocess.call(['ping','-c1','-i0.2',IP],stdout=devnull,stderr=devnull)
    if resp==0:
        return True
    else: 
        return False

def main():
    while 1:
        scanARP()
        checkARPhosts()

main()
