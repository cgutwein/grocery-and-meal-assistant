import pandas as pd
import numpy as np
import uuid
import pickle

# The Mifflin St Jeor Equation for Basal Metabolic Rate (BMR) or resting calorie burn rate
# Accounting for Activity Level and Goals
# Activity Acts as a multiplier to one's BMR
# The Academy of Nutrition and Dietetics recommends aiming for 1-2 pounds per week of weight lost.
# For our purposes we aim for 1 lb per week.

def calc_cal(weight, height, age, gender, gym, goals):

    """BMR is calculated by the following equation:
    P = (10.0*m + 6.25*h - 5.0*a +s)
    P = kcal burned at rest
    m = mass in kg
    h = height in cm
    a = age in years
    s = -5 for females and +161 for males

    BMR is then multiplied by an activity level factor, then adjusted by user goal
    """

    act_level = {0:1.2, 1:1.375, 2:1.55, 3:1.725}
    goals_c = {0:-1, 1:1, 2:0}

    m = weight*0.453592
    h = height*2.54
    a = float(age)
    if gender=='m':
        s = 161.0
    else:
        s = -5.0

    bmr = (10.0*m + 6.25*h - 5.0*a +s)
    act_mult = act_level[gym]
    user_goal = 500.0*goals_c[goals]

    return int(bmr*act_mult + user_goal)

def calc_macros(daily_cal, weight, goal):

    goals_p = {0:0.85, 1:1.0, 2:0.85}
    #act_mult = act_level[user_calc.iloc[0]['act_level']]
    p_mult = goals_p[goal]

    p = p_mult*weight
    f = (0.25*daily_cal)/9
    c = (daily_cal-p*4-f*9)/4

    return int(p),int(f),int(c)

def list_gen():
    data = data=pd.read_csv('../python/data/data.csv')
    n = len(data)
    df = pd.DataFrame(data = {'scores':np.repeat(3,len(data)), 'man': np.repeat(0,len(data))})
    filename = 'user_scores/' + uuid.uuid4().hex + '.pkl'
    with open(filename, 'wb') as output:  # Overwrites any existing file.
        pickle.dump(df, output, -1)
    return filename
