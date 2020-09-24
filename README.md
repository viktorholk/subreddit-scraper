# Subreddit Scraper
📒 Scrape multiple subreddits and store them in a JSON format<br />
🔖 Edit the posts with the built-in editor

## How to use
# Scraper
Clone the repository on your computer and open up a terminal.
Execute the program with ``python app.py``, this will scrape the subreddits in the list of the source code.<br /> Feel free to change these subreddits to whatever.<br />
You can also type ``python app.py [count]`` (example ``python app 15``) - This will scrape 15 posts in each of the subreddits and store them in the json.
# Editor
To edit all the files you just scraped type ``python app -e`` pr ``python app --editor`` to open the editor.
<br />
![image of editor](https://i.imgur.com/qoKEhRR.png)
Here you can press SPACE to edit the content of the post, blacklist it with ESC which will remove it and prevent appending on other scrapes, U to open the url of the body (if it's a url) and Q to quit the editor.
