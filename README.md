# grocery-and-meal-assistant
Application to help users develop grocery list, form recipes, and plan meals based on nutritional, budgetary, and other preferences.
## Table of Contents
1. [Introduction](#introduction)  
  a. [Objective](#objective)  
  b. [Workflow](#workflow)  
  c. [Recommendation System](#recommendation-system)  
    1. [User Preferences](#user-preferences)  
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

Users will then start by loading a grocery list. The application will accept an upload in .txt or .csv format. Once a grocery list is uploaded, the item inventory will be stored to the users profile.

Users can utilize the recipe optimizer to generate a list of recipes recommended based on the active grocery list and other filters manually adjustable by the user. Subsitution recommendations will also be made based on the allowable substitutions constraint.

An analysis of the active grocery list can be viewed.

### Recommendation System
Recepticon is a hybrid recommendation system which takes into account user preferences as well as influence of other users by way of collaborative filtering.
#### User Preferences
#### Collaborative Filtering

## Architecture
* Flask - front-end for web application
* Python 3 - back-end code for Recommendation System, user management, and other tooling
* Sci-kit-learn - machine learning toolkit utilized for knowledge-based recommendation system
* Reserved - Relational database for storing data

![First draft - Recepticon architecture.](https://raw.githubusercontent.com/cgutwein/grocery-and-meal-assistant/master/arch_01.PNG)
### Data Structure
The Recepticon application is made up of several different data tables. There are 5 primary
data tables that make up the application. These data are stored in the ... defined above in the [Architecture](#architecture) section.
#### Account Data
Each time a new account is initiated, the user vital characteristics and attributed are stored
to the *Account Data* table. This data is mostly initiated during the account set-up sequence
but can be adjusted at any time manually by the user. The data is in the form:

| Username      | Password      | Age      | ... | ... | Allergies       |
| ------------- | ------------- | -------- | --- | --- | --------------- |
| alpha_bob     | kanye000000   | 45       | ... | ... | [peanut, gluten]|
| beta_cathy    | pw123         | 61       | ... | ... |  []             |

#### Grocery List Data
Users can upload or create a grocery list. A historical set of grocery lists can be stored in a
user account to access or duplicate for later use. Grocery list data is stored in a data table that takes the form:

| Username      | Timestamp            | Title          | Items           |
| ------------- | ---------------------| -------------- | --------------- |
| alpha_bob     | 10-11-2018 08:00:00  | routine_list1  | [list of items] |
| alpha_bob     | 10-01-2018 11:15:00  | thifty_list1   | [list of items] |

#### Recipe Data

#### Food Item Data

#### User Recipe Score Data


## Data Sources

## User Guide

## Team
