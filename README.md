# Entry Level IT Job Finder

This project is a web application designed to help users find entry-level IT jobs in a specified location. The app is powered by a Python backend that scrapes Indeed for job listings and a simple HTML front-end that allows users to interact with the app through a clean, modern interface.

## Features

- **Job Search by Location**: Users can enter a location to search for available entry-level IT jobs in that area.
- **Modern User Interface**: The front-end uses a clean, responsive design to display job listings, making it easy to navigate.
- **Job Details**: For each job listing, users can view the job title, company, location, summary, and a link to apply.

## Technologies Used

- **HTML, CSS, JavaScript**: Used for the front-end interface.
- **Flask**: Used to create a local server for handling requests and executing the Python scraping script.
- **Python**: The backend uses Python and Selenium to scrape job listings from Indeed.

## Installation

To run this project locally, you will need Python and Node.js installed. Follow these steps to set up the project:

1. **Clone the Repository**
   ```bash
   git clone https://github.com/your-username/entry-level-it-job-finder.git
   cd entry-level-it-job-finder
   ```

2. **Install Python Dependencies**
   Ensure you have Python installed and then install the necessary Python libraries:
   ```bash
   pip install flask selenium
   ```

3. **Install ChromeDriver**
   Selenium requires ChromeDriver to interact with the web browser. Download ChromeDriver and add it to your PATH.

4. **Run the Flask Server**
   Start the Flask server to handle requests from the front-end:
   ```bash
   python server.py
   ```

5. **Open the HTML File**
   Open the `index.html` file in your browser to use the application.

## Usage

1. Click the **Search Jobs** button.
2. Enter the desired location (e.g., "Charlotte").
3. The app will display a list of job titles along with details like the company, location, and a link to apply.

## Notes

- Make sure the Flask server is running before using the web app.
- The web scraper is designed to work with Indeed and might require updates if the site's structure changes.

## Future Enhancements

- **More Job Platforms**: Extend the scraper to gather listings from other job boards.
- **Pagination Handling**: Add support for scraping multiple pages of job listings.
- **Deployment**: Deploy the application online so that it can be used without local setup.

## License

This project is licensed under the MIT License. Feel free to use and modify it as needed.

## Contributions

Contributions are welcome! If you have suggestions or want to add features, feel free to submit a pull request or open an issue.

