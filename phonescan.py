import os
import subprocess
import csv
import pynma

SAVEFILE="hosts"
ARPFILE="tmp"
Hosts=dict()
devnull=open(os.devnull, 'w')
myMAC="fc:db:b3:f9:0d:2f"
NMAapi="481390ced1969e7e3514c1ec369197c78bd1d5cc427f73be"
#IP Range to search
STARTIP="192.168.1.100"
ENDIP="192.168.1.199"

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
    if self.status!=stat:
      if stat=="alive":
         self.status = "alive"
      elif stat=="dead":
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
      print("Please enter only yes or no")

def scanARP():
  if subprocess.call(['fping','-c 1','-q','-g '+STARTIP+' '+ENDIP],stdout=devnull,stderr=devnull) in (0, 1):
    os.system("arp -n | awk -v OFS='\t' '{if(NR>1)print $1, $3}' | grep -vw 'eth0' > "+ARPFILE)

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
          if Hosts[MAC].status=="dead":
            if MAC==myMAC:
              notifier = pynma.PyNMA(NMAapi)
              notifyKyle(notifier)
              del notifier
            Hosts[MAC].updateStatus("alive")
        else:
          Hosts[MAC].updateStatus("dead")
        if Hosts[MAC].status=="alive":
          print(MAC+" is alive")
        elif Hosts[MAC].status=="dead":
          print(MAC+" is dead")
  fileObj.close()

def hostAlive(IP):
  resp=subprocess.call(['fping','-c 1',IP],stdout=devnull,stderr=devnull)
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

def notifyKyle(notifier):
    notifier.push("PhoneScan","Connected to WiFi","Description","http://www.google.com")

def main():
  if not loadHosts():
    print("host file not loaded")
  while 1:
    try:
      scanARP()
      checkARPhosts()
    except (KeyboardInterrupt, SystemExit):
      saveHosts()
      devnull.close()
      break

main()
