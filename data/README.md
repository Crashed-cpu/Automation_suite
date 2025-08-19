# Data Directory

This directory is used for storing application data, including:

## 📂 Directory Structure

- `csv/`: Contains CSV files used for bulk operations
  - `contacts.csv`: Default contact list for bulk messaging
  - `results/`: Directory for exported data and reports

## 📝 Usage

### For Bulk Operations
1. Prepare your CSV files with the required columns
2. Place them in the appropriate subdirectory
3. Reference them in the application interface

### File Naming Convention
- Use lowercase with underscores (e.g., `user_data.csv`)
- Include a timestamp for generated files (e.g., `report_20230809.csv`)

## 🔒 Security Notes

- Never commit sensitive data to version control
- Add sensitive files to `.gitignore`
- Ensure proper file permissions are set
