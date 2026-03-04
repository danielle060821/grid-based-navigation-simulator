import json
"""
Record player trajectory for behaviour cloning training
"""
class TrajectoryRecorder:
    def __init__(self, path):
        self.file = open(path, "a")
    
    def record(self, obs, action):
        self.file.write(json.dumps({
            #convert numpy array to list because json does not recognize numpy array
            "obs": obs.tolist(),
            "action": int(action)
        }) + "\n")
        
    #clear previous data
    def reset(self, path):
        open(path, "w").close()
        
    def close(self):
        self.file.close()
        