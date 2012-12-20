import httplib
import random
import time
import threading

HOST = "damp-refuge-4312.herokuapp.com"
PORT = 80
STEPS = 20
INSTANCES = 2

results = []
class CalculationRequest(threading.Thread):
	lock = threading.Lock()

	def __init__(self, x, prefix):
		threading.Thread.__init__(self)
		self.x = x
		self.prefix = prefix

	def run(self):
		con = httplib.HTTPConnection(host=HOST, port=PORT)
		path = '%s%d' % (self.prefix, self.x)
		con.request('GET', path)
		resp = con.getresponse()
		CalculationRequest.lock.acquire()
		results.append(resp.read())
		CalculationRequest.lock.release()
		if not resp.status in range(200,299):
			raise Exception(resp.status)

def clear_cache():
	con = httplib.HTTPConnection(host=HOST, port=PORT)
	con.request('GET','/clear')
	con.getresponse()

def test_method(prefix):
	global results
	clear_cache()
	print "cache cleared"
	start = time.time()
	for i in range(0, STEPS):
		threads = []
		for j in range(0, INSTANCES):
			rand = random.choice(range(10,20))
			t = CalculationRequest(rand, prefix)
			threads.append(t)
			t.start()
		for thread in threads:
			thread.join()
	print "Total time (prefix: %s): %f" % (prefix, time.time() - start)
	print "These are %d results." % len(results)
	results = []

def main():
	for prefix in ("/diligent/", "/negative/"):
		print prefix
		test_method(prefix)

if __name__ == "__main__":
	try:
		main()
	except Exception as e:
		print "error: status code {0}!".format(e)

