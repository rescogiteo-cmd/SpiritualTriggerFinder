# Spiritual Trigger Finder

## Overview
A Python tool that analyzes spiritual communities on Reddit to identify emotional patterns and triggers. This helps understand what struggles people face in their spiritual journeys.

## Purpose
- Scans Reddit communities (customizable list)
- Identifies emotional patterns in posts (frustration, confusion, fear, loneliness, insecurity, disappointment)
- Shows full post content and top comments
- Provides insights into the most common emotional triggers

## Features
- **Customizable Communities**: Edit the `COMMUNITIES` list at the top of the script to choose which subreddits to analyze
- **Comprehensive Data Extraction**: Captures full post content, metadata, and comments
- **Multiple Export Formats**: Saves data in CSV, JSON, and text formats
- **Post Details**: Extracts title, content, URL, flair, creation date, upvotes, author, and more
- **Comment Analysis**: Collects top comments with text, upvotes, dates, and authors
- **Emotional Patterns**: Automatically detects 6 emotional patterns in posts and comments

## Project Structure
- `spiritual_trigger_finder.py` - Main analysis script
- `.gitignore` - Excludes Python cache and sensitive files

## Dependencies
- Python 3.11
- PRAW (Python Reddit API Wrapper) 7.8.1

## Environment Variables
- `REDDIT_CLIENT_ID` - Reddit API client ID
- `REDDIT_CLIENT_SECRET` - Reddit API secret key

## Configuration
At the top of `spiritual_trigger_finder.py`, you can customize:
- `COMMUNITIES`: List of subreddit names to analyze (default: ['spirituality', 'meditation', 'Mindfulness', 'awakened'])
- `POSTS_PER_COMMUNITY`: Number of recent posts to check per community (default: 25)
- `SHOW_COMMENTS`: Whether to fetch comments (default: True)
- `MAX_COMMENTS_PER_POST`: Number of top comments to show per post (default: 3)

## How to Run
The workflow is already configured. Click "Run" to analyze spiritual communities and see detailed post content with comments.

## Exported Files
After each run, the script automatically creates three files:

### 1. spiritual_posts.csv
- **Purpose**: Spreadsheet analysis (Excel, Google Sheets)
- **Contains**: Post ID, community, title, content, URL, flair, created date, upvotes, comments count, author, emotions, and top 3 comments
- **Use for**: Filtering, sorting, pivot tables, and quantitative analysis

### 2. spiritual_posts.json
- **Purpose**: LLM/AI processing and programmatic access
- **Contains**: Complete structured data with all post and comment metadata including timestamps
- **Use for**: Training AI models, custom analysis scripts, or feeding to ChatGPT/Claude via API

### 3. spiritual_posts_for_chatgpt.txt
- **Purpose**: Easy copying to ChatGPT or other AI chat interfaces
- **Contains**: Human-readable formatted text with all post content and comments
- **Use for**: Copy entire file or specific posts to ChatGPT for deeper analysis, content generation, or insights

## Recent Analysis Results (Oct 30, 2025)
- **Posts Analyzed**: 45 emotionally charged posts
- **Top Emotional Triggers**:
  - CONFUSION: 48.9%
  - FRUSTRATION: 46.7%
  - FEAR: 37.8%
  - LONELINESS: 13.3%
  - INSECURITY: 13.3%
  - DISAPPOINTMENT: 6.7%
- **Key Insight**: Spiritual clients struggle most with CONFUSION

## Security
Reddit API credentials are stored securely in Replit Secrets and accessed via environment variables. Never hardcode credentials in the script.
