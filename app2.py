from flask import Flask, jsonify
import requests
import re

app = Flask(__name__)

def get_time_stories():
    url = 'https://time.com'
    response = requests.get(url)
    if response.status_code == 200:
        html_content = response.text
        # Find the latest stories using regex
        pattern = r'<a href="(.*?)".*?data-tim=".*?">(.*?)<\/a>'
        matches = re.findall(pattern, html_content)
        
        stories = []
        for match in matches[:6]:
            title = match[1].strip()
            link = match[0].strip()
            stories.append({'title': title, 'link': link})

        return stories
    else:
        print('Failed to fetch data from Time.com')
        return None

@app.route('/getTimeStories', methods=['GET'])
def get_latest_stories():
    time_stories = get_time_stories()
    if time_stories:
        return jsonify(time_stories)
    else:
        return jsonify({'error': 'Failed to fetch stories from Time.com'}), 500

if __name__ == '__main__':
    app.run(debug=True)
