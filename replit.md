# Spiritual Trigger Finder

## Overview
A Python tool that analyzes spiritual communities on Reddit to identify emotional patterns and triggers. This helps understand what struggles people face in their spiritual journeys.

## Purpose
- Scans Reddit communities (r/spirituality, r/meditation, r/Mindfulness, r/awakened)
- Identifies emotional patterns in posts (frustration, confusion, fear, loneliness, insecurity, disappointment)
- Provides insights into the most common emotional triggers

## Project Structure
- `spiritual_trigger_finder.py` - Main analysis script
- `.gitignore` - Excludes Python cache and sensitive files

## Dependencies
- Python 3.11
- PRAW (Python Reddit API Wrapper) 7.8.1

## Environment Variables
- `REDDIT_CLIENT_ID` - Reddit API client ID
- `REDDIT_CLIENT_SECRET` - Reddit API secret key

## How to Run
The workflow is already configured. The script runs automatically and analyzes recent posts from spiritual communities.

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
