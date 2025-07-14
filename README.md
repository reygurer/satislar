# Concrete Inventory and Production Tracking System

This is a Python-based desktop application developed using Tkinter to help a concrete paving business manage inventory, production, and sales operations efficiently. The system was built for a real-life company and tailored to address daily operational needs.

## Features

- **Material Inventory Management**: Add, update, and track stock levels of raw materials.
- **Production Recipes**: Define formulas for each product using multiple materials and percentages.
- **Automated Stock Reduction**: Raw materials are automatically deducted based on production formulas during production entries.
- **Sales Recording**: Record each sale with product, quantity, and date information.
- **Excel Integration**: Save and update sales, stock, and production data in Excel format for easy access and editing.
- **Profit Calculation**: Automatically calculates net profit by subtracting raw material costs and applying 20% VAT.
- **Scrap and Return Tracking**: Log returned or defective products separately.
- **Separate Income and Expense Tracking**: Maintain independent records for quarry and concrete business units.
- **Input Validation**: Warns users when Turkish characters are used in restricted input fields.

## Technologies Used

- Python
- Tkinter (GUI)
- Pandas (Data management)
- OpenPyXL (Excel file handling)
- Matplotlib (Optional: Data visualization)

## Folder Structure

satislar/
├── beton_takip.py # Main application file
├── satislar.xlsx # Sales data
├── alislar.xlsx # Purchase records
├── gelir_gider_beton.xlsx # Concrete income and expenses
├── gelir_gider_tas.xlsx # Quarry income and expenses
├── urunler.xlsx # Recipe definitions
├── README.md # Project documentation
├── requirements.txt # Optional: dependencies list
└── .gitignore # File exclusion rules


## Future Improvements

- PDF invoice generation
- User authentication
- Dashboard with summary statistics and charts
- Web or mobile-based interface

## Author

**Reyyan Gürer** – [github.com/reygurer](https://github.com/reygurer)

This project was developed as a practical tool for managing operations in a family-owned concrete paving company.
