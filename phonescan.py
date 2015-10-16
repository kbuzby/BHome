import os 
import subprocess
import csv

SAVEFILE="hosts"
ARPFILE="tmp" 
Hosts=dict() 
devnull=open(os.devnull, 'w')

class Host:
    def __init__(self, MAC, IP, track):
        self.MAC = MAC
        self.track = track
        self.IP = IP
        if track=="yes":
            self.Actions=set()
            self.status="dead"

    def addAction(self, action):
        if action not in self.Actions:
            self.Actions.add(action)
            return True
        else:
            return False

    def updateStatus(self, stat):
        if stat=="alive":
            self.status = "alive"
        elif stat=="dead":
            self.status = "dead"
            #confirmed = False
            #for i in range(1,3):
            #    if not hostAlive(self.IP):
            #        break
            #    if i==2:
            #        confirmed = True
            #if confirmed:
            #    self.status = "dead"
                 

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
    with open(ARPFILE) as fileObj:
        for line in fileObj.readlines():
            line=line.split()
            ip=line[0]
            MAC=line[1]
            if MAC not in Hosts:
                addKnown(MAC, ip)
            elif Hosts[MAC].track=="yes":
                if hostAlive(ip):
                    Hosts[MAC].updateStatus("alive")
                else:
                    Hosts[MAC].updateStatus("dead")
                if Hosts[MAC].status=="alive":
                    print MAC+" is alive"
                elif Hosts[MAC].status=="dead":
                    print MAC+" is dead"
    fileObj.close()

def hostAlive(IP):
    resp=subprocess.call(['ping','-c1','-i0.2',IP],stdout=devnull,stderr=devnull)
    if resp==0:
        return True
    else: 
        return False

def saveHosts():
    f = csv.writer(open(SAVEFILE, 'w'))
    for key in Hosts:
        f.writerow([Hosts[key].MAC, Hosts[key].IP, Hosts[key].track])

def loadHosts():
    try:
        for MAC,IP,track in csv.reader(open(SAVEFILE)):
            Hosts[MAC] = Host(MAC, IP, track)
        return 1
    except:
        return 0

def main():
    if not loadHosts():
        print "host file not loaded"        
    while 1:
        try:
            scanARP()
            checkARPhosts()
        except (KeyboardInterrupt, SystemExit):
            saveHosts()
            devnull.close()
            break

main()
