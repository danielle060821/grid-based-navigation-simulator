import torch.nn as nn

class Policy(nn.Module):
    def __init__(self):
        super().__init__()
        #Sequential: make the list recognizable by pyTorch
        #Put the 6D input to 32 equations and finalize all outputs to four scores(up down left right)
        #ReLu: introduces non-linearality
        """
        number of weights: 6 * 32 + 32 * 32 + 32 * 5
        number of bias: 32 + 32 + 5
        """
        self.net = nn.Sequential(
            nn.Linear(6, 32),
            nn.ReLU(),
            nn.Linear(32, 32),
            nn.ReLU(),
            nn.Linear(32, 5)
        )
        
    #get output(4 scores)
    def forward(self, x):
        return self.net(x)