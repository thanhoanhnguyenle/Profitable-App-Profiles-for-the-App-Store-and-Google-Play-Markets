#!/usr/bin/env python
# coding: utf-8

# # Profitable App Profiles for the App Store and Google Play Markets
# Our goal for this project is to analyze data to help our developers understand what type of apps are likely to attract more users.

# ## Data Loading

# In[1]:


opened_file = open('AppleStore.csv')

from csv import reader
read_file = reader(opened_file)
appstore_data = list(read_file)

opened_file = open('googleplaystore.csv')
from csv import reader
read_file = reader(opened_file)
gpstore_data = list(read_file)


# In[2]:


print(appstore_data)


# In[3]:


print(gpstore_data)


# In[4]:


def explore_data(dataset, start, end, rows_and_columns=False):
    dataset_slice = dataset[start:end]    
    for row in dataset_slice:
        print(row)
        print('\n') # adds a new (empty) line after each row

    if rows_and_columns:
        print('Number of rows:', len(dataset))
        print('Number of columns:', len(dataset[0]))


# In[5]:


explore_data(appstore_data, 1, 6)
explore_data(gpstore_data, 1, 6, True)


# In[6]:


print(appstore_data[0])
print(gpstore_data[0])


# In[7]:


print(gpstore_data[10473])
len(gpstore_data[10473])


# In[8]:


del gpstore_data[10473]
gpstore_data[10473]


# ## Duplicates Removing

# In[9]:


apps = {}
for app in gpstore_data[1:]:  
    if app[0] in apps:
        apps[app[0]] += 1
    else: 
        apps[app[0]] = 1


# In[10]:


duplicates = []
for app in apps: 
    if apps[app] > 1: 
        duplicates.append(app)
print(duplicates)


# From the abode investigation, we can see that the 'Google Play' dataset has duplicates, so we will further look at the duplicates of an app to decide whether or not keep those duplicates, if not, then how the duplicates will be removed. 

# In[11]:


for app in gpstore_data: 
    if app[0] == 'WeChat': 
        print(app) 


# The diffence of the instances are most likely to be selected at different time, since the number of reviews are different over time. This means, the higher the number of reviews are, the more later the instance is. 
# 
# This indicates that we only have to keep the instance with highest reviews number.

# In[12]:


duplicates_removed = []
for i in range(len(duplicates)):
    temp = 0
    instance_kept = []
    for app in gpstore_data: 
        name = app[0] 
        if name == duplicates[i]: 
            if int(app[3]) >= temp: 
                instance_kept.append(app)
                temp = int(app[3])
    instance = instance_kept[-1]
    duplicates_removed.append(instance)
print(duplicates_removed)


# After that, I will concatenate the unique values and removed-duplicated-values in one single dataset which is `gpstore_data_new`

# In[13]:


gpstore_data_new = []
gpstore_data_new.append(gpstore_data[0])
for app in apps: 
    if apps[app] == 1: 
        for instance in gpstore_data: 
            if app == instance[0]:
                gpstore_data_new.append(instance)
gpstore_data_new.extend(duplicates_removed)
print(gpstore_data_new)


# So I have finished creating a new dataset without duplicates, let's count to check if the new dataset has the exact length.

# In[14]:


print(len(gpstore_data_new))


# ## Removing Non-English names

# I created a function to remove the observations of non-

# In[15]:


def english_named(name):
    count = 0
    for letter in name: 
        if ord(letter) > 127:
            count += 1
            if count > 2: 
                return False
    return True


# In[16]:


english_kept = []
for app in gpstore_data_new[1:]: 
    if english_named(app[0]): 
        english_kept.append(app)
        
print(english_kept)


# In[17]:


print(len(english_kept))


# ## Free Apps Isolation

# In[18]:


free_apps = []
for app in english_kept: 
    if app[6] == 'Free':
#         print(app[6])
        free_apps.append(app)
        
print(len(free_apps))


# ## Most Common Apps by Genre

# The aim of this project is determine the kinds of apps that are likely to attract more users since the revenue is highly influenced by the number of people using apps. Therefore, I will further investigate the popularity of the apps on both platform GooglePlay Store and AppStore based on their genres and categories.

# In[19]:


def freq_table(dataset, index):
    freq_table = {}
    for app in dataset: 
        name = app[index]
        if app[index] in freq_table: 
            freq_table[name] += 1
        else: 
            freq_table[name] = 1
    return freq_table
            
def display_table(dataset, index):
    table = freq_table(dataset, index)
    table_display = []
    for key in table:
        key_val_as_tuple = (table[key], key)
        table_display.append(key_val_as_tuple)

    table_sorted = sorted(table_display, reverse = True)
    for entry in table_sorted:
        print(entry[1], ':', entry[0])


# In[30]:


gps_category_tab = freq_table(free_apps, 1)
print(gps_category_tab)


# In[21]:


gps_genres_tab = freq_table(free_apps, 9)
print(gps_genres_tab)


# The most common genre in Google Play Store is "Family", the second most is "Game", then "Tools", "Productivity" and "Lifestyle". 
# 
# Regarding category, the most popular categories are "Entertainment", "Education", "Business", "Sport"... 
# 
# The general impression is that Google Play shows a balanced landscape of both practical and entertaining apps. 

# In[22]:


as_genres_tab = freq_table(appstore_data[1:], -5)
print(as_genres_tab)


# The most popular app in Appstore is "Game" (3862), "Entertainment" (535), "Education" (453), "Photo & Video" (349). From what I see, most of those popular apps on Appstore belongs to Entertaining Category. However, it doesn't imply that apps of those genres have a large number of users. 

# ## Most Popular Apps by Genre on the App Store & Google Play
# 
# - One way to find out what genres are the most popular (have the most users) is to calculate the average number of installs for each app genre. For the Google Play dataset, we can find this information in the Installs column, but this information is missing for the App Store dataset. As a workaround, we'll take the total number of user ratings as a proxy, which we can find in the `rating_count_tot` app.

# Below I generate a function that takes in the dataset name, the frequency table, the index of genre/category, the index of total rating count/installs, and a default value of whether or not return the max value of the dictionary. This function will return the dictionary with genre/category name as key and average number of installs as value.

# In[31]:


def char_remove(installs):
    installs = installs.replace('+', '')
    installs = installs.replace(',', '')
    return installs
    
def avg_installs(dataset, freq_tab, category_index, user_installs_index, max_value = False):
    avg_installs = {}
    for category in freq_tab: 
        total = 0
        len_category = 0
        for app in dataset:
            if app[category_index] == category:
                len_category += 1
                install_num = char_remove(app[user_installs_index])
                total += int(install_num)
        avg_installs[category] = int(total / len_category)
    
    if max_value:
        max_value = max(avg_installs, key=lambda k: float(avg_installs[k]))
        print(f"Highest average installs is '{max_value}': {avg_installs[max_value]}")
    return avg_installs


# In[32]:


avg_as_installs = avg_installs(appstore_data, as_genres_tab, -5, 5)
print(avg_as_installs)


# In[33]:


avg_gp_installs = avg_installs(gpstore_data, gps_category_tab, 1, 5)
print(avg_gp_installs)


# From what I have seen so far, I personally recommend an app belongs to a genre that has high number of Installs but low number of apps count, since it means the demand for that genre (installs) is lower than the supply (apps designed). For this reason, I create a function that returns the ratio of installs/app counts of each genre, the genre with the highest ratio will be recommended.

# In[43]:


def installs_genres_ratio(avg_installs, freq_tab):
    installs_genres_ratio = {}
    for genre in freq_tab: 
        ratio = round(avg_installs[genre] / freq_tab[genre], 2)
        installs_genres_ratio[genre] = ratio
    return installs_genres_ratio


# In[45]:


as_installs_genres_ratio = installs_genres_ratio(avg_as_installs, as_genres_tab)
gps_installs_genres_ratio = installs_genres_ratio(avg_gp_installs, gps_category_tab)
as_ratio_max = max(as_installs_genres_ratio, key=lambda k: float(as_installs_genres_ratio[k]))
gps_ratio_max = max(gps_installs_genres_ratio, key=lambda k: float(gps_installs_genres_ratio[k]))

print(as_installs_genres_ratio)
print(as_ratio_max)
print('----------------------')
print(gps_installs_genres_ratio)
print(gps_ratio_max)


# From the information above, I decided to recommend a Social Networking app profile for both platform, based on the fact that the ratio of installs to apps of this genre is hight in both platform, indicates that there are rooms for our newly launched app to compete.
