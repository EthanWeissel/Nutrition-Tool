# 🥦 Food Nutrition Information Tool

A desktop application for searching, filtering, and visualising nutritional data across hundreds of food items. Built with Python using wxPython for the GUI and Matplotlib for data visualisation.

---

## Features

- **Food Search** — Search for any food item by name with real-time filtering
- **Nutrition Range Filter** — Filter results by setting a min/max value for any nutrient
- **Nutrition Level Filter** — Filter foods by low, medium, or high content of a selected nutrient
- **Bar Charts** — Visualise macro and micro nutrient breakdowns for any food item
- **Pie Charts** — See the proportional nutrient composition of any food
- **Food Comparison** — Compare the full nutritional profile of two foods side by side
- **Paginated Results** — Browse through hundreds of food entries across multiple pages

---

## Requirements

- Python 3.x
- wxPython
- pandas
- matplotlib
- numpy

---

## Installation

**1. Clone the repository**
```bash
git clone https://github.com/EthanWeissel/Nutrition-Tool
cd Nutrition-Tool
```

**2. Install dependencies**
```bash
pip install wxPython pandas matplotlib numpy
```

---

## Usage

```bash
python3 code.py
```

Make sure `Food_Nutrition_Dataset.csv` is in the same directory as `code.py` before running.

---

## Project Structure

```
Nutrition-Tool/
├── code.py                    # Main application logic
├── GUI.py                     # Auto-generated wxPython GUI layout
├── Food_Nutrition_Dataset.csv # Nutritional dataset
└── README.md
```

---

## Dataset

The dataset contains nutritional information per 100g for a wide range of food items, covering macronutrients (fat, protein, carbohydrates) as well as micronutrients (vitamins and minerals).

---

## Built With

- [wxPython](https://wxpython.org/) — GUI framework
- [pandas](https://pandas.pydata.org/) — Data manipulation
- [Matplotlib](https://matplotlib.org/) — Data visualisation
- [NumPy](https://numpy.org/) — Numerical operations
