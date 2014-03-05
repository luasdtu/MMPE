import time
no_trials = 10
def repeat(func, *args, **kwargs):
    for i in range(no_trials):
        try:
            func(*args, **kwargs)
            return
        except Exception as e:
            print ("%d/%d: %s. Trying again in 1 second" % (i + 1, no_trials, str(e)))
            time.sleep(1)
    print "Giving up. %s" % str(e)
    raise
