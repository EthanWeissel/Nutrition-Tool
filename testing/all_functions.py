import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def load_file(file_name):
    try:
        df = pd.read_csv(file_name)  # Import the dataset
        return df
    except FileNotFoundError:
        raise FileNotFoundError("Food_Nutrition_Dataset.csv not found in the specified path")


class MyMainFrame:
    def __init__(self, parent=None):
        self.df = load_file("../Food_Nutrition_Dataset.csv")
        self.filtered_df = self.df.copy()


    def tableSearch(self, input_text):
        # Type checking
        special_characters = {'@', '_', '!', '#', '$', '%', '^', '&', '*', '(', ')', '<', '>', '?', '/', '\\', '|', '}',
                              '{', '~', ':'}
        if not isinstance(input_text, str):
            raise ValueError("Search input must be a string")
        if input_text.isdigit():
            raise ValueError("Search input cannot be numeric")
        if any(char in special_characters for char in input_text):
            raise ValueError("No Special Symbols allowed")


        # Handle empty input
        if not input_text.strip():
            return self.filtered_df.copy()

        # Clean input - remove leading/trailing whitespace
        search_term = input_text.strip()

        # Create mask for matching rows
        # If the search term is capitalized, we'll capitalize the first letter of matching results
        if search_term[0].isupper():
            result = self.filtered_df.loc[self.filtered_df['food'].str.contains(search_term, na=False, case=False)]
            if result.empty:
                #wx.MessageBox("The food you searched for is not in the database.", "Invalid Input",
                              #wx.OK | wx.ICON_ERROR)
                raise ValueError(f"No data found for '{input_text}'")
            # First find all matches (case insensitive)
            matched_rows = self.filtered_df['food'].str.contains(search_term, case=False, na=False)
            # Create a copy of the filtered dataframe
            result_df = self.filtered_df[matched_rows].copy()
            # Capitalize the first letter of each word in matching food names
            result_df['food'] = result_df['food'].apply(lambda x: ' '.join(word.capitalize() if word.lower() in search_term.lower()
                                                                         else word
                                                                         for word in x.split()))
            return result_df
        else:
            result = self.filtered_df.loc[self.filtered_df['food'].str.contains(search_term, na=False, case=False)]
            if result.empty:
                #wx.MessageBox("The food you searched for is not in the database.", "Invalid Input",
                              #wx.OK | wx.ICON_ERROR)
                raise ValueError(f"No data found for '{input_text}'")
            # For lowercase searches, just return as is
            matched_rows = self.filtered_df['food'].str.contains(search_term, case=False, na=False)
            return self.filtered_df[matched_rows]

    def onPlotBar(self, user_input):  # Plot bar chart for the nutritional breakdown of a food item
        selected_food = user_input
        if selected_food == '':
            #wx.MessageBox("Please select a food", "Invalid Input",
                          #wx.OK | wx.ICON_ERROR)
            raise ValueError("No Food Selected.")

        df_food = self.df[self.df['food'] == selected_food]

        if df_food.empty:
            #wx.MessageBox(f"No data found for '{selected_food}'.", "Invalid Input",
                          #wx.OK | wx.ICON_ERROR)
            raise ValueError(f"No data found for '{selected_food}'")

        df_food = self.df[self.df['food'] == selected_food].iloc[0]

        # Assuming that nutrients are in columns, and we want to plot them
        #nutrients = ["Caloric Value", "Protein", "Fat", "Carbohydrates"]   # Example nutrient columns
        nutrients_name = self.df.columns[1:]
        nutrient_values = df_food[nutrients_name].mean()  # Aggregate by mean if multiple rows

        # Plotting the bar chart
        plt.bar(nutrients_name, nutrient_values)
        plt.title(f'Nutritional Breakdown of {selected_food}')
        plt.xlabel('Nutrients')
        plt.ylabel('Values')
        #plt.show()

        return pd.DataFrame({
            "Nutrient": nutrients_name,
            "Value": nutrient_values
        })  # Return a dataframe for testing purposes

    def onPlotPie(self, user_input):  # Plot pie chart for the nutritional breakdown of a food item
        selected_food = user_input

        if selected_food == '':
            # wx.MessageBox("Please select a food", "Invalid Input",
            # wx.OK | wx.ICON_ERROR)
            raise ValueError("No Food Selected.")


        df_food = self.df[self.df['food'] == selected_food]

        if df_food.empty:
            raise ValueError(f"No data found for '{selected_food}'")


        df_food = df_food.iloc[0]

        # Assuming that nutrients are in columns
        nutrients_name = self.df.columns[1:]   # Example nutrient columns
        nutrient_values = df_food[nutrients_name].values



        # Plotting the pie chart
        plt.pie(nutrient_values, labels=nutrients_name, autopct='%1.1f%%')
        plt.title(f'Nutritional Breakdown of {selected_food}')
        #plt.show()

        return pd.DataFrame({
            "Nutrient": nutrients_name,
            "Value": nutrient_values
        })  # Return a dataframe for testing purposes

    def onCompare(self, input_1, input_2):  # Compare nutritional values of two food items
        food_1 = input_1
        food_2 = input_2


        if food_1 == "" or food_2 == "":
            #wx.MessageBox("Please select food for both inputs", "Invalid Input",
                          #wx.OK | wx.ICON_ERROR)
            raise ValueError("Both food items not selected.")


        df_food1 = self.df[self.df['food'] == food_1]  # food data of first selection
        df_food2 = self.df[self.df['food'] == food_2]



        if df_food1.empty and df_food2.empty:
            raise ValueError(f"No data found for '{food_1}' or '{food_2}'")
        elif df_food1.empty:
            raise ValueError(f"No data found for '{food_1}'")
        elif df_food2.empty:
            raise ValueError(f"No data found for '{food_2}'")

        df_food1 = self.df[self.df['food'] == food_1].iloc[0]  # food data of first selection
        df_food2 = self.df[self.df['food'] == food_2].iloc[0]


        # Assuming that nutrients are in columns
        nutrients_name = self.df.columns[1:]  # Example nutrient columns
        nutrient_values_food1 = df_food1[nutrients_name].mean()
        nutrient_values_food2 = df_food2[nutrients_name].mean()

        # Plotting comparison
        width = 0.35  # Width of bars
        fig, ax = plt.subplots()
        ax.bar(nutrients_name, nutrient_values_food1, width, label=food_1)
        ax.bar([n + width for n in range(len(nutrients_name))], nutrient_values_food2, width, label=food_2)

        ax.set_xlabel('Nutrients')
        ax.set_title(f'Comparison of {food_1} and {food_2}')
        ax.legend()
        #plt.show()

        # Modified return statement to match the expected column names in the test
        return pd.DataFrame({
            "Nutrient": nutrients_name,
            f"{food_1.capitalize()} Value": nutrient_values_food1,
            f"{food_2.capitalize()} Value": nutrient_values_food2
        })

    def rangeFilter(self, input_1, input_2, input_3):
        min_range = input_1.strip() #strip down min range input
        max_range = input_2.strip() #strip down max range input
        nutrition_type = input_3 #check nutrition type selected
        min_ok = False #by default min and max is not ok, as it is invalid
        max_ok = False

        special_characters = {'@', '_', '!', '#', '$', '%', '^', '&', '*', '(', ')', '<', '>', '?', '/', '\\', '|', '}',
                              '{', '~', ':'}
        if not isinstance(nutrition_type, str):
            raise ValueError("Nutrition type must be a string")
        if nutrition_type.isdigit():
            raise ValueError("Nutrition type cannot be numeric")
        if any(char in special_characters for char in nutrition_type):
            raise ValueError("Nutrition type cannot contain symbols")
        if nutrition_type == '':
            raise ValueError("Please select a nutrition type")

        if min_range: #check if min input has a value
            try: #error check
                input_min = int(min_range) #if it passes store input as integer
                min_ok = True #set min to ok as it is valid
            except ValueError: #print error
                #wx.MessageBox("Please enter a valid integer for the first input.", "Invalid Input",
                              #wx.OK | wx.ICON_ERROR)
                raise ValueError(f"{min_range} contains invalid input'")

        if max_range:#check if max input has a value
            try: #error check
                input_max = int(max_range) #if it passes store input as integer
                max_ok = True #set max to ok as it is valid
            except ValueError:
                #wx.MessageBox("Please enter a valid integer for the second input.", "Invalid Input",
                              #wx.OK | wx.ICON_ERROR)
                raise ValueError(f"{max_range} contains invalid input'")

        ser_nutrition = self.filtered_df[nutrition_type] #grabbing column based on selected nutritoon type
        index = [] #create list
        if min_ok and max_ok: #setup if both min and max contain valid input
            for nutrition in ser_nutrition:  #loop through and select each item
                if input_min <= nutrition <= input_max: #check if user input is less than value and value less than max
                    index.append(True) #if so add to new list
                else: #otherwise
                    index.append(False) #don't add to new list
        elif min_ok: #setup if min contains valid input
            for nutrition in ser_nutrition: #loop through and select each item
                if input_min <= nutrition: #check if user input is less than value
                    index.append(True) #if so add to new list
                else: #otherwise
                    index.append(False) #don't add to new list
        elif max_ok: #setup if max contains valid input
            for nutrition in ser_nutrition:  #loop through and select each item
                if nutrition <= input_max: #check if nutrition less than user input max value
                    index.append(True) #if so add to new list
                else: #otherwise
                    index.append(False) #don't add to new list
        else: #setup if neither contain valid input
            #wx.MessageBox("Please enter a valid integer for both inputs.", "Invalid Input",
                          #wx.OK | wx.ICON_ERROR)
            raise ValueError(f"{min_range} and {max_range} contains invalid input'")
        df_search_filtered = self.filtered_df[index] #new list filtered
        return df_search_filtered #return back to search function

    def levelFilter(self): #function to filter through based on seleected nutrition type and content level
        nutrition_type = self.m_nutritionType.GetStringSelection() #grab typr selected
        nutrition_level = self.m_nutritionLevel.GetStringSelection() #grab level selected

        errors = []

        if nutrition_type not in ['Protein', 'Carbohydrates', 'Sugars', 'Fat', 'Nutrition Density']:
            errors.append(f"Invalid nutrition type selected: {nutrition_type}")
            if nutrition_level not in ['Low', 'Medium', 'High']:
                errors.append(f"Invalid nutrition level selected: {nutrition_level}")
                raise ValueError(" and ".join(errors))
            else:
                raise ValueError(errors[0])

        #if nutrition_level not in ['Low', 'Medium', 'High']:
            #errors.append(f"Invalid nutrition level selected: {nutrition_level}")

        ser_nutrition = self.filtered_df[nutrition_type] #filter df based on selected nutrition type
        max_nutrition = max(ser_nutrition) #get highest nutrition value based on nutrition selected
        index = [] #new list
        if nutrition_level == "Low": #check if nutriiton content level is Low
            for nutrition in ser_nutrition: #loop through and select each item
                if nutrition < max_nutrition*0.33: #check if entry is less than 33% of max
                    index.append(True) #if so add to new list
                else: #otherwise
                    index.append(False) #don't add to list
        elif nutrition_level == "Medium": #check if nutriiton content level is Medium
            for nutrition in ser_nutrition: #loop through and select each item
                if max_nutrition*0.33 <= nutrition <= max_nutrition*.66: #check if it is between 33% and 66% of max
                    index.append(True) #if so add to new list
                else: #otherwise
                    index.append(False) #don't add to list
        elif nutrition_level == "High": #check if nutriiton content level is High
            for nutrition in ser_nutrition: #loop through and select each item
                if nutrition > max_nutrition*.66: #check if entry is greater than 66% of max
                    index.append(True) #if so add to new list
                else: #otherwise
                    index.append(False) #don't add to list
        else:
            raise ValueError(f"Invalid nutrition level selected: {nutrition_level}")

        df_search_filtered = self.filtered_df[index] #new filtered df
        return df_search_filtered #return new filtered df