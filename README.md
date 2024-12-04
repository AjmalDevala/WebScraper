# Web Scraper to CSV

## 📌 Project Overview

This Python-based web scraping tool allows you to extract data from web pages and save it directly to a CSV file. The scraper is designed to be flexible, handling various HTML structures and capturing key elements like images, links, headings, and section context.

## ✨ Features

- 🌐 Fetch webpage content using `requests`
- 🍲 Parse HTML with `BeautifulSoup`
- 📊 Extract multiple data points:
  - Image sources
  - Hyperlinks
  - Headings
  - Section context
- 💾 Save data to CSV, preserving duplicates

## 🚀 Installation

```bash
# Clone the repository
git clone https://github.com/AjmalDevala/WebScraper.git

# Navigate to project directory
cd WebScraper

# Install required dependencies
pip install requests beautifulsoup4
```

## 🛠 Usage

```python
# Customize the URL and output file
url = "https://www.example.com/target-page"
output_csv = "scraped_data.csv"

scraper = WebScraperToCSV(url, output_csv)
scraper.run()
```

## 📦 Dependencies

- `requests`
- `beautifulsoup4`
- `csv` (built-in)

## 👤 Author

**Ajmal Devala**

## 🔗 Connect With Me
[![LinkedIn](https://img.shields.io/badge/LinkedIn-blue?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/ajmal-devala/)
[![GitHub](https://img.shields.io/badge/GitHub-black?style=for-the-badge&logo=github&logoColor=white)](https://github.com/AjmalDevala)
[![Email](https://img.shields.io/badge/Email-D14836?style=for-the-badge&logo=gmail&logoColor=white)](mailto:ajmaldevala@gmail.com)

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check [issues page](https://github.com/YourUsername/WebScraperToCSV/issues).

## 📝 License

This project is [MIT](LICENSE) licensed.
