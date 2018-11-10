# grocery-and-meal-assistant
Application to help users develop grocery list, form recipes, and plan meals based on nutritional, budgetary, and other preferences.
## Table of Contents
1. [Introduction](#introduction)  
  a. [Objective](#objective)  
  b. [Workflow](#workflow)  
  c. [Recommendation System](#recommendation-system)  
    1. [User Preferences](#user-preferences)  
      i. [Fit Score](#fit-score)
    2. [Collaborative Filtering](#collaborative-filtering)  
2. [Architecture](#architecture)  
  a. [Data Structure](#data-structure)  
    1. [Account Data](#account-data)  
    2. [Grocery List Data](#grocery-list-data)  
    3. [Recipe Data](#recipe-data)    
    4. [Food Item Data](#food-item-data)  
    5. [User Recipe Score Data](#user-recipe-score-data)  
3. [Data Sources](#data-sources)
4. [User Guide](#user-guide)
5. [Team](#team)

## Introduction
### Objective
Food impacts several components of our daily life, from our health to our overall happiness. With the increasing ability of grocery store chains to accomodate online ordering and fast delivery, we feel there is a need to assist users to choose what they order in such a way that helps meet their needs in several key areas:  
* Nutrition
* Budget
* Personal Taste
* Time  

To do this, we have created an application which we call **Recepticon**. Users will leverage the application to quickly identify the grocery items and recipes that acheive their personalized mix of priorities. Interactive components of the application allows users to modify and choose recommendations.

### Workflow
The app will require users to have an account, which will store essential user data such as nutrition goals, allergies, and meal preferences. 

Users will then start by loading a grocery list. The current prototype allows for users to search a fixed list of ingredients and add them one at a time. In future versions, we expect the application will accept an upload in .txt or .csv format. Once a grocery list is uploaded, the item inventory will be stored to the users profile. Users can store multiple grocery lists with the ability to load, modify, and delete them as desired.

Users can utilize the recipe optimizer to generate a list of recipes recommended based on the active grocery list and other filters manually adjustable by the user. Subsitution recommendations will also be made based on the allowable substitutions constraint.

Currently, the prototype does not support any visualization of grocery stats such as aggregated calorie count and fat-carb-protein ratio. Future versions will incorporate an analysis of the active grocery list.

### Recommendation System
Recepticon is a hybrid recommendation system which takes into account user preferences as well as influence of other users by way of collaborative filtering.
#### User Preferences
During the account creation phase, users will enter information such as their age, height, gender, and activity level to produce nutritional contraints from which the system will incorporate into its *fit score*. Future versions will also incorporate budgetary contraints.

This portion of the recommendation sytem is *knowledge based* and will utilize information inputted by the user to determined the best recipes for the user based on the calculated *fit score*.
##### Fit Score
The *fit score* is a simple weight average of the cosine dissimilarity between *nutrition*, *complexity*, and *preference*. These are calculated as such by the system:

[reserved]

#### Collaborative Filtering
The second facet of the recommendation system is collaborative filtering. It is not anticipated that collaborative filtering will be implemented as part of the Capstone design product/prototype because a large user base is needed in order for collaborative filtering to be effective. The idea behind this is that users from the community with similar preferences will influence recommendations. 

[reserved - continue to elaborate about technical implementation]

## Architecture
* Flask - front-end for web application
* Python 3 - back-end code for Recommendation System, user management, and other tooling
* Sci-kit-learn - machine learning toolkit utilized for knowledge-based recommendation system
* SQLite - Relational database for storing user data
* NoSQL - store grocery list and other data as pickled Python objects

![First draft - Recepticon architecture.](https://raw.githubusercontent.com/cgutwein/grocery-and-meal-assistant/master/arch_01.PNG)
### Data Structure
The Recepticon application is made up of several different data tables. There are 5 primary
data tables that make up the application. These data are stored in the ... defined above in the [Architecture](#architecture) section.
#### Account Data
Each time a new account is initiated, the user vital characteristics and attributed are stored
to the *Account Data* table. Flask's LoginManager is being utilized to implement password hashing. This data is mostly initiated during the account set-up sequence but can be adjusted at any time manually by the user. The data is in the form:

| Username      | Password      | Age      | ... | ... | Allergies       |
| ------------- | ------------- | -------- | --- | --- | --------------- |
| alpha_bob     | kanye000000   | 45       | ... | ... | [peanut, gluten]|
| beta_cathy    | pw123         | 61       | ... | ... |  []             |

#### Grocery List Data
Users can upload or create a grocery list. A historical set of grocery lists can be stored in a
user account to access or duplicate for later use. Grocery list data is stored in a data table that takes the form:

| Username      | list_name            | file_name                            |
| ------------- | ---------------------| -----------------------------------  | 
| alpha_bob     | mylist_1             | 9e84951b2d0045c08a06001231c7729d.pkl |
| alpha_bob     | dinner_party         | e03fb853493247f2a0e6adc74f1f58d8.pkl |

Grocery lists are stored as python objects in a .pkl file. The grocery list class structure is defined as follows:  

`class GroceryList:
    def __init__(self, name, user_id):
        self.name = name
        self.user_id = user_id
        self.groc_list = [] # initialize with empty list of items
        self.filename = uuid.uuid4().hex + '.pkl'

    def add_item(self, item):
        self.groc_list.append(item)
        print(item + " has been added to " + self.name + ".")

    def delete_item(self, item):
        self.groc_list.remove(item)
        print(item + " has been removed from " + self.name + ".")

    def get_items(self):
        print("Current items in " + self.name + ":")
        for item in self.groc_list:
            print(item)

    def save_list(self):
        with open(self.filename, 'wb') as output:  # Overwrites any existing file.
            pickle.dump(self, output, -1)

    def clear_list(self):
        self.groc_list = []
`

#### Recipe Data
Recipe data is stored across two separate documents:

* Informative .json that includes text, ingredient list, url, and image.
* ingredient matrix in a .csv - sparse matrix for cross referencing ingredients

#### Food Item Data
A list of available ingredients from which users can create grocery lists in the form of a .csv. This list is an exact match to all the ingredients in the recipe .csv.

#### User Recipe Score Data
[Reserved]


## Data Sources
https://www.kaggle.com/hugodarwood/epirecipes/version/2


## User Guide

## Team
This application was developed for UC Berkeley's Master of Information and Data Science (MIDS) program W210 Capstone course.
* Chet Gutwein
* Andrew Mamroth
* Albero Melgoza
* Veronika Nuretdinova
