import praw
import time
import os
from collections import Counter

COMMUNITIES = ['spirituality', 'meditation', 'Mindfulness', 'awakened']
POSTS_PER_COMMUNITY = 25
SHOW_COMMENTS = True
MAX_COMMENTS_PER_POST = 3

print("🌈 Spiritual Trigger Finder - Starting...")
print("This will analyze spiritual communities for emotional patterns...")
print("=" * 50)
print(f"\n🎯 Communities to analyze: {', '.join(['r/' + c for c in COMMUNITIES])}")
print(f"📊 Posts per community: {POSTS_PER_COMMUNITY}")
print(f"💬 Show comments: {'Yes' if SHOW_COMMENTS else 'No'}")
print("=" * 50)

REDDIT_CLIENT_ID = os.environ.get('REDDIT_CLIENT_ID')
REDDIT_CLIENT_SECRET = os.environ.get('REDDIT_CLIENT_SECRET')

if not REDDIT_CLIENT_ID or not REDDIT_CLIENT_SECRET:
    print("❌ Missing Reddit API credentials!")
    print("\n🔧 Please set the following environment variables:")
    print("   • REDDIT_CLIENT_ID")
    print("   • REDDIT_CLIENT_SECRET")
    exit(1)

try:
    reddit = praw.Reddit(
        client_id=REDDIT_CLIENT_ID,
        client_secret=REDDIT_CLIENT_SECRET,
        user_agent="spiritual_research_v1"
    )
    reddit.read_only = True
    
    print("✅ Successfully connected to Reddit!")
    
except Exception as e:
    print(f"❌ Connection failed: {e}")
    print("\n🔧 TROUBLESHOOTING:")
    print("1. Check your credentials are correct")
    print("2. Make sure you installed 'praw' package")
    exit(1)

EMOTIONAL_PATTERNS = {
    'frustration': ['frustrated', 'stuck', 'cannot', 'struggling', 'difficult', 'hard', 'trying', 'failed', 'cant'],
    'confusion': ['confused', "don't understand", 'lost', 'uncertain', 'question', 'what does', 'how to', 'not sure'],
    'fear': ['afraid', 'scared', 'worried', 'anxious', 'fear', 'nervous', 'panic'],
    'loneliness': ['alone', 'lonely', 'isolated', 'no one understands', 'by myself', 'no friends'],
    'insecurity': ['not good enough', 'inadequate', 'imposter', 'doubt', 'not sure if', 'worthless'],
    'disappointment': ['disappointed', 'let down', 'failed', 'not working', 'waste', 'regret']
}

def find_emotional_content(text):
    """Check if text contains emotional triggers"""
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

def analyze_spiritual_communities():
    print("\n🔍 Scanning spiritual communities...")
    print("This may take 1-2 minutes...")
    
    all_findings = []
    
    for community in COMMUNITIES:
        print(f"📖 Checking r/{community}...")
        
        try:
            subreddit = reddit.subreddit(community)
            
            for post in subreddit.new(limit=POSTS_PER_COMMUNITY):
                full_text = post.title + " " + (post.selftext or "")
                emotions = find_emotional_content(full_text)
                
                if emotions:
                    post_data = {
                        'community': community,
                        'title': post.title,
                        'content': post.selftext or "",
                        'url': f"https://reddit.com{post.permalink}",
                        'emotions': emotions,
                        'upvotes': post.score,
                        'num_comments': post.num_comments,
                        'top_comments': []
                    }
                    
                    if SHOW_COMMENTS and post.num_comments > 0:
                        try:
                            post.comments.replace_more(limit=0)
                            for comment in list(post.comments)[:MAX_COMMENTS_PER_POST]:
                                if hasattr(comment, 'body') and comment.body not in ['[removed]', '[deleted]']:
                                    post_data['top_comments'].append({
                                        'text': comment.body,
                                        'upvotes': comment.score
                                    })
                        except Exception as e:
                            pass
                    
                    all_findings.append(post_data)
            
            time.sleep(1)
            
        except Exception as e:
            print(f"   ⚠️  Couldn't access r/{community}: {str(e)[:50]}...")
    
    return all_findings

print("\n" + "="*50)
print("🚀 STARTING ANALYSIS...")
print("="*50)

results = analyze_spiritual_communities()

print("\n" + "="*50)
print("🎯 ANALYSIS COMPLETE!")
print("="*50)

if results:
    print(f"📊 Found {len(results)} emotionally charged posts")
    
    all_emotions = []
    for post in results:
        all_emotions.extend(post['emotions'])
    
    emotion_counts = Counter(all_emotions)
    
    print("\n🔥 TOP EMOTIONAL TRIGGERS:")
    print("-" * 30)
    for emotion, count in emotion_counts.most_common():
        percentage = (count / len(results)) * 100
        print(f"• {emotion.upper()}: {count} posts ({percentage:.1f}%)")
    
    print(f"\n📝 DETAILED POST ANALYSIS:")
    print("=" * 70)
    for i, post in enumerate(results[:6]):
        print(f"\n{'─' * 70}")
        print(f"POST #{i+1} | r/{post['community']} | {post['upvotes']} ↑ | {post['num_comments']} comments")
        print(f"{'─' * 70}")
        print(f"\n📌 TITLE: {post['title']}")
        
        if post['content']:
            content_preview = post['content'][:400]
            if len(post['content']) > 400:
                content_preview += "..."
            print(f"\n📄 CONTENT:\n{content_preview}")
        
        print(f"\n💔 EMOTIONS DETECTED: {', '.join(post['emotions']).upper()}")
        print(f"🔗 URL: {post['url']}")
        
        if post['top_comments']:
            print(f"\n💬 TOP COMMENTS ({len(post['top_comments'])}):")
            for j, comment in enumerate(post['top_comments'], 1):
                comment_preview = comment['text'][:200]
                if len(comment['text']) > 200:
                    comment_preview += "..."
                print(f"\n   [{j}] ({comment['upvotes']} ↑)")
                print(f"   {comment_preview}")
    
    print(f"\n💡 INSIGHT:")
    if emotion_counts:
        top_emotion = emotion_counts.most_common(1)[0][0]
        print(f"Your spiritual clients struggle most with: {top_emotion.upper()}")
    else:
        print("No strong emotional patterns detected yet.")
    
else:
    print("❌ No emotional content found.")
    print("\n🔧 Try increasing the post limit or checking different communities")

print("\n✨ Done! Use these insights to better understand your clients' struggles.")
