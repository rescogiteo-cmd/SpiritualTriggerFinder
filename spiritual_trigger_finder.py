import praw
import time
import os
from collections import Counter

print("🌈 Spiritual Trigger Finder - Starting...")
print("This will analyze spiritual communities for emotional patterns...")
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
    
    communities = ['spirituality', 'meditation', 'Mindfulness', 'awakened']
    
    all_findings = []
    
    for community in communities:
        print(f"📖 Checking r/{community}...")
        
        try:
            subreddit = reddit.subreddit(community)
            
            for post in subreddit.new(limit=25):
                emotions = find_emotional_content(post.title + " " + (post.selftext or ""))
                
                if emotions:
                    all_findings.append({
                        'community': community,
                        'title': post.title[:80] + "..." if len(post.title) > 80 else post.title,
                        'emotions': emotions,
                        'upvotes': post.score,
                        'comments': post.num_comments
                    })
            
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
    
    print(f"\n📝 RECENT EXAMPLES FOUND:")
    print("-" * 30)
    for i, post in enumerate(results[:6]):
        print(f"\n{i+1}. r/{post['community']}")
        print(f"   '{post['title']}'")
        print(f"   💔 Emotions: {', '.join(post['emotions'])}")
        print(f"   📈 Engagement: {post['upvotes']} 👍, {post['comments']} 💬")
    
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
