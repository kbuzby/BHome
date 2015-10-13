import os
import subprocess

monitor=dict()

def yn(ans):
    if ans.lower() in ("yes","y","no","n"):
        if ans.lower() in ("yes","y"):
            return "yes"
        elif ans.lower() in ("no","n"):
            return "no"
    else:
        return False

def addKnown(MAC):
    done1 = False
    while not done1:
        ans=raw_input("Would you like to add "+MAC+" to known devices (yes/no)?")
        ans=yn(ans)
        if ans in ("yes","no"):
            if ans=="yes":
                done2=False
                while not done2:
                    ans=raw_input("Would you like to monitor this device (yes/no)?")
                    ans=yn(ans)
                    if ans in ("yes","no"):
                        if ans=="yes":
                            monitor[MAC]="yes"
                        elif ans=="no":
                            monitor[MAC]="no"
                        done1=True
                        done2=True
                    else:
                        print "Please enter only yes or no"
            if ans=="no":
                done1=True
        else:    
            print "Please enter only yes or no"


devnull = open(os.devnull, 'w')
while 1:
    os.system("arp | awk -v OFS='\t' '{print $1, $3}' > tmp")
    with open("tmp") as fileObj:
        for line in fileObj.readlines():
            line=line.split()
            ip=line[0]
            MAC=line[1]
            if MAC not in monitor:
                addKnown(MAC)
            elif monitor[MAC]=="yes":
                resp=subprocess.call(['ping','-c 1','-i 0.2',ip],stdout=devnull,stderr=devnull)
                if resp==0:
                    print MAC+" is alive"
                else:
                    print MAC+" is dead"
