import wx
import wx.grid
import pandas as pd
import matplotlib
import numpy as np
matplotlib.use('WXAgg') # allows Matplotlib to render plots within wxPython

from GUI import MyFrame1 as MyFrame

from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg
import matplotlib.pyplot as plt

EVEN_ROW_COLOUR = '#CCE6FF'
GRID_LINE_COLOUR = '#ccc'

class DataTable(wx.grid.GridTableBase):
    def __init__(self, data=None):
        wx.grid.GridTableBase.__init__(self)
        self.headerRows = 1
        self.data = data

    def GetNumberRows(self):
        return len(self.data.index)

    def GetNumberCols(self):
        return len(self.data.columns)

    def GetValue(self, row, col):
        return self.data.iloc[row, col]

    def SetValue(self, row, col, value):
        self.data.iloc[row, col] = value

    # For better visualisation
    def GetColLabelValue(self, col):
        return self.data.columns[col]

    def GetAttr(self, row, col, prop):
        attr = wx.grid.GridCellAttr()
        if row % 2 == 1:
            attr.SetBackgroundColour(EVEN_ROW_COLOUR)
        return attr

def load_file(file_name):
    try:
        df = pd.read_csv(file_name)  # Import the dataset
        return df
    except FileNotFoundError:
        raise FileNotFoundError("Food_Nutrition_Dataset.csv not found in the specified path")

class MyMainFrame(MyFrame):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.df = load_file("Food_Nutrition_Dataset.csv")
        self.filtered_df = self.df.copy() #copy of dataset for filtering
        self.canvas = ''

        self.rows_per_page = 26 #set maximum rows
        self.current_page = 0 #set current page

        self.m_breakdownChoice.Clear()
        unique_foods = self.df['food'].unique()
        unique_foods.sort()
        self.m_breakdownChoice.AppendItems(unique_foods)

        self.m_comparisonSecondary.Clear()
        unique_foods = self.df['food'].unique()
        unique_foods.sort()
        self.m_comparisonSecondary.AppendItems(unique_foods)

        self.m_comparisonPrimary.Clear()
        unique_foods = self.df['food'].unique()
        unique_foods.sort()
        self.m_comparisonPrimary.AppendItems(unique_foods)

        self.RangeCheck = False #range filtering starts disabled
        self.LevelCheck = False #level filtering starts disabled

        #lists of widgets for each setup, search widgets used for searching for food items
        #graph widgets used in the graphing setup
        #these needs to be hidden and show to save space

        self.search_widgets =[self.m_staticText1, self.m_foodSearch, self.m_nutritionRangeCheck, self.m_rangeChoice, self.m_rangeMin, self.m_rangeMax,
                          self.m_NutritionLevelCheck, self.m_nutritionType, self.m_nutritionLevel, self.m_searchButton, self.m_graphSwap,
                              self.m_dataGrid, self.m_staticText7, self.m_staticText8, self.m_currentPage, self.m_staticText10,
                              self.m_pageCount, self.m_previousPage, self.m_nextPage]

        self.graph_widgets = [self.m_staticText4, self.m_breakdownChoice, self.m_barGraph, self.m_pieChart, self.m_staticText5,
                         self.m_comparisonPrimary, self.m_comparisonSecondary, self.m_compareFoods, self.m_foodSwap]


        self.updateGrid()
        self.Show(True)
        self.Layout()



    def onGraphSwap( self, event ): #when user presses data graphing button
        event.Skip()                #it will hide search widgets and show graphing widgets
        for widget in self.search_widgets: #also hides search grid
            widget.Hide()

        for widget in self.graph_widgets:
            widget.Show()
            if self.canvas:
                self.canvas.Show()

        self.GetSizer().Layout()

    def onSearchSwap( self, event ): #when user presses search results button
        event.Skip()                    #hide graph widgets and show search widgets
        for widget in self.graph_widgets: #TBD also needs to hide graph
            widget.Hide()
            if self.canvas:
                self.canvas.Hide()

        for widget in self.search_widgets:
            widget.Show()

        self.GetSizer().Layout()

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
                # wx.MessageBox("The food you searched for is not in the database.", "Invalid Input",
                # wx.OK | wx.ICON_ERROR)
                raise ValueError(f"No data found for '{input_text}'")
            # First find all matches (case insensitive)
            matched_rows = self.filtered_df['food'].str.contains(search_term, case=False, na=False)
            # Create a copy of the filtered dataframe
            result_df = self.filtered_df[matched_rows].copy()
            # Capitalize the first letter of each word in matching food names
            result_df['food'] = result_df['food'].apply(
                lambda x: ' '.join(word.capitalize() if word.lower() in search_term.lower()
                                   else word
                                   for word in x.split()))
            return result_df
        else:
            result = self.filtered_df.loc[self.filtered_df['food'].str.contains(search_term, na=False, case=False)]
            if result.empty:
                # wx.MessageBox("The food you searched for is not in the database.", "Invalid Input",
                # wx.OK | wx.ICON_ERROR)
                raise ValueError(f"No data found for '{input_text}'")
            # For lowercase searches, just return as is
            matched_rows = self.filtered_df['food'].str.contains(search_term, case=False, na=False)
            return self.filtered_df[matched_rows]

    def onSearch( self, event ):
        event.Skip()
        self.filtered_df = self.df.copy() #make a new copy of filtered df
        search_text = self.m_foodSearch.GetValue().strip() #strip down text input
        if search_text: #if there is a value in search field
            self.filtered_df = self.tableSearch(search_text) #pass it through to search function
        else: #otherwise
            self.filtered_df = self.df #grid will display unfiltered df

        if self.RangeCheck: #check if range filter has been checked
            self.filtered_df = self.rangeFilter() #if so then update filtered df based on return from function
        else: #otherwise
            pass #pass

        if self.LevelCheck:#check if level filter has been checked
            self.filtered_df = self.levelFilter() #if so then update filtered df based on return from function
        else: #otherwise
            pass #pass

        self.current_page = 0 #set current page back to 0
        self.updateGrid() #go to update grid function

    def updateGrid(self): #function to refresh the grid
        start_row = self.current_page * self.rows_per_page #determine start row number
        end_row = start_row + self.rows_per_page #determine end row number

        df_to_display = self.filtered_df.iloc[start_row:end_row] #show df but only from start row to end row from before

        self.m_dataGrid.ClearGrid() #clear out old grid
        self.table = DataTable(df_to_display) #datatable of new grid
        self.m_dataGrid.SetTable(self.table, takeOwnership=True) #set the table
        self.m_dataGrid.AutoSize() #autosize
        #self.m_dataGrid.EnableScrolling(True, True) #make sure scrolling is enabled
        #self.m_dataGrid.AlwaysShowScrollbars() #always show the scroll bar, not working !?!?!?!??!?!
        #self.m_dataGrid.ForceRefresh() #didn't help[

        self.updateButtonStates() #go to update buttons
        self.m_currentPage.SetLabel(str(self.current_page+1)) #change current page number, add 1 since start at 0
        self.m_pageCount.SetLabel(str(self.total_pages+1)) #change total pages, start at 0 so add 1
        #self.m_panelContent.Hide()
        #self.m_panelContent.Show()
        self.GetSizer().Layout()

    def updateButtonStates(self): #update buttons so user can't go past 0 or max pages
        # Disable/enable buttons based on current page
        self.m_previousPage.Enable(self.current_page > 0) #enable previous button if current page > 0
        self.total_pages = (len(self.filtered_df) - 1) // self.rows_per_page #calcualte total page length based on df length
        self.m_nextPage.Enable(self.current_page < self.total_pages) #enable next button if current page less than max


    def rangeFilter(self):
        min_range = self.m_rangeMin.GetValue().strip() #strip down min range input
        max_range = self.m_rangeMax.GetValue().strip() #strip down max range input
        nutrition_type = self.m_rangeChoice.GetStringSelection() #check nutrition type selected
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
                wx.MessageBox("Please enter a valid integer for the first input.", "Invalid Input",
                              wx.OK | wx.ICON_ERROR)
                raise ValueError(f"{min_range} contains invalid input'")

        if max_range:#check if max input has a value
            try: #error check
                input_max = int(max_range) #if it passes store input as integer
                max_ok = True #set max to ok as it is valid
            except ValueError:
                wx.MessageBox("Please enter a valid integer for the second input.", "Invalid Input",
                              wx.OK | wx.ICON_ERROR)
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
            wx.MessageBox("Please enter a valid integer for both inputs.", "Invalid Input",
                          wx.OK | wx.ICON_ERROR)
            raise ValueError(f"{min_range} and {max_range} contains invalid input'")
        df_search_filtered = self.filtered_df[index] #new list filtered
        return df_search_filtered #return back to search function

    def levelFilter(self): #function to filter through based on seleected nutrition type and content level
        nutrition_type = self.m_nutritionType.GetStringSelection() #grab typr selected
        nutrition_level = self.m_nutritionLevel.GetStringSelection() #grab level selected

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

        df_search_filtered = self.filtered_df[index] #new filtered df
        return df_search_filtered #return new filtered df

    def onPlotPie( self, event ):
        event.Skip()
        selected_food = self.m_breakdownChoice.GetStringSelection()  # get food name
        if selected_food == '':
            wx.MessageBox("Please select a food", "Invalid Input",
                          wx.OK | wx.ICON_ERROR)
            raise ValueError("No Food Selected.")


        df_food = self.df[self.df['food'] == selected_food]  # food data

        if df_food.empty:
            raise ValueError(f"No data found for '{selected_food}'")

        food_data = df_food.iloc[0]

        nutrients_name = self.df.columns[1:] #nutrient names, exclude first since that is food name
        food_values = food_data[nutrients_name].tolist() #grab food values for each nutrient
        fig,ax = plt.subplots(figsize=(6, 6))  # plot figure
        totals= sum(food_values) #get total of food values
        food_percentages = [] #list of food percentage values
        for value in food_values: #loop through food values
            food_percentages.append((value/totals)*100) #determine percentage of food item against whole group

        legends_labels = [] #list for legend labels
        for nutrients, percentage in zip(nutrients_name,food_percentages): #loop through nutriennt names and percentages
            legends_labels.append(f"{nutrients}: ({percentage:0.3f}%)") #apppend nutrient name and percentage value

        num_colors = len(food_values)
        colors = plt.cm.viridis(np.linspace(0, 1, num_colors))

        ax.pie(food_values, colors=colors, wedgeprops=dict(edgecolor='white')) #create pie chart
        ax.set_title(f"nutrient breakdown for {selected_food}", loc='left') #set title of pie chart
        ax.set_position([0.01,0.1,0.4,0.8]) #move pie chart to make room for legend

        #plt.tight_layout()

        #legend so we can actually see pie chart values
        plt.legend(legends_labels, title="Details of nutrients", loc="center left", bbox_to_anchor=(1,0.4),ncol=2)

        if self.canvas: #if a canvas exists
            self.canvas.Destroy() #destroy it

        h, w = self.m_panelContent.GetSize()  # get size of panel
        fig.set_size_inches(h / fig.get_dpi(), w / fig.get_dpi())  # set size of figure
        self.canvas = FigureCanvasWxAgg(self.m_panelContent, -1, fig)  # draw canvas
        self.canvas.SetSize((h, w))  # set size of canvas
        self.Layout()  # display



    def onCompare( self, event ):
        event.Skip()
        food_1 = self.m_comparisonPrimary.GetStringSelection() #get food name of first selection
        food_2 = self.m_comparisonSecondary.GetStringSelection() #get food name of second selection

        if food_1 == '' or food_2 == '':
            wx.MessageBox("Please select food for both inputs", "Invalid Input",
                          wx.OK | wx.ICON_ERROR)
            raise ValueError("Both food items not selected.")

        df_food1 = self.df[self.df['food'] == food_1] #food data of first selection
        df_food2 = self.df[self.df['food'] == food_2] #food data of second selection

        if df_food1.empty and df_food2.empty:
            raise ValueError(f"No data found for '{food_1}' or '{food_2}'")
        elif df_food1.empty:
            raise ValueError(f"No data found for '{food_1}'")
        elif df_food2.empty:
            raise ValueError(f"No data found for '{food_2}'")

        df_food1 = self.df[self.df['food'] == food_1].iloc[0]  # food data of first selection
        df_food2 = self.df[self.df['food'] == food_2].iloc[0]

        nutrients = self.df.columns[1:] #nutrient names

        values_food_1 = df_food1[nutrients].tolist() #food 1 nutrients
        values_food_2 = df_food2[nutrients].tolist() #food 2 nutrients

        bar_width = 0.35 #bar width, change as needed
        index = np.arange(len(nutrients)) #bar chart coordinates

        fig, ax = plt.subplots(figsize=(8, 4)) #plot figure

        ax.bar(index, values_food_1, bar_width, label=food_1, color='blue') #first set of data
        ax.bar(index + bar_width, values_food_2, bar_width, label=food_2, color='green') #second set of data

        ax.set_xlabel('Nutrients') #x axis label
        ax.set_ylabel('Values') #y axis label
        ax.set_title(f'Comparison of {food_1} vs {food_2}') #graph title
        ax.set_yticks(np.linspace(min(values_food_1+values_food_2), max(values_food_1+values_food_2), 10))
        ax.set_xticks(index + bar_width / 2) #x label spacing
        ax.set_xticklabels(nutrients,rotation=45,ha='right',fontsize='9') #rotate x axis labels
        ax.grid(visible=True, which='both', axis='both')

        plt.tight_layout()

    #    for i, value in enumerate(values_food_1): #loop through food data
    #        if value > 1: #don't want to overflow visual so only show if value > 1
    #            ax.text(i-bar_width/ 2,value+0.3,f'{value}',ha='center',color='blue') #setup text, x axis, y axis, value, position, colour

    #    for i, value in enumerate(values_food_2):#loop through food data
    #        if value > 1:#don't want to overflow visual so only show if value > 1
    #            ax.text(i+bar_width/2,value+0.3,f'{value}',ha='center',color='green')#setup text, x axis, y axis, value, position, colour

        ax.legend() #create a legend to see what is what
        if self.canvas: #if a canvas exists
            self.canvas.Destroy() #destroy it

        h, w = self.m_panelContent.GetSize() #get size of panel
        fig.set_size_inches(h / fig.get_dpi(), w / fig.get_dpi()) #set size of figure
        self.canvas = FigureCanvasWxAgg(self.m_panelContent, -1, fig) #draw canvas
        self.canvas.SetSize((h, w)) #set size of canvas
        self.Layout() #display


    def onPrevious( self, event ): #previous page button
        event.Skip()
        if self.current_page > 0: #check if current page is greater than 0
            self.current_page -= 1 #if so, reduce current page number by 0
            self.updateGrid() #update grid to display previous page

    def onNext( self, event ): #next page button
        event.Skip()
        total_pages = (len(self.filtered_df) - 1) // self.rows_per_page #calculate total number of pages
        if self.current_page < total_pages: #if current page is less than the total
            self.current_page += 1 #add 1 to current page count
            self.updateGrid() #update grid to display next page

    def onRangeCheck( self, event ): #event when range filter button checked
        event.Skip()
        if self.m_nutritionRangeCheck.GetValue(): #if checked, function work, otherwise it is ignored
            self.RangeCheck = True
        else:
            self.RangeCheck = False

    def onLevelCheck( self, event ): #event when level filter button checked
        event.Skip()
        if self.m_NutritionLevelCheck.GetValue(): #if checked, function work, otherwise it is ignored
            self.LevelCheck = True
        else:
            self.LevelCheck = False

    def onPlotBar(self, event):
        selected_food = self.m_breakdownChoice.GetStringSelection() #grab selected food from dropdown
        if selected_food == '':
            wx.MessageBox("Please select a food", "Invalid Input",
                          wx.OK | wx.ICON_ERROR)
            raise ValueError("No Food Selected.")


        df_food = self.df[self.df['food'] == selected_food] #grab food data

        if df_food.empty:
            wx.MessageBox(f"No data found for '{selected_food}'.", "Invalid Input",
                          wx.OK | wx.ICON_ERROR)
            raise ValueError(f"No data found for '{selected_food}'")

        df_food = self.df[self.df['food'] == selected_food].iloc[0]

        macro_nutrients = df_food[2:13].tolist() #nutrient data for macro
        microNutrients = df_food[[11] + list(range(13, 34))].tolist() #food data for micro

        #plt.figure()

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 6)) #figure, both axes, two columns

        macro_columns = self.df.columns[2:13] #macro columns go here
        print(macro_columns)
        micro_columns = self.df.columns[[11] + list(range(13, 34))] #micro columns here

        ax1.bar(macro_columns, macro_nutrients, color='blue', width=0.2) #first bar data
        ax1.set_xlabel('Nutritional Components') #x axis labels
        ax1.set_ylabel('Values') #y axis labels
        #ax1.set_yticks(np.linspace(min(macro_nutrients), max(macro_nutrients), 10))
        ax1.set_title(f'Nutritional Information for {selected_food} Per 100g') #title for first graph
        ax1.set_xticklabels(macro_columns, rotation=45, ha='right') #x axis data labels, rotated so they don't overlap

        ax2.bar(micro_columns, microNutrients, color='blue', width=0.2) #second bar data
        ax2.set_xlabel('Nutritional Components') #x axis labels
        ax2.set_ylabel('Values') #y axis labels
        #ax1.set_yticks(np.linspace(min(micro_columns), max(micro_columns), 10))
        ax2.set_title(f'Micro Nutritional Information for {selected_food} Per 100g') #title for second graph
        ax2.set_xticklabels(micro_columns, rotation=45, ha='right', fontsize='8') #x axis data labels, rotated so they don't overlap

        plt.tight_layout()

    #    for i, value in enumerate(nutrients): #loop through food data
    #        if value > 0.1: #don't want to overflow visual so only show if value > 1
    #            ax1.text(i-0.2/ 2,value+0.1,f'{value} g',ha='center',color='blue') #setup text, x axis, y axis, value, position, colour

    #    for i, value in enumerate(microNutrients):#loop through food data
    #        if value > 0.1:#don't want to overflow visual so only show if value > 1
    #            ax2.text(i+0.2/2,value+0.1,f'{value} mg',ha='center',color='green')#setup text, x axis, y axis, value, position, colour

        if self.canvas: #if a canvas has already been created
            self.canvas.Destroy() #destroy it, this prevents overlapping canvas'

        h, w = self.m_panelContent.GetSize() #set height and width based on panel size
        fig.set_size_inches(h / fig.get_dpi(), w / fig.get_dpi()) #get size of figure
        self.canvas = FigureCanvasWxAgg(self.m_panelContent, -1, fig) #create canvas
        self.canvas.SetSize((h, w)) #set the canvas size
        self.Layout() #display


if __name__ == "__main__":
    app = wx.App()
    frame = MyMainFrame()
    app.MainLoop()
