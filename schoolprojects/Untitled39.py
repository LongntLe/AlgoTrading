
# coding: utf-8

# In[3]:

get_ipython().magic(u'matplotlib inline')
from scipy import stats
import numpy as np
import random
import matplotlib.pyplot as plt

def create_norm_pop(n): #creates and returns a random normal-like population distribution
    distrib = 1000 * np.random.normal(0,1,(n, )) # o: mean; 1: SD 
    return distrib

#sample_size = int(raw_input("Enter the sample size - for example 1,000: "))
def test_hypothesis(population, sample_size):
    #sample_mean = pop_mean = null hypothesis
    #sam_ > pop_ then type 1 error
    #sam_ < pop_ then type 1 error
    
    
    pop_mean = np.mean(population)
    pop_std = np.std(population)
    sample = np.random.choice(population,(sample_size, ))
    sample_std = np.std(sample)
    sample_mean = np.mean(sample)
        
    mean_dif = pop_mean - sample_mean
       
    SE = ((pop_std**2/len(population)) + (sample_std**2/sample_size))**0.5 #finding standard error
    
    #t-value = 1.96 for 95% interval
    
    lower_bound = 0 - 1.96*SE
    upper_bound = 0 + 1.96*SE
    
    return mean_dif >= lower_bound and mean_dif <= upper_bound #the test return true if the mean dif is in the interval 

pop1 = create_norm_pop(2000)
pop2 = create_norm_pop(2000)
#sample_size = int(raw_input("Enter the sample size - for example 1,000: "))
sample_repeats = int(raw_input("Enter the number of times to repeat the experiment - for example 1,000: "))
error_count = 0.0

for i in range (sample_repeats): #check both hypothesis at the same time
    if not test_hypothesis(pop1, sample_size) or not test_hypothesis(pop2, sample_size): #test type 1 error
        error_count = error_count + 1
            
print error_count/sample_repeats


# In[ ]:



