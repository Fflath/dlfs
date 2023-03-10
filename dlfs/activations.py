# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/03_activations.ipynb.

# %% auto 0
__all__ = ['Hook', 'append_stats', 'Hooks', 'get_hist', 'HooksCB']

# %% ../nbs/03_activations.ipynb 2
from .Dataset import *
from .Learner import *
import math,torch,matplotlib.pyplot as plt
from torch import tensor,nn,no_grad
import torch
import torch.nn.functional as F
import fastcore.all as fc
from torch import optim
from copy import copy
from fastprogress import progress_bar,master_bar

import torchvision.transforms.functional as TF
from torcheval.metrics import MulticlassAccuracy,Mean
from functools import partial


# %% ../nbs/03_activations.ipynb 8
class Hook():
    def __init__(self, m, f): self.hook = m.register_forward_hook(partial(f, self))
    def remove(self): self.hook.remove()
    def __del__(self): self.remove()
    
def append_stats(hook, mod, inp, outp):
    if not hasattr(hook,'stats'): hook.stats=([],[],[])
    acts=to_cpu(outp)
    hook.stats[0].append(acts.mean())
    hook.stats[1].append(acts.std())
    hook.stats[2].append(acts.abs().histc(40,0,10))

# %% ../nbs/03_activations.ipynb 12
class Hooks(list):
    def __init__(self, ms, f): super().__init__([Hook(m,f) for m in ms])
    def __enter__(self, *args): return self
    def __exit__(self, *args): self.remove()
    def __del__(self): self.remove()
    def __delitem__(self, i):
        self[i].remove()
        super().__delitem__(i)
    def remove(self):
        for h in self: h.remove()

# %% ../nbs/03_activations.ipynb 13
def get_hist(h): return torch.stack(h.stats[2]).t().float().log1p()

# %% ../nbs/03_activations.ipynb 15
class HooksCB(Callback):
    def __init__(self, hookfunc, mod_filter=fc.noop):
        fc.store_attr()
        super().__init__()
        
    def before_fit(self):
        mods = fc.filter_ex(self.learner.model.modules(), self.mod_filter)
        self.hooks = Hooks(mods, self._hookfunc)
        
    def _hookfunc(self, *args, **kwargs):
        if self.learner.model.training: self.hookfunc(*args, **kwargs)
        
    def after_fit(self): 
        self.hooks.remove()
        fig, axs=plt.subplots(1,2, figsize=(10,4))
        for h in hc:
            for i in 0,1: axs[i].plot(h.stats[0])
        fig,axes=plt.subplots(1,len(hooks),figsize=(10,20))
        for ax,h in zip(axes.flatten(), hooks):
            show_image(get_hist(h), ax, origin='lower', figsize=(20,20))
        
    def __iter__(self): return iter(self.hooks)
    def __len__(self): return len(self.hooks)
    
