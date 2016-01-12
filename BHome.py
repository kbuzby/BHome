import sys
import time
from daemon import Daemon


def main:
	#main routine that will looped in daemon process or called just once


class BHomeDaemon(Daemon):
	def run(self):
		while True:
			main()
			time.sleep(1)



if __name__ == "__main__":
	daemon = BHomeDaemon('/var/run/BHome.pid')
	if len(sys.argv) == 2:
		if sys.argv[1] == 'start':
			daemon.start()
		elif sys.argv[1] == 'stop':
			daemon.stop()
		elif sys.argv[1] == 'restart':
			daemon.restart()
		else:
			print "Unknown command"
			sys.exit(2)
		sys.exit(0)
	else:
		print "usage: %s start|stop|restart" % sys.argv[0]
		sys.exit(2)
