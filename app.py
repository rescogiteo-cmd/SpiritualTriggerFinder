from flask import Flask, render_template, request, jsonify, send_file
import praw
import time
import os
import csv
import json
from collections import Counter
from datetime import datetime
import threading

app = Flask(__name__)

REDDIT_CLIENT_ID = os.environ.get('REDDIT_CLIENT_ID')
REDDIT_CLIENT_SECRET = os.environ.get('REDDIT_CLIENT_SECRET')

EMOTIONAL_PATTERNS = {
    'frustration': ['frustrated', 'stuck', 'cannot', 'struggling', 'difficult', 'hard', 'trying', 'failed', 'cant', "can't"],
    'confusion': ['confused', "don't understand", 'lost', 'uncertain', 'question', 'what does', 'how to', 'not sure'],
    'fear': ['afraid', 'scared', 'worried', 'anxious', 'fear', 'nervous', 'panic'],
    'loneliness': ['alone', 'lonely', 'isolated', 'no one understands', 'by myself', 'no friends'],
    'insecurity': ['not good enough', 'inadequate', 'imposter', 'doubt', 'not sure if', 'worthless'],
    'disappointment': ['disappointed', 'let down', 'failed', 'not working', 'waste', 'regret']
}

analysis_status = {
    'running': False,
    'progress': 0,
    'total': 0,
    'current_community': '',
    'message': ''
}

latest_results = []

def find_emotional_content(text):
    if not text or text == '[removed]' or text == '[deleted]':
        return []
    
    text_lower = text.lower()
    found_emotions = []
    
    for emotion, words in EMOTIONAL_PATTERNS.items():
        for word in words:
            if word in text_lower:
                found_emotions.append(emotion)
                break
    
    return found_emotions

def export_to_csv(data, filename='exports/spiritual_posts.csv'):
    if not data:
        return
    
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['post_id', 'community', 'title', 'content', 'url', 'flair', 
                     'created_date', 'upvotes', 'num_comments', 'author', 
                     'emotions', 'comment_count', 'top_comment_1', 'top_comment_2', 'top_comment_3']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for post in data:
            row = {
                'post_id': post['post_id'],
                'community': post['community'],
                'title': post['title'],
                'content': post['content'],
                'url': post['url'],
                'flair': post['flair'],
                'created_date': post['created_date'],
                'upvotes': post['upvotes'],
                'num_comments': post['num_comments'],
                'author': post['author'],
                'emotions': ', '.join(post['emotions']),
                'comment_count': len(post['top_comments'])
            }
            
            for i, comment in enumerate(post['top_comments'][:3], 1):
                row[f'top_comment_{i}'] = comment['text']
            
            writer.writerow(row)

def export_to_json(data, filename='exports/spiritual_posts.json'):
    if not data:
        return
    
    with open(filename, 'w', encoding='utf-8') as jsonfile:
        json.dump(data, jsonfile, indent=2, ensure_ascii=False)

def export_to_text(data, filename='exports/spiritual_posts_for_chatgpt.txt'):
    if not data:
        return
    
    with open(filename, 'w', encoding='utf-8') as textfile:
        textfile.write("=" * 80 + "\n")
        textfile.write("SPIRITUAL REDDIT POSTS ANALYSIS\n")
        textfile.write(f"Extracted: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        textfile.write(f"Total Posts: {len(data)}\n")
        textfile.write("=" * 80 + "\n\n")
        
        for i, post in enumerate(data, 1):
            textfile.write(f"\n{'=' * 80}\n")
            textfile.write(f"POST #{i}\n")
            textfile.write(f"{'=' * 80}\n\n")
            
            textfile.write(f"Subreddit: r/{post['community']}\n")
            textfile.write(f"Title: {post['title']}\n")
            textfile.write(f"Posted: {post['created_date']}\n")
            textfile.write(f"Author: {post['author']}\n")
            if post['flair']:
                textfile.write(f"Flair: {post['flair']}\n")
            textfile.write(f"Upvotes: {post['upvotes']} | Comments: {post['num_comments']}\n")
            textfile.write(f"URL: {post['url']}\n")
            textfile.write(f"Emotions Detected: {', '.join(post['emotions']).upper()}\n\n")
            
            textfile.write(f"Content:\n{'-' * 80}\n")
            textfile.write(post['content'] if post['content'] else "[No text content]\n")
            textfile.write(f"\n{'-' * 80}\n")
            
            if post['top_comments']:
                textfile.write(f"\nTop Comments ({len(post['top_comments'])}):\n")
                textfile.write(f"{'-' * 80}\n")
                for j, comment in enumerate(post['top_comments'], 1):
                    textfile.write(f"\nComment #{j} | {comment['upvotes']} upvotes | By: {comment['author']} | {comment['created_date']}\n")
                    textfile.write(f"{comment['text']}\n")
                    textfile.write(f"{'-' * 40}\n")
            
            textfile.write("\n\n")

def analyze_communities(communities, posts_per_community, show_comments, max_comments, sleep_time):
    global analysis_status, latest_results
    
    analysis_status['running'] = True
    analysis_status['progress'] = 0
    analysis_status['total'] = len(communities)
    
    try:
        reddit = praw.Reddit(
            client_id=REDDIT_CLIENT_ID,
            client_secret=REDDIT_CLIENT_SECRET,
            user_agent="spiritual_research_v1"
        )
        reddit.read_only = True
        
        all_findings = []
        
        for idx, community in enumerate(communities):
            analysis_status['current_community'] = community
            analysis_status['message'] = f'Scanning r/{community}...'
            
            try:
                subreddit = reddit.subreddit(community)
                
                for post in subreddit.new(limit=posts_per_community):
                    full_text = post.title + " " + (post.selftext or "")
                    emotions = find_emotional_content(full_text)
                    
                    if emotions:
                        post_created = datetime.fromtimestamp(post.created_utc)
                        
                        post_data = {
                            'community': community,
                            'title': post.title,
                            'content': post.selftext or "",
                            'url': f"https://reddit.com{post.permalink}",
                            'flair': post.link_flair_text or "",
                            'created_date': post_created.strftime('%Y-%m-%d %H:%M:%S'),
                            'created_timestamp': post.created_utc,
                            'emotions': emotions,
                            'upvotes': post.score,
                            'num_comments': post.num_comments,
                            'post_id': post.id,
                            'author': str(post.author) if post.author else "[deleted]",
                            'top_comments': []
                        }
                        
                        if show_comments and post.num_comments > 0:
                            try:
                                post.comments.replace_more(limit=0)
                                for comment in list(post.comments)[:max_comments]:
                                    if hasattr(comment, 'body') and comment.body not in ['[removed]', '[deleted]']:
                                        comment_created = datetime.fromtimestamp(comment.created_utc)
                                        post_data['top_comments'].append({
                                            'text': comment.body,
                                            'upvotes': comment.score,
                                            'created_date': comment_created.strftime('%Y-%m-%d %H:%M:%S'),
                                            'created_timestamp': comment.created_utc,
                                            'author': str(comment.author) if comment.author else "[deleted]"
                                        })
                            except Exception as e:
                                pass
                        
                        all_findings.append(post_data)
                
                analysis_status['progress'] = idx + 1
                
                if idx < len(communities) - 1:
                    analysis_status['message'] = f'Waiting {sleep_time}s before next community...'
                    time.sleep(sleep_time)
                
            except Exception as e:
                analysis_status['message'] = f'Error accessing r/{community}: {str(e)[:50]}'
                time.sleep(2)
        
        latest_results = all_findings
        
        export_to_csv(all_findings)
        export_to_json(all_findings)
        export_to_text(all_findings)
        
        analysis_status['message'] = f'Complete! Found {len(all_findings)} posts'
        analysis_status['running'] = False
        
    except Exception as e:
        analysis_status['message'] = f'Error: {str(e)}'
        analysis_status['running'] = False

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    communities = [c.strip() for c in data.get('communities', []) if c.strip()]
    posts_per_community = int(data.get('postsPerCommunity', 25))
    show_comments = data.get('showComments', True)
    max_comments = int(data.get('maxComments', 3))
    sleep_time = int(data.get('sleepTime', 2))
    
    if not communities:
        return jsonify({'error': 'Please add at least one community'}), 400
    
    if analysis_status['running']:
        return jsonify({'error': 'Analysis already in progress'}), 400
    
    thread = threading.Thread(target=analyze_communities, args=(communities, posts_per_community, show_comments, max_comments, sleep_time))
    thread.daemon = True
    thread.start()
    
    return jsonify({'status': 'started'})

@app.route('/status')
def status():
    return jsonify(analysis_status)

@app.route('/results')
def results():
    return jsonify(latest_results)

@app.route('/download/<file_type>')
def download(file_type):
    files = {
        'csv': 'exports/spiritual_posts.csv',
        'json': 'exports/spiritual_posts.json',
        'txt': 'exports/spiritual_posts_for_chatgpt.txt'
    }
    
    if file_type not in files:
        return 'Invalid file type', 400
    
    file_path = files[file_type]
    if not os.path.exists(file_path):
        return 'File not found. Run analysis first.', 404
    
    return send_file(file_path, as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
