import sys
import time
from daemon import Daemon
from phonescan import HostManager

def main(hostMgr):
	while 1:
		try:
			hostMgr.scanARP()
			hostMgr.checkARPhosts()
		except (KeyboardInterrupt, SystemExit):
			hostMgr.saveHosts()
			break

class BHomeDaemon(Daemon):
	def run(self):
		hostMgr = HostManager()
		while True:
			main(hostMgr)
			time.sleep(5)

if __name__ == "__main__":
	daemon = BHomeDaemon('/var/run/BHome/BHome.pid')
	if len(sys.argv) == 2:
		if sys.argv[1] == 'start':
			daemon.start()
		elif sys.argv[1] == 'stop':
			daemon.stop()
		elif sys.argv[1] == 'restart':
			daemon.restart()
		elif sys.argv[1] == 'manual':
			hostMgr = HostManager()
			main(hostMgr)
		else:
			print "Unknown command"
			sys.exit(2)
		sys.exit(0)
	else:
		print "usage: %s start|stop|restart" % sys.argv[0]
		sys.exit(2)
