# grocery-and-meal-assistant
Application to help users develop grocery list, form recipes, and plan meals based on nutritional, budgetary, and other preferences.

## Introduction

## Architecture
### Data Structure
The Recepticon application is made up of several different data tables. There are 4 primary
data tables that make up the application. These data are stored in the ... defined above in the [Architecture](#Architecture) section.
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
