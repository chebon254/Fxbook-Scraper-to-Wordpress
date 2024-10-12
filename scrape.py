from selenium import webdriver
from bs4 import BeautifulSoup
import time
from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods.posts import NewPost

# Initialize the WebDriver
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # Run in headless mode
driver = webdriver.Chrome(options=options)

# Define the URL to scrape
url = 'https://www.myfxbook.com/members/KP100/c-100k/9333268'
driver.get(url)

# Wait for dynamic content to load
time.sleep(5)

# Inject JavaScript to hide specific elements
driver.execute_script("""
    // Hide specific elements
    var elements = [
        '.page-wrapper-top',
        '.toolbar-container',
        '#page-footer-section',
        '#brokerBottomContainer'
    ];
    elements.forEach(function(selector) {
        var element = document.querySelector(selector);
        if (element) {
            element.style.display = 'none';
            element.style.setProperty('display', 'none', 'important');  // Ensure !important is used
        }
    });
""")


# Execute JavaScript to trigger tabs (if necessary)
# Example for Bootstrap tabs:
driver.execute_script("document.querySelector('a[data-toggle=\"tab\"]').click();")

# Get the page source after JavaScript execution
html = driver.page_source

# Close the driver
driver.quit()

# Parse the page with BeautifulSoup
soup = BeautifulSoup(html, 'html.parser')

# Optionally, save the HTML to a file for later use
with open("scraped_page.html", "w") as file:
    file.write(str(soup))

# WordPress setup
wp = Client('https://affiliatepro.website/xmlrpc.php', 'kelvinchebon90@gmail.com', '@?Kelvin11468')

# Create a new post with the scraped HTML
post = WordPressPost()
post.title = "Scraped MyFXBook Content"
with open("scraped_page.html", "r") as file:
    post.content = file.read()

# Set post status to publish (or draft)
post.post_status = 'publish'

# Upload post to WordPress
wp.call(NewPost(post))
