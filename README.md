# AI Powered Data Insights

## Overview

The AI-Driven data insights is a Streamlit-based web application that allows users to upload datasets, clean data, generate AI-powered insights, and visualize data using DeepSeek API. This tool is designed for data analysts and business professionals to quickly analyze and interpret their datasets.

## Features

**1.** Upload CSV/Excel files or connect to an SQLite database

**2.** Remove null values and duplicate entries with one click.

**3.** Generate statistical summaries of the dataset

**4.** Get AI-generated insights using DeepSeek API

**5.** Ask AI-driven questions about the dataset

**6.** Visualize data with interactive charts (histograms, correlation heatmaps.)

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

- Generate Insights: The AI model analyzes the dataset and provides key observations and click on Clean Data to remove null values and duplicates.

- Ask a Question: Enter a natural language query to get AI-generated responses.

- Visualize Data: Select a column to generate plots (histograms, correlation heatmaps).

## Future Enhancements

+ Integration with local LLMs like Ollama to reduce API dependency

+ Export generated AI Insights as PDF/Excel

## License

This project is open-source and available under the [MIT License]().

## Contact

For issues or suggestions, please open an issue on GitHub or mail me at mishradipti2402@gmail.com
