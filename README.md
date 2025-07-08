# Concrete Inventory and Production Tracking System

This is a Python-based desktop application developed using Tkinter to help a concrete paving business manage inventory, production, and sales operations efficiently. The system was built for a real-life company and tailored to address daily operational needs.

## Features

- **Material Inventory Management**: Add, update, and track stock levels of raw materials.
- **Production Recipes**: Define formulas for each product using multiple materials and percentages.
- **Automated Stock Reduction**: Raw materials are automatically deducted based on production formulas.
- **Sales Recording**: Record each sale with product, quantity, and date information.
- **Excel Export**: Save sales, stock, and production data to Excel files for external use.
- **Profit Calculation**: Calculates net profit by subtracting raw material costs and applying 20% VAT and 21% platform commission.
- **Scrap and Return Tracking**: Logs defective or returned products.
- **Critical Stock Warnings**: Alerts when material stock falls below a defined threshold.
- **Input Validation**: Turkish character warnings shown in all input screens.

## Technologies Used

- Python
- Tkinter (GUI)
- Pandas (Data management)
- OpenPyXL (Excel file export)
- Matplotlib (Data visualization - optional)
- FPDF2 (PDF invoice generation - upcoming)

## Folder Structure

satislar/
│
├── beton_takip.py # Main application file
├── *.xlsx # Excel files for sales, stock, production, etc.
├── README.md # Project documentation
├── requirements.txt # Dependencies (if needed)
└── .gitignore # File exclusion rules


## Future Improvements

- PDF invoice generation (under development)
- User authentication system
- Dashboard with charts and statistics
- Mobile-friendly or web-based version

## Author

Reyyan Gürer – [github.com/reygurer](https://github.com/reygurer)

This project was developed as part of a real-world solution for a family-owned concrete paving company.
