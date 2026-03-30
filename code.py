import wx
import wx.grid
import pandas as pd
import matplotlib
import numpy as np

matplotlib.use('WXAgg')  # Allows Matplotlib to render plots within wxPython

from GUI import MyFrame1 as MyFrame
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg
import matplotlib.pyplot as plt

EVEN_ROW_COLOUR = '#CCE6FF'
GRID_LINE_COLOUR = '#ccc'


class DataTable(wx.grid.GridTableBase):
    """Wraps a pandas DataFrame for display in a wx.grid.Grid."""

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

    def GetColLabelValue(self, col):
        return self.data.columns[col]

    def GetAttr(self, row, col, prop):
        attr = wx.grid.GridCellAttr()
        if row % 2 == 1:
            attr.SetBackgroundColour(EVEN_ROW_COLOUR)
        return attr


def load_file(file_name):
    """Load a CSV file and return it as a DataFrame."""
    try:
        return pd.read_csv(file_name)
    except FileNotFoundError:
        raise FileNotFoundError(f"{file_name} not found in the specified path")


class MyMainFrame(MyFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.df = load_file("Food_Nutrition_Dataset.csv")
        self.filtered_df = self.df.copy()
        self.canvas = None

        self.rows_per_page = 26
        self.current_page = 0

        # Populate all food dropdowns from the same sorted unique list
        unique_foods = sorted(self.df['food'].unique())
        for dropdown in [self.m_breakdownChoice, self.m_comparisonPrimary, self.m_comparisonSecondary]:
            dropdown.Clear()
            dropdown.AppendItems(unique_foods)

        self.range_check = False
        self.level_check = False

        # Widgets shown in the search/table view
        self.search_widgets = [
            self.m_staticText1, self.m_foodSearch, self.m_nutritionRangeCheck,
            self.m_rangeChoice, self.m_rangeMin, self.m_rangeMax,
            self.m_NutritionLevelCheck, self.m_nutritionType, self.m_nutritionLevel,
            self.m_searchButton, self.m_graphSwap, self.m_dataGrid,
            self.m_staticText7, self.m_staticText8, self.m_currentPage,
            self.m_staticText10, self.m_pageCount, self.m_previousPage, self.m_nextPage
        ]

        # Widgets shown in the graphing view
        self.graph_widgets = [
            self.m_staticText4, self.m_breakdownChoice, self.m_barGraph,
            self.m_pieChart, self.m_staticText5, self.m_comparisonPrimary,
            self.m_comparisonSecondary, self.m_compareFoods, self.m_foodSwap
        ]

        self.updateGrid()
        self.Show(True)
        self.Layout()

    def onGraphSwap(self, event):
        """Switch to the graphing view."""
        event.Skip()
        for widget in self.search_widgets:
            widget.Hide()
        for widget in self.graph_widgets:
            widget.Show()
        if self.canvas:
            self.canvas.Show()
        self.GetSizer().Layout()

    def onSearchSwap(self, event):
        """Switch back to the search/table view."""
        event.Skip()
        for widget in self.graph_widgets:
            widget.Hide()
        if self.canvas:
            self.canvas.Hide()
        for widget in self.search_widgets:
            widget.Show()
        self.GetSizer().Layout()

    def tableSearch(self, input_text):
        """Filter the DataFrame by food name, with input validation."""
        special_characters = {
            '@', '_', '!', '#', '$', '%', '^', '&', '*', '(', ')', '<', '>',
            '?', '/', '\\', '|', '}', '{', '~', ':'
        }

        if not isinstance(input_text, str):
            raise ValueError("Search input must be a string")
        if input_text.isdigit():
            raise ValueError("Search input cannot be numeric")
        if any(char in special_characters for char in input_text):
            raise ValueError("No special symbols allowed")

        search_term = input_text.strip()

        if not search_term:
            return self.filtered_df.copy()

        matched_rows = self.filtered_df['food'].str.contains(search_term, case=False, na=False)
        result_df = self.filtered_df[matched_rows].copy()

        if result_df.empty:
            raise ValueError(f"No data found for '{input_text}'")

        # Capitalise matched words if the search term starts with a capital
        if search_term[0].isupper():
            result_df['food'] = result_df['food'].apply(
                lambda x: ' '.join(
                    word.capitalize() if word.lower() in search_term.lower() else word
                    for word in x.split()
                )
            )

        return result_df

    def onSearch(self, event):
        """Handle the search button press."""
        event.Skip()
        self.filtered_df = self.df.copy()
        search_text = self.m_foodSearch.GetValue().strip()

        if search_text:
            self.filtered_df = self.tableSearch(search_text)

        if self.range_check:
            self.filtered_df = self.rangeFilter()

        if self.level_check:
            self.filtered_df = self.levelFilter()

        self.current_page = 0
        self.updateGrid()

    def updateGrid(self):
        """Refresh the data grid for the current page."""
        start_row = self.current_page * self.rows_per_page
        end_row = start_row + self.rows_per_page
        df_to_display = self.filtered_df.iloc[start_row:end_row]

        self.m_dataGrid.ClearGrid()
        self.table = DataTable(df_to_display)
        self.m_dataGrid.SetTable(self.table, takeOwnership=True)
        self.m_dataGrid.AutoSize()

        self.updateButtonStates()
        self.m_currentPage.SetLabel(str(self.current_page + 1))
        self.m_pageCount.SetLabel(str(self.total_pages + 1))
        self.GetSizer().Layout()

    def updateButtonStates(self):
        """Enable or disable pagination buttons based on the current page."""
        self.m_previousPage.Enable(self.current_page > 0)
        self.total_pages = (len(self.filtered_df) - 1) // self.rows_per_page
        self.m_nextPage.Enable(self.current_page < self.total_pages)

    def rangeFilter(self):
        """Filter the DataFrame to rows where a nutrient falls within a given range."""
        min_range = self.m_rangeMin.GetValue().strip()
        max_range = self.m_rangeMax.GetValue().strip()
        nutrition_type = self.m_rangeChoice.GetStringSelection()

        special_characters = {
            '@', '_', '!', '#', '$', '%', '^', '&', '*', '(', ')', '<', '>',
            '?', '/', '\\', '|', '}', '{', '~', ':'
        }

        if not isinstance(nutrition_type, str):
            raise ValueError("Nutrition type must be a string")
        if nutrition_type.isdigit():
            raise ValueError("Nutrition type cannot be numeric")
        if any(char in special_characters for char in nutrition_type):
            raise ValueError("Nutrition type cannot contain symbols")
        if nutrition_type == '':
            raise ValueError("Please select a nutrition type")

        min_ok = False
        max_ok = False

        if min_range:
            try:
                input_min = int(min_range)
                min_ok = True
            except ValueError:
                wx.MessageBox("Please enter a valid integer for the minimum value.", "Invalid Input", wx.OK | wx.ICON_ERROR)
                raise ValueError(f"'{min_range}' is not a valid integer")

        if max_range:
            try:
                input_max = int(max_range)
                max_ok = True
            except ValueError:
                wx.MessageBox("Please enter a valid integer for the maximum value.", "Invalid Input", wx.OK | wx.ICON_ERROR)
                raise ValueError(f"'{max_range}' is not a valid integer")

        if not min_ok and not max_ok:
            wx.MessageBox("Please enter a valid integer for at least one input.", "Invalid Input", wx.OK | wx.ICON_ERROR)
            raise ValueError("Both min and max range inputs are invalid")

        ser_nutrition = self.filtered_df[nutrition_type]

        if min_ok and max_ok:
            mask = ser_nutrition.between(input_min, input_max)
        elif min_ok:
            mask = ser_nutrition >= input_min
        else:
            mask = ser_nutrition <= input_max

        return self.filtered_df[mask]

    def levelFilter(self):
        """Filter the DataFrame by low/medium/high nutrition content level."""
        nutrition_type = self.m_nutritionType.GetStringSelection()
        nutrition_level = self.m_nutritionLevel.GetStringSelection()

        ser_nutrition = self.filtered_df[nutrition_type]
        max_nutrition = ser_nutrition.max()

        if nutrition_level == "Low":
            mask = ser_nutrition < max_nutrition * 0.33
        elif nutrition_level == "Medium":
            mask = ser_nutrition.between(max_nutrition * 0.33, max_nutrition * 0.66)
        elif nutrition_level == "High":
            mask = ser_nutrition > max_nutrition * 0.66
        else:
            return self.filtered_df

        return self.filtered_df[mask]

    def onPlotPie(self, event):
        """Plot a pie chart showing nutrient breakdown for the selected food."""
        event.Skip()
        selected_food = self.m_breakdownChoice.GetStringSelection()

        if not selected_food:
            wx.MessageBox("Please select a food.", "Invalid Input", wx.OK | wx.ICON_ERROR)
            raise ValueError("No food selected.")

        df_food = self.df[self.df['food'] == selected_food]

        if df_food.empty:
            raise ValueError(f"No data found for '{selected_food}'")

        food_data = df_food.iloc[0]
        nutrient_names = self.df.columns[1:]
        food_values = food_data[nutrient_names].tolist()

        total = sum(food_values)
        food_percentages = [(v / total) * 100 for v in food_values]
        legend_labels = [f"{n}: ({p:.3f}%)" for n, p in zip(nutrient_names, food_percentages)]

        colors = plt.cm.viridis(np.linspace(0, 1, len(food_values)))
        fig, ax = plt.subplots(figsize=(6, 6))
        ax.pie(food_values, colors=colors, wedgeprops=dict(edgecolor='white'))
        ax.set_title(f"Nutrient breakdown for {selected_food}", loc='left')
        ax.set_position([0.01, 0.1, 0.4, 0.8])
        plt.legend(legend_labels, title="Nutrient details", loc="center left", bbox_to_anchor=(1, 0.4), ncol=2)

        self._render_canvas(fig)

    def onCompare(self, event):
        """Plot a bar chart comparing nutrients between two selected foods."""
        event.Skip()
        food_1 = self.m_comparisonPrimary.GetStringSelection()
        food_2 = self.m_comparisonSecondary.GetStringSelection()

        if not food_1 or not food_2:
            wx.MessageBox("Please select food for both inputs.", "Invalid Input", wx.OK | wx.ICON_ERROR)
            raise ValueError("Both food items must be selected.")

        df_food1 = self.df[self.df['food'] == food_1]
        df_food2 = self.df[self.df['food'] == food_2]

        if df_food1.empty:
            raise ValueError(f"No data found for '{food_1}'")
        if df_food2.empty:
            raise ValueError(f"No data found for '{food_2}'")

        nutrients = self.df.columns[1:]
        values_1 = df_food1.iloc[0][nutrients].tolist()
        values_2 = df_food2.iloc[0][nutrients].tolist()

        bar_width = 0.35
        x = np.arange(len(nutrients))

        fig, ax = plt.subplots(figsize=(8, 4))
        ax.bar(x, values_1, bar_width, label=food_1, color='blue')
        ax.bar(x + bar_width, values_2, bar_width, label=food_2, color='green')

        ax.set_xlabel('Nutrients')
        ax.set_ylabel('Values')
        ax.set_title(f'Comparison of {food_1} vs {food_2}')
        ax.set_yticks(np.linspace(min(values_1 + values_2), max(values_1 + values_2), 10))
        ax.set_xticks(x + bar_width / 2)
        ax.set_xticklabels(nutrients, rotation=45, ha='right', fontsize=9)
        ax.grid(visible=True, which='both', axis='both')
        ax.legend()
        plt.tight_layout()

        self._render_canvas(fig)

    def onPlotBar(self, event):
        """Plot bar charts showing macro and micro nutrient breakdown for the selected food."""
        event.Skip()
        selected_food = self.m_breakdownChoice.GetStringSelection()

        if not selected_food:
            wx.MessageBox("Please select a food.", "Invalid Input", wx.OK | wx.ICON_ERROR)
            raise ValueError("No food selected.")

        df_food = self.df[self.df['food'] == selected_food]

        if df_food.empty:
            wx.MessageBox(f"No data found for '{selected_food}'.", "Invalid Input", wx.OK | wx.ICON_ERROR)
            raise ValueError(f"No data found for '{selected_food}'")

        food_data = df_food.iloc[0]
        macro_cols = self.df.columns[2:13]
        micro_cols = self.df.columns[[11] + list(range(13, 34))]

        macro_values = food_data[macro_cols].tolist()
        micro_values = food_data[micro_cols].tolist()

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 6))

        ax1.bar(macro_cols, macro_values, color='blue', width=0.2)
        ax1.set_xlabel('Nutritional Components')
        ax1.set_ylabel('Values')
        ax1.set_title(f'Macro Nutrients for {selected_food} Per 100g')
        ax1.set_xticklabels(macro_cols, rotation=45, ha='right')

        ax2.bar(micro_cols, micro_values, color='blue', width=0.2)
        ax2.set_xlabel('Nutritional Components')
        ax2.set_ylabel('Values')
        ax2.set_title(f'Micro Nutrients for {selected_food} Per 100g')
        ax2.set_xticklabels(micro_cols, rotation=45, ha='right', fontsize=8)

        plt.tight_layout()
        self._render_canvas(fig)

    def _render_canvas(self, fig):
        """Destroy any existing canvas and render a new matplotlib figure."""
        if self.canvas:
            self.canvas.Destroy()
        h, w = self.m_panelContent.GetSize()
        fig.set_size_inches(h / fig.get_dpi(), w / fig.get_dpi())
        self.canvas = FigureCanvasWxAgg(self.m_panelContent, -1, fig)
        self.canvas.SetSize((h, w))
        self.Layout()

    def onPrevious(self, event):
        """Go to the previous page of results."""
        event.Skip()
        if self.current_page > 0:
            self.current_page -= 1
            self.updateGrid()

    def onNext(self, event):
        """Go to the next page of results."""
        event.Skip()
        total_pages = (len(self.filtered_df) - 1) // self.rows_per_page
        if self.current_page < total_pages:
            self.current_page += 1
            self.updateGrid()

    def onRangeCheck(self, event):
        """Toggle range filtering on or off."""
        event.Skip()
        self.range_check = self.m_nutritionRangeCheck.GetValue()

    def onLevelCheck(self, event):
        """Toggle level filtering on or off."""
        event.Skip()
        self.level_check = self.m_NutritionLevelCheck.GetValue()


if __name__ == "__main__":
    app = wx.App()
    frame = MyMainFrame()
    app.MainLoop()
