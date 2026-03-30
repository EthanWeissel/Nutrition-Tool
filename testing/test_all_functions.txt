import pytest
import pandas as pd
from all_functions import load_file
from all_functions import MyMainFrame
from unittest.mock import Mock

#Function 1


def test_valid_load_file():

    test_input = "../Food_Nutrition_Dataset.csv"

    result = load_file(test_input)

    expected_result = load_file("../Food_Nutrition_Dataset.csv")

    pd.testing.assert_frame_equal(result, expected_result)

def test_invalid_load_file():
    with pytest.raises(FileNotFoundError) as exc_info:
        test_input = "nonexistent_file.csv"
        result = load_file(test_input)
    assert exc_info.type is FileNotFoundError


#Function 2

def test_tableSearch_valid_input():
    # Setup
    frame = MyMainFrame()  # Initialize the frame
    test_input_1 = "apple"  # Valid food item
    test_input_2 = ""       #no input
    test_input_3 = "Apple"  #capitalised valid food item
    test_input_4 = "           cooking wine            "

    # Execution
    result_1 = frame.tableSearch(test_input_1)
    result_2 = frame.tableSearch(test_input_2)
    result_3 = frame.tableSearch(test_input_3)
    result_4 = frame.tableSearch(test_input_4)

    # Expected result: dataframe returned will contain 30 results
    expected_result_1 = 30
    # Expected result: dataframe returned will contain apple data
    expected_result_2 = "apple"
    # Expected result: dataframe returned will contain pineapple data
    expected_result_3 = "pineapple"
    # Expected result: dataframe returned will match unfiltered dataframe
    expected_result_4 = frame.df
    # Expected result: dataframe returned will contain capitalised food names
    expected_result_5 = "Apple"
    # Expected result: dataframe returned will contain cooking wine data
    expected_result_6 = "cooking wine"


    # Assertion
    assert len(result_1) == expected_result_1, f"expected {expected_result_1} results, but got {len(result_1)}"
    assert expected_result_2 in result_1["food"].values
    assert expected_result_3 in result_1["food"].values
    assert len(result_2) == len(expected_result_4), f"expected {len(expected_result_4)} results, but got {len(result_2)}"
    assert expected_result_5 in result_3["food"].values
    assert expected_result_6 in result_4["food"].values

def test_tableSearch_invalid_input():
    frame = MyMainFrame()

    with pytest.raises(ValueError) as exc_info:
        input = "123"
        result = frame.tableSearch(input)
    assert exc_info.type is ValueError

    with pytest.raises(ValueError) as exc_info:
        result = frame.tableSearch("kerfluffle")
    assert exc_info.type is ValueError

    with pytest.raises(ValueError) as exc_info:
        result = frame.tableSearch("&*^(*()")
    assert exc_info.type is ValueError

    with pytest.raises(ValueError) as exc_info:
        result = frame.tableSearch(["apple", "pineapple"])
    assert exc_info.type is ValueError

    with pytest.raises(ValueError) as exc_info:
        result = frame.tableSearch("Kerfluffle")
    assert exc_info.type is ValueError

#function 2

def test_onPlotBar_valid_input():
    # Setup
    frame = MyMainFrame()  # Initialize the frame
    input_data = "apple"  # Valid food item

    # Execution
    result = frame.onPlotBar(input_data)

    # Expected result: Bar chart showing nutritional values of "apple"
    expected_columns = ["Nutrient", "Value"]  # Example column names for the plot data

    # Assertion
    assert result is not None, "Expected a bar chart, but got None."
    assert all(col in result.columns for col in
               expected_columns), f"Expected columns {expected_columns}, but got {result.columns}"


def test_onPlotBar_invalid_input():
    # Setup
    frame = MyMainFrame()  # Initialize the frame
    input_data = "kerfluffle"  # Invalid food item

    # Execution and Assertion
    with pytest.raises(ValueError) as exc_info:
        frame.onPlotBar(input_data)

    # Expected result: Raise ValueError or similar error
    assert str(
        exc_info.value) == "No data found for 'kerfluffle'", f"Expected ValueError for invalid input, but got {exc_info.value}"

    input_data = ""

    # Execution and Assertion
    with pytest.raises(ValueError) as exc_info:
        frame.onPlotBar(input_data)

    # Expected result: Raise ValueError or similar error
    assert str(
        exc_info.value) == "No Food Selected.", f"Expected ValueError for invalid input, but got {exc_info.value}"




#Function 3

def test_onPlotPie_valid_input():
    # Setup
    frame = MyMainFrame()  # Initialize the frame
    input_data = "banana"  # Valid food item

    # Execution
    result = frame.onPlotPie(input_data)

    # Expected result: Pie chart showing nutritional breakdown of "banana"
    expected_columns = ["Nutrient", "Value"]  # Example column names for the plot data

    # Assertion
    assert result is not None, "Expected a bar chart, but got None."
    assert all(col in result.columns for col in
               expected_columns), f"Expected columns {expected_columns}, but got {result.columns}"


def test_onPlotPie_invalid_input():
    # Setup
    frame = MyMainFrame()  # Initialize the frame
    input_data = "unknown_food"  # Invalid food item

    # Execution and Assertion
    with pytest.raises(ValueError) as exc_info:
        frame.onPlotPie(input_data)

    # Expected result: Raise ValueError or appropriate error
    assert str(
        exc_info.value) == "No data found for 'unknown_food'", f"Expected ValueError for invalid input, but got {exc_info.value}"

    input_data = ""

    # Execution and Assertion
    with pytest.raises(ValueError) as exc_info:
        frame.onPlotPie(input_data)

    # Expected result: Raise ValueError or similar error
    assert str(
        exc_info.value) == "No Food Selected.", f"Expected ValueError for invalid input, but got {exc_info.value}"


#Function 4
def test_levelFilter_valid_input():
    # Test 1: Valid Low input
    frame = MyMainFrame()  # Initialize the frame
    frame.filtered_df = pd.DataFrame({
        'Sugars': [100, 200, 300, 400, 500],
    })
    frame.m_nutritionType = Mock()
    frame.m_nutritionType.GetStringSelection.return_value = 'Sugars'
    frame.m_nutritionLevel = Mock()
    frame.m_nutritionLevel.GetStringSelection.return_value = 'Low'

    expected_df_low = frame.filtered_df[frame.filtered_df['Sugars'] < 500 * 0.33]
    result_low = frame.levelFilter()
    pd.testing.assert_frame_equal(result_low, expected_df_low)

    # Test 2: Valid Medium input
    frame.m_nutritionLevel.GetStringSelection.return_value = 'Medium'
    expected_df_medium = frame.filtered_df[
        (frame.filtered_df['Sugars'] >= 500 * 0.33) & (frame.filtered_df['Sugars'] <= 500 * 0.66)
        ]
    result_medium = frame.levelFilter()
    pd.testing.assert_frame_equal(result_medium, expected_df_medium)

    # Test 3: Valid High input
    frame.m_nutritionLevel.GetStringSelection.return_value = 'High'
    expected_df_high = frame.filtered_df[frame.filtered_df['Sugars'] > 500 * 0.66]
    result_high = frame.levelFilter()
    pd.testing.assert_frame_equal(result_high, expected_df_high)

def test_levelFilter_invalid_input():
    frame = MyMainFrame()
    frame.filtered_df = pd.DataFrame({
        'Sugars': [10, 250, 300, 400, 500],
    })

    # test 1 - both type and level are invalid
    frame.m_nutritionType = Mock()
    frame.m_nutritionType.GetStringSelection.return_value = 'InvalidType'
    frame.m_nutritionLevel = Mock()
    frame.m_nutritionLevel.GetStringSelection.return_value = 'Invalid'

    with pytest.raises(ValueError) as exc_info:
        frame.levelFilter()

    # error message for both invalid options
    assert str(exc_info.value) == "Invalid nutrition type selected: InvalidType and Invalid nutrition level selected: Invalid", \
        f"Unexpected exception: {exc_info.value}"

    # the type is wrong but the level is right
    frame.m_nutritionType.GetStringSelection.return_value = 'InvalidType'
    frame.m_nutritionLevel.GetStringSelection.return_value = 'Low'

    with pytest.raises(ValueError) as exc_info:
        frame.levelFilter()

    # error message for invalid type
    assert str(exc_info.value) == "Invalid nutrition type selected: InvalidType", \
        f"Unexpected exception: {exc_info.value}"

    # type is correct but the level is wrong
    frame.m_nutritionType.GetStringSelection.return_value = 'Sugars'
    frame.m_nutritionLevel.GetStringSelection.return_value = 'Invalid'

    with pytest.raises(ValueError) as exc_info:
        frame.levelFilter()

    # error message for only invalid level
    assert str(exc_info.value) == "Invalid nutrition level selected: Invalid", \
        f"Unexpected exception: {exc_info.value}"

def test_onCompare_valid_input():
    # Setup
    frame = MyMainFrame()  # Initialize the frame
    input_data1 = "apple"  # First valid food item
    input_data2 = "banana"  # Second valid food item

    # Execution
    result = frame.onCompare(input_data1, input_data2)

    # Expected result: Comparison chart showing nutritional values of both "apple" and "banana"
    expected_columns = ["Nutrient", "Apple Value", "Banana Value"]  # Example columns for the comparison chart

    # Assertion
    assert result is not None, "Expected a comparison chart, but got None."
    assert all(col in result.columns for col in
               expected_columns), f"Expected columns {expected_columns}, but got {result.columns}"


def test_onCompare_invalid_input():
    # Setup
    frame = MyMainFrame()  # Initialize the frame
    input_data1 = "kerfluffle"  # Invalid food item
    input_data2 = "bacon egg cheese smoothie"  # Another invalid food item

    # Execution and Assertion
    with pytest.raises(ValueError) as exc_info:
        frame.onCompare(input_data1, input_data2)

    # Expected result: Raise ValueError or appropriate error
    assert str(
        exc_info.value) == f"No data found for '{input_data1}' or '{input_data2}'", f"Expected ValueError for invalid input, but got {exc_info.value}"

    input_data1 = ""  # Invalid food item
    input_data2 = ""  # Another invalid food item

    # Execution and Assertion
    with pytest.raises(ValueError) as exc_info:
        frame.onCompare(input_data1, input_data2)

    # Expected result: Raise ValueError or appropriate error
    assert str(
        exc_info.value) == f"Both food items not selected.", f"Expected ValueError for invalid input, but got {exc_info.value}"

    input_data1 = "kerfluffle"  # Invalid food item
    input_data2 = "apple"  # invalid food item

    # Execution and Assertion
    with pytest.raises(ValueError) as exc_info:
        frame.onCompare(input_data1, input_data2)

    # Expected result: Raise ValueError or appropriate error
    assert str(
        exc_info.value) == f"No data found for '{input_data1}'", f"Expected ValueError for invalid input, but got {exc_info.value}"

    input_data1 = "apple"  # valid food item
    input_data2 = "kerfluffle"  # invalid food item

    # Execution and Assertion
    with pytest.raises(ValueError) as exc_info:
        frame.onCompare(input_data1, input_data2)

    # Expected result: Raise ValueError or appropriate error
    assert str(
        exc_info.value) == f"No data found for '{input_data2}'", f"Expected ValueError for invalid input, but got {exc_info.value}"

#Function 5

def test_rangeFilter_valid_input():
    # Setup
    frame = MyMainFrame()  # Initialize the frame
    test_1_input_1 = "2"  # Valid minimum input
    test_1_input_2 = "3" #valid maximum input
    test_1_input_3 = "Sugars" #valid nutriton type

    # Execution
    result_1 = frame.rangeFilter(test_1_input_1, test_1_input_2, test_1_input_3)

    # Expected result: Comparison chart showing nutritional values of both "apple" and "banana"
    expected_result_1 = 102  # Example columns for the comparison chart

    # Assertion
    assert result_1 is not None, "Expected a dataframe chart, but got None."
    assert len(result_1) == expected_result_1, f"expected {expected_result_1} results, but got {len(result_1)}"

    # Setup
    frame = MyMainFrame()  # Initialize the frame
    test_2_input_1 = ""  # Valid minimum input
    test_2_input_2 = "3"  # valid maximum input
    test_2_input_3 = "Sugars"  # valid nutriton type

    # Execution
    result_2 = frame.rangeFilter(test_2_input_1, test_2_input_2, test_2_input_3)

    # Expected result: Comparison chart showing nutritional values of both "apple" and "banana"
    expected_result_2 = 1777  # Example columns for the comparison chart

    # Assertion
    assert result_2 is not None, "Expected a dataframe chart, but got None."
    assert len(result_2) == expected_result_2, f"expected {expected_result_2} results, but got {len(result_2)}"

    # Initialize the frame
    test_3_input_1 = "3"  # Valid minimum input
    test_3_input_2 = ""  # valid maximum input
    test_3_input_3 = "Sugars"  # valid nutrition type

    # Execution
    result_3 = frame.rangeFilter(test_3_input_1, test_3_input_2, test_3_input_3)

    # Expected result: Comparison chart showing nutritional values of both "apple" and "banana"
    expected_result_3 = 627  # Example columns for the comparison chart

    # Assertion
    assert result_2 is not None, "Expected a dataframe chart, but got None."
    assert len(result_3) == expected_result_3, f"expected {expected_result_3} results, but got {len(result_3)}"

def test_rangeFilter_invalid_input():
    frame = MyMainFrame()

    with pytest.raises(ValueError) as exc_info:
        input_1 = "strawberries"
        input_2 = "123"
        input_3 = "Sugars"
        result = frame.rangeFilter(input_1, input_2, input_3)
    assert exc_info.type is ValueError

    with pytest.raises(ValueError) as exc_info:
        input_1 = "123"
        input_2 = "strawberries"
        input_3 = "Sugars"
        result = frame.rangeFilter(input_1, input_2, input_3)
    assert exc_info.type is ValueError

    with pytest.raises(ValueError) as exc_info:
        input_1 = ""
        input_2 = ""
        input_3 = "Sugars"
        result = frame.rangeFilter(input_1, input_2, input_3)
    assert exc_info.type is ValueError

    with pytest.raises(ValueError) as exc_info:
        input_1 = "1"
        input_2 = "2"
        input_3 = "123"
        result = frame.rangeFilter(input_1, input_2, input_3)
    assert exc_info.type is ValueError

    with pytest.raises(ValueError) as exc_info:
        input_1 = "1"
        input_2 = "2"
        input_3 = ""
        result = frame.rangeFilter(input_1, input_2, input_3)
    assert exc_info.type is ValueError

    with pytest.raises(ValueError) as exc_info:
        input_1 = "1"
        input_2 = "2"
        input_3 = "Sug@rs"
        result = frame.rangeFilter(input_1, input_2, input_3)
    assert exc_info.type is ValueError

    with pytest.raises(ValueError) as exc_info:
        input_1 = "1"
        input_2 = "2"
        input_3 = 123
        result = frame.rangeFilter(input_1, input_2, input_3)
    assert exc_info.type is ValueError
