import os
import subprocess
import csv
import pynma

myMAC="fc:db:b3:f9:0d:2f"
NMAapi="481390ced1969e7e3514c1ec369197c78bd1d5cc427f73be"

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

class HostManager:

	def __init__(self, startIP="192.168.1.100", endIP="192.168.1.199", saveFile="hosts", arpFile="tmp"):
		prefix = "/home/kyle/dev/hauto/"
		self.Hosts = dict()
		self._saveFile = prefix+saveFile
		self._arpFile = prefix+arpFile
		self._startIP = startIP
		self._endIP = endIP
		self._loadHosts()

	def addKnown(self, MAC, IP):
		done = False
		while not done:
			ans=raw_input("Would you like to track "+MAC+" to known devices (yes/no)?")
			ans=yn(ans)
			if ans in ("yes","no"):
				self.Hosts[MAC] = Host(MAC, IP, ans)
				done = True
			else:
				print "Please enter only yes or no"

	def checkARPhosts(self):
		with open(self._arpFile) as fileObj:
			for line in fileObj.readlines():
				line=line.split()
				ip=line[0]
				MAC=line[1]
				if MAC not in self.Hosts.keys():
					self.addKnown(MAC, ip)
				elif self.Hosts[MAC].track=="yes":
					if self.hostAlive(self.Hosts[MAC]):
						if self.Hosts[MAC].status=="dead":
							if MAC==myMAC:
								notifier = pynma.PyNMA(NMAapi)
								notifyKyle(notifier)
								del notifier
							self.Hosts[MAC].updateStatus("alive")
					else:
						self.Hosts[MAC].updateStatus("dead")
					if self.Hosts[MAC].status=="alive":
						print MAC+" is alive"
					elif self.Hosts[MAC].status=="dead":
						print MAC+" is dead"
		fileObj.close()

	def scanARP(self):
		devnull=open(os.devnull, 'w')
		if subprocess.call(['fping','-c 1','-q','-g '+self._startIP+' '+ self._endIP],stdout=devnull,stderr=devnull) in (0, 1):
			os.system("arp -n | awk -v OFS='\t' '{if(NR>1)print $1, $3}' | grep -vw 'eth0' > " + self._arpFile)
		devnull.close()

	def hostAlive(self,host):
		devnull=open(os.devnull, 'w')
		resp=subprocess.call(['fping','-c 1',host.IP],stdout=devnull,stderr=devnull)
		devnull.close()
		if resp==0:
			return True
		else:
			return False

	def saveHosts(self):
		f = csv.writer(open(self._saveFile, 'w'))
		for key in self.Hosts:
			f.writerow([self.Hosts[key].MAC, self.Hosts[key].IP, self.Hosts[key].track])

	def _loadHosts(self):
		try:
			for MAC,IP,track in csv.reader(open(self._saveFile)):
				self.Hosts[MAC] = Host(MAC, IP, track)
		except:
			return

def notifyKyle(notifier):
	notifier.push("PhoneScan","Connected to WiFi","Description","http://www.google.com")
