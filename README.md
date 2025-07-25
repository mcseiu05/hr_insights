# 📊 HR Insights Dashboard

**HR Insights Dashboard** is an interactive Streamlit-based application designed for analyzing employee leave patterns and payroll summaries. Tailored for construction management ERP contexts, this tool empowers HR professionals and top-level management to derive actionable workforce insights and make data-driven decisions.

---

## ✨ Features

* **Data Integration:** Seamlessly integrates leave and payroll data from CSV files.
* **Visual Summaries:** Provides clear visual summaries of total leaves, unplanned leaves, and key payroll metrics.
* **Dynamic Filtering:** Allows filtering of data by specific projects and salary sessions for targeted analysis.
* **Key Employee Insights:** Highlights critical employee patterns to support informed management decisions.
* **Intuitive Charts:** Presents data through easy-to-understand charts for quick comprehension of workforce trends.

---

## 🚀 Getting Started

Follow these steps to set up and run the HR Insights Dashboard on your local machine.

### Prerequisites

Ensure you have **Python 3.8 or higher** installed.

### Installation

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/mcseiu05/hr_insights.git
    cd hr_insights
    ```

2.  **Create and activate a virtual environment On Windows:**
    It's highly recommended to use a virtual environment to manage project dependencies.

    ```bash
    python -m venv venv
    ```

    * ****
        ```bash
        .\venv\Scripts\activate
        ```

3.  **Install the required packages:**

    ```bash
    pip install -r requirements.txt
    ```

### Running the App

With your virtual environment activated, run the Streamlit application:

```bash
streamlit run app.py
