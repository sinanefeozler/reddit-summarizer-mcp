# Reddit Summarizer MCP Server
A Model Context Protocol (MCP) server for summarizing homepage of the user or contents of subreddits and comments on posts.
## Features
- Summarize user's reddit frontpage (homepage) with or without comment analyses.
- Summarize a subreddit contents by inspecting posts sorted by hot, new, top, rising, random (if aviable) with or without comment analysis.
- Summarize comments on a post.
## Requirements
- Python 3.12 or higher
- uv package manager (recommended)
- Reddit API credentials
- MCP client (e.g. Claude Desktop)
## Installation
Clone repository or download files manually.
```bash
git clone https://github.com/sinanefeozler/reddit-summarizer-mcp.git
cd reddit-summarizer-mcp
```
Create virtual envoriment and install dependencies.
```bash
uv venv
source .venv/bin/activate
uv sync
```
### Setting Up The Envoriment Variables
- This server needs reddit username, password and reddit authentication.
- You can get client id and client secret by following [these steps](https://github.com/reddit-archive/reddit/wiki/OAuth2-Quick-Start-Example#first-steps)
- When you get the required keys create .env file according to .env.example
For claude desktop client users check out this [link](https://modelcontextprotocol.io/quickstart/user) to setup the server.
## Available Tools
### `summarize_frontpage`
Summarize user's homepage with post limits and optional comment analyse on posts.
Parameters:
- `limit` (default: 10): Post fetching limit
- `with_comments` (default: false): Summarize with comments on posts
### `summarize_subreddit`
Summarize a subreddit's contents by inspecting posts.
Parameters:
- `limit` (default: 10): Post fetching limit
- `with_comments` (default: false): Summarize with comments on posts
- `fetch_by` (default: 'hot') : Sorting option for posts. (hot, new, top, rising, random if aviable)
### `reed_comments`
Reed and summarize comments on a post. Needs post id or url.
Parameters:
- `id` (default: None) : id of post
- `url` (default: None) : url of post
- `limit` (default: 15) : fetching limit of the comments
## Prompts
### Example Prompts:
- "Summarize my reddit frontpage with comment analyse for deeper understanding of public opinion"
- "Summarize the hot post of Politics"
### Prompt Template:
#### `/summarize_my_page`
Provides a prompt to summarize and categorize the posts and comments on frontpage. Gives LLM a predefined template and categorize to make a more human readable outputs.
