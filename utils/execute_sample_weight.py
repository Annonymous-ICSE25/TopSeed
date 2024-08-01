import numpy as np
import random
from scipy.stats import truncnorm

def sample(n_features, n_section, prob_w_info, prob_w_section):
    weight_vector = [random.uniform(-1, 1) for _ in range(n_features)]
    for j in range(n_features):
        if np.sum(prob_w_section[j]) == 0.0:
            continue
        component = np.random.choice(n_section, p=prob_w_section[j])
        loc_ = prob_w_info[j][component][0]
        scale_ = prob_w_info[j][component][1]

        a_ = (-1.0 - loc_) / scale_
        b_ = (1.0 - loc_) / scale_

        sample = truncnorm.rvs(a=a_, b=b_, loc=loc_, scale=scale_)
        weight_vector[j] = sample

    return weight_vector