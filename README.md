# AI Powered Data Insights

## Overview

The AI-Driven Report Generator is a Streamlit-based web application that allows users to analyze datasets, generate AI-powered insights, ask natural language questions, and visualize data using DeepSeek AI.

## Features

**1.** Upload CSV/Excel files or connect to an SQLite database

**2.** Generate statistical summaries of the dataset

**3.** Get AI-generated insights using DeepSeek API

**4.** Ask AI-driven questions about the dataset

**5.** Visualize data with interactive charts (histograms, KDE plots, etc.)

## Technologies Used

**1.** Streamlit – Web interface

**2.** Pandas – Data processing

**3.** Matplotlib & Seaborn – Data visualization

**4.** SQLite3 – Database connection

**5.** DeepSeek API – AI-powered insights

**6.** Requests – API communication

## Installation

**1. Clone the Repository**

git https://github.com/Dipti-24/AI_Powered_Data_Insights.git

cd AI_Powered_Data_Insights


**2. Install Dependencies**

pip install -r requirements.txt


**3. Configure API Key**

+ Create a config.py file in the project directory.

+ Add your DeepSeek API Key

**4. Run the Streamlit App**

### Using the App

- Choose Data Source: Upload a CSV/Excel file or connect to an SQLite database.

- Preview Data: The first few rows of the dataset will be displayed.

- Generate Insights: The AI model analyzes the dataset and provides key observations.

- Ask a Question: Enter a natural language query to get AI-generated responses.

- Visualize Data: Select a column to generate plots (histograms, KDE plots, etc.).

## Future Enhancements

+ Integration with local LLMs like Ollama to reduce API dependency

+ Advanced visualizations like correlation heatmaps and scatter plots

## License

This project is open-source and available under the [MIT License]().

## Contact

For issues or suggestions, please open an issue on GitHub or mail me at mishradipti2402@gmail.com
