from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP
import asyncpraw
import os
from dotenv import load_dotenv

load_dotenv()
mcp = FastMCP("reddit-summary")

async def get_reddit():
    try:
        username = os.getenv("USERNAME")
        password = os.getenv("PASSSWORD")
        client_id = os.getenv("CLIENT_ID")
        client_secret = os.getenv("CLIENT_SECRET")
        user_agent= os.getenv("USER_AGENT")
        reddit = asyncpraw.Reddit(username=username,password=password,client_id = client_id,client_secret=client_secret,user_agent=user_agent)
        return reddit
    except Exception as e:
        print(e)
        return None

@mcp.tool()
async def reed_comments(id=None,url=None,limit=15):
    """
        Reads and summarizes the top level comments that a submission have.
        Args:
            post id: str or url: str
        Output:
            List with the comments.
    """
    if id is None and url is None: return "Invalid argumnts."
    reddit = await get_reddit()
    if reddit is None: return "Cannot access the reddit client."
    submission = None
    if id is not None: submission = await reddit.submission(id=id)
    if url is not None: submission = await reddit.submission(url=url)
    res = []
    cnt = 0
    async for comment in submission.comments:
        if isinstance(comment,asyncpraw.models.MoreComments): continue
        if cnt > limit: break
        cnt += 1
        res.append(comment.body)
    await reddit.close()
    return res

@mcp.tool()
async def summarize_frontpage(limit:int = 10, with_comments:bool = False) -> dict:
    """
    Summarizes the user's reddit frontpage (alias: homepage, feed) by giving information dictinory to LLM.
    Optionaly this function can use comments for deeper summaries.
    Args:
        limit: integer (Optional) [default = 10]: sets a limit for how many post to fetch.
        with_comments: bool (Optional) [default = false]: indicates that summary will be done with comments.
    Output:
        Dictinory with keys as post id's and values as post informations
    """
    res = {}
    reddit = await get_reddit()
    if reddit is None: return "Cannot access the reddit client."
    async for submission in reddit.front.best(limit=limit):
        res[submission.id] = {
            "title": submission.title,
            "subreddit": submission.subreddit.display_name,
            "is-only-text":submission.is_self,
            "url": "www.reddit.com"+submission.permalink,
            "comments": await reed_comments(id=submission.id) if with_comments else []
        }
    await reddit.close()
    return res

@mcp.tool()
async def summarize_subreddit(subreddit_name:str ,fetch_by: str = "hot",limit: int = 10, with_comments:bool = False):
    """
    Summarizes the subreddit's frontpage (alias: homepage, feed) by giving information dictinory to LLM.
    Sorting, fetchings options are hot, new, top, rising, random.
    Optionaly this function can use comments for deeper summaries.
    Args:
        subreddit_name: str : name for subrredit without 'r/'
        fetch_by: str (Optional) [default = ''hot]: sorting, fetching option for subreddit's feed
        limit: integer (Optional) [default = 10]: sets a limit for how many post to fetch.
        with_comments: bool (Optional) [default = false]: indicates that summary will be done with comments.
    Output:
        Dictinory with keys as post id's and values as post informations
    """
    reddit = await get_reddit()
    if reddit is None: return "Cannot access the reddit client."
    subreddit = None
    try:
        subreddit = await reddit.subreddit(subreddit_name)
    except:
        return "Invalid subreddit name."
    generator = None
    match fetch_by.lower():
        case "hot":
            generator = subreddit.hot(limit=limit)
        case "new":
            generator = subreddit.new(limit=limit)
        case "top":
            generator = subreddit.top(limit=limit)
        case "rising":
            generator = subreddit.rising(limit=limit)
        case "random":
            generator = [None]*limit
            try:
                for i in range(limit): generator[i] = await subreddit.random()
            except:
                await reddit.close()
                return "This subreddit does not support random feature."
        case _:
            return "Invalid option for fetching. Only valid options are hot, new, top, rising, random."
    
    res = {}
    async for submission in generator:
        res[submission.id] = {
            "title": submission.title,
            "subreddit": submission.subreddit.display_name,
            "is-only-text":submission.is_self,
            "url": "www.reddit.com"+submission.permalink,
            "comments": await reed_comments(id=submission.id) if with_comments else []
        }
    await reddit.close()
    return res

@mcp.prompt()
def summarize_my_page():
    """Fixed prompt for detailed summary"""
    return """Make a summary of the reddit front page via summarize_frontpage function with limit=15 and with_comments=True arguments
    Use comments to get deeper understanding of public opinion about posts.
    Categorise these post into meaningful categories (e.g. politics/eceonomics, humour and meme, cultural/social etc.)
    
    For each category display context with following format:
    **Number**-**Category Name**:
    - **summary of post with comment analysis** from **Subreddit name**
    use this format for each post
    """

if __name__ == "__main__":
    mcp.run(transport='stdio')
    
