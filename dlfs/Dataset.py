# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/01_data.ipynb.

# %% auto 0
__all__ = ['Dataset', 'get_dataset']

# %% ../nbs/01_data.ipynb 1
import fastcore.all as fc

# %% ../nbs/01_data.ipynb 4
class Dataset:
    def __init__(self, x, y): fc.store_attr()
        
    def __len__(self): return len(self.x)
    
    def __getitem__(self,i): return self.x[i], self.y[i]

# %% ../nbs/01_data.ipynb 5
def get_dataset():
    training_data = datasets.FashionMNIST(root="data",train=True,download=True,transform=ToTensor())
    return Dataset(training_data.data, training_data.targets)
