## W210 Synthetic Capstone project, UC-Berkeley MIDS Fall 2018
## Team Recepticon

# Libraries
import pandas as pd

# define user class
class User:
    def __init__(self, user_name, pw1, pw2):
        self.name = user_name
        if pw1 == pw2:
            self.password = pw1
        else:
            print("Passwords do not match, please re-enter password")

    def general(self, age, h, w, g, freq): # h = height(inches), w = weight(lb), g = gender, freq (how often you go grocery shopping)
        self.age = age
        self.h = h
        self.w = w
        self.g = g
        self.freq = freq

    def add_nutrition(self, exer, fruit, vegetables, grains, meat, goal, r_fat, r_carb, r_protein, d_cal):
        self.exer = exer # exercise frequency
        self.fruit = fruit # desired servings of fruit per day
        self.veg = vegetables # desired servings of fruit per day
        self.grains = grains # desired servings of fruit per day
        self.meat = meat # desired servings of fruit per day
        self.goal = goal # gain muscle, stay the same, lose weight
        self.r_fat = r_fat # ratio of fat to total caloric intake
        self.r_carb = r_carb # ratio of carb to total caloric intake
        self.r_protein = r_protein # ratio of protein to total caloric intake
        self.d_cal = d_cal # target daily caloric intake 

    def p_user(self):
        print("I am a ", self.age, " year old ", self.g, "who shops", self.freq, " times a day.")
