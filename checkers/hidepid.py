import logging
import psutil
import helpers

CHECKER_NAME = "HIDEPID"

logging.basicConfig(format="[%(name)s] %(message)s")
log = logging.getLogger(CHECKER_NAME)


class HidePID:
	def checkHidePID(self):
		for mountpoint in psutil.disk_partitions(all=True):
			if mountpoint.mountpoint == "/proc":
				if "hidepid" not in mountpoint.opts \
				or "hidepid=0" in mountpoint.opts:
					log.error("Set hidepid mount option on /proc.")


def run():
    checker = HidePID()
    
    c = helpers.getCheckers(HidePID, CHECKER_NAME)
    for name in sorted(c):
        getattr(checker, name)()

if __name__ == "__main__":
    run()