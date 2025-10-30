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
- **Post Details**: View full post titles, content (400 character preview), and direct URLs
- **Comment Analysis**: See top comments from each post (configurable)
- **Emotional Patterns**: Automatically detect 6 emotional patterns in posts and comments

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
