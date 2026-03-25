import json
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from policy import Policy

"""
store data as 
    X = [obs1, obs2, ...]
    Y = [action1, action2, ...]
"""
X = []
Y = []
with open("BC/dataset.jsonl","r") as f:
    for line in f:
        data = json.loads(line)
        
        obs = data["obs"]
        action = data["action"]
        X.append(obs)
        Y.append(action)
#numpy: for organizting data into consistent structure, also makes debugging easier(can get size)
#X needs to be used for calculation, so float is more accurate
X = np.array(X, dtype = np.float32)
#Y is "answer index", so int
Y = np.array(Y, dtype = np.int64)

#convert data to tensor
X_tensor = torch.tensor(X, dtype = torch.float32)
Y_tensor = torch.tensor(Y, dtype = torch.int64)

model = Policy()
optimizer = optim.Adam(model.parameters(), lr = 1e-3)
criterion = nn.CrossEntropyLoss()

#train 500 times
for epoch in range(500):
    #initialize optimizer
    optimizer.zero_grad()
    
    #raw scores(tensor)
    logits = model(X_tensor)
    
    """
    CrossEntropyLoss:
        (1)turn logits to probability
        (2)take the probability of the right answer(Y_tensor)(p)
        (3)loss = -log(p)
    """
    loss = criterion(logits, Y_tensor)   
    
    """
    Calculate gradient:
        gradientw = d(loss)/dw
        gradientb = d(loss)/db
    """
    loss.backward()
    
    """
    Update weights and bias(parameters):
            new weight = old weight - gradientw * learning rate       
            new bias = old bias - gradientb * learning rate
    """
    optimizer.step()
    
    #print output every 50 epochs
    if epoch % 50 == 0:
        #.item(): transform tensor to float
        print(f"epoch{epoch}, loss{loss.item():.4f}")
        
#save model trained
torch.save(model.state_dict(), "BC/model.pth")
    
#test accuracy
with torch.no_grad():
    #take index with max score
    pred = torch.argmax(model(X_tensor), dim = 1)
    acc = (pred == Y_tensor).float().mean()
    print("accuracy: ", acc.item())
    
        
    
    
        

