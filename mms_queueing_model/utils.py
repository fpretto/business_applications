import pandas as pd
import numpy as np
pd.set_option('display.float_format', '{:.6f}'.format)

def get_mms_queue(lam, mu, servers):
    """
    Calculates M/M/S statistics for solving queueing problems
    
    Params:
        - lam: arrival rate
        - mu: service rate
        - servers: number of servers to analize

    Returns:
        - DataFrame with M/M/S statistics
    """
    df = pd.DataFrame(columns=['S', 'Lq', 'Ls', 'Wq', 'Ws', 'prob_0', 'prob_delay', 'rho'])
    lam_mu = lam/mu
    inter_calc = 1
    cumsum = 1

    for s in range(servers+1):
        if s==0:
            row = {'S': [s],
                   'Lq': [np.nan],
                   'Ls': [np.nan],
                   'Wq': [np.nan],
                   'Ws': [np.nan],
                   'prob_0': [np.nan],
                   'prob_delay': [np.nan],
                   'rho': [np.nan]}

            df = df.append(pd.DataFrame.from_dict(row))

        else:
            inter_calc = inter_calc * lam_mu / s
            rho = min(1, lam/(s*mu))
            prob_0 = 1/(cumsum + inter_calc/(1-rho)) if rho<1 else 0        
            prob_delay = 1-prob_0*cumsum if rho<1 else 1
            Lq = prob_0*inter_calc*rho/(1-rho)**2 if rho<1 else np.nan
            Ls = Lq + lam_mu if rho<1 else np.nan
            Wq = Lq / lam if rho<1 else np.nan
            Ws = Wq + 1/mu if rho<1 else np.nan
            cumsum = cumsum + inter_calc

            row = {'S': [s],
                   'Lq': [Lq],
                   'Ls': [Ls],
                   'Wq': [Wq],
                   'Ws': [Ws],
                   'prob_0': [prob_0],
                   'prob_delay': [prob_delay],
                   'rho': [rho]}

            df = df.append(pd.DataFrame.from_dict(row))
        
    return df.reset_index(drop=True)        