# Advanced BMI Calculator (Python GUI)

A Python-based Body Mass Index (BMI) calculator application featuring a modern Tkinter GUI interface, user profiles, persistent data storage, and BMI history visualization.

## Features

- **User Login:** Enter your username to manage BMI history separately for each user.
- **Input Validation:** Input your weight (kg) and height (m) with built-in checks for sensible values.
- **BMI Calculation:** Instantly calculates your BMI and assigns a health category (Underweight, Normal, Overweight, Obese) with distinct colors.
- **Persistent History:** Every calculation is stored in an SQLite database and associated with your profile.
- **History Visualization:** View your BMI progress over time in a convenient line graph (using Matplotlib).
- **Graceful Error Handling:** Clear error and info messages ensure a smooth experience.

## Requirements

- Python 3.x
- [matplotlib](https://matplotlib.org/)
- Tkinter and sqlite3 (part of Python standard library)

Install dependencies:

pip install matplotlib

text

## How to Run

1. **Download the project files** into a folder.
2. Make sure you have Python 3 and required packages.
3. Run the application from your command line or terminal:

    ```
    python advanced_bmi_calculator.py
    ```

## Usage

1. Launch the program. Enter a username to begin (creates a new profile if needed).
2. Enter your weight and height, then click **Calculate BMI**.
3. The app will show your BMI score and health category in a color-coded message.
4. Click **Show BMI History** to see your results over time visualized as a graph.
5. Your data is saved automatically between sessions.

## Project Structure

- **advanced_bmi_calculator.py** — Main application source code.
- **bmi_app.db** — SQLite database file automatically created and managed by the app.
- **requirements.txt** — List of Python dependencies.

## Customization Ideas

- Add password protection for login.
- Enable data export (CSV, PDF).
- Support alternate units (lbs/inches).
- Improve history chart (e.g., average lines, goal weight).

## License

Free for personal or educational use.