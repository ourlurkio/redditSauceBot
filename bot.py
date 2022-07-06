import praw
import re
import random
import json


# FUNCTIONS
def get_response_list():
    '''Returns a list of daft responses from file responses.txt'''
    with open('responses.txt', 'r') as responses:
        rawText = responses.read()
        return rawText.split('\n')


def generate_response():
    '''Calls get_response_list to generate list, assigns random int to pick reponse to return'''
    responseList = get_response_list()
    randomise = random.randint(0, len(responseList) - 1)
    return responseList[randomise]


def get_recipe_list():
    '''Opens recipe json file, loads and returns json object'''
    with open('recipe_json.json', 'r') as file:
        return json.load(file)


def generate_recipe():
    '''Calls get_recipe_list to generate recipe dictionary, assigns random int to pick recipe to return'''
    recipeDict = get_recipe_list()
    randomise = random.randint(0, len(recipeDict) - 1)
    return recipeDict[randomise]


def add_comment_to_replied_cache(commentId):
    with open('comments_replied_to.txt', 'a') as cache:
        cache.write('\n')
        cache.write(commentId)
        cache.close()


# MAIN
reddit = praw.Reddit(
    site_name="sauceBot",
)

subTarget = "all"
matchString = 'source?'

subreddit = reddit.subreddit(subTarget)
source = re.compile(matchString, re.IGNORECASE)

# open comments that have been replied too, and stores ids in list for checking
with open('comments_replied_to.txt', 'r') as cache:
    postsRepliedTo = cache.read()
    postsRepliedTo = postsRepliedTo.split('\n')
    commentIdList = list(postsRepliedTo)
    cache.close()

for submission in subreddit.hot(limit=10):
    # using a breadth first traverse to navigate all comments in a thread
    submission.comments.replace_more(limit=0)
    comment_queue = submission.comments[:]
    while comment_queue:
        comment = comment_queue.pop(0)
        comment_queue.extend(comment.replies)
        isMatch = re.search(source, comment.body)  # checks if match keyword in comment, match object returned
        if isMatch and comment.id not in commentIdList:  # if comment not replied to, and isMatch == True, reply and append comment ID to cache file
            recipe = generate_recipe()
            comment.reply(body=f'{generate_response()}\n\n'
                               f'Everything is better with sauce, so here is a recipe for one, enjoy!\n\n'
                               f'Name: {recipe["name"]}\n\n'
                               f'Link: {recipe["link"]}')
            add_comment_to_replied_cache(comment.id)
