# -*- coding: utf-8 -*-
import schedule
import time
import sys
import os
import random
import yaml             #->added to make pics upload -> see job8
import glob             #->added to make pics upload -> see job8
import ConfigParser
from tqdm import tqdm
import threading        #->added to make multithreadening possible -> see fn run_threaded

sys.path.append(os.path.join(sys.path[0],'../../'))
from instabot import Bot

def initbot():
    bot = Bot(
        max_likes_per_day=config.getint('BotParams','max_likes_per_day'),
        max_unlikes_per_day=config.getint('BotParams','max_unlikes_per_day'),
        max_follows_per_day=config.getint('BotParams','max_follows_per_day'),
        max_unfollows_per_day=config.getint('BotParams','max_unfollows_per_day'),
        max_comments_per_day=config.getint('BotParams','max_comments_per_day'),
        max_likes_to_like=config.getint('BotParams','max_likes_to_like'),
        max_followers_to_follow=config.getint('BotParams','max_followers_to_follow'),
        min_followers_to_follow=config.getint('BotParams','min_followers_to_follow'),
        max_following_to_follow=config.getint('BotParams','max_following_to_follow'),
        min_following_to_follow=config.getint('BotParams','min_following_to_follow'),
        max_followers_to_following_ratio=config.getint('BotParams','max_followers_to_following_ratio'),
        max_following_to_followers_ratio=config.getint('BotParams','max_following_to_followers_ratio'),
        max_following_to_block=config.getint('BotParams','max_following_to_block'),
        min_media_count_to_follow=config.getint('BotParams','min_media_count_to_follow'),
        like_delay=config.getint('BotParams','like_delay'),
        unlike_delay=config.getint('BotParams','unlike_delay'),
        follow_delay=config.getint('BotParams','follow_delay'),
        unfollow_delay=config.getint('BotParams','unfollow_delay'),
        comment_delay=config.getint('BotParams','comment_delay'),
        whitelist=whitelist,
        blacklist=blacklist,
        comments_file=comment,
        stop_words=[
            'order',
            'shop',
            'store',
            'free',
            'doodleartindonesia',
            'doodle art indonesia',
            'fullofdoodleart',
            'commission',
            'vector',
            'karikatur',
            'jasa',
            'open'])

    bot.login()
    bot.logger.info("ULTIMATE script. 24hours save")
    return bot

def parameter_setting():
    global config
    bot.logger.info("Showing current parameter\n")
    bot.logger.info("Max likes per day: " + config.get('BotParams','max_likes_per_day'))
    bot.logger.info("Max unlikes per day: " + config.get('BotParams','max_unlikes_per_day'))
    bot.logger.info("Max follows per day: " + config.get('BotParams','max_follows_per_day'))
    bot.logger.info("Max unfollows per day: " + config.get('BotParams','max_unfollows_per_day'))
    bot.logger.info("Max comments per day: " + config.get('BotParams','max_comments_per_day'))
    bot.logger.info("Max likes to like: " + config.get('BotParams','max_likes_to_like'))
    bot.logger.info("Max followers to follow: " + config.get('BotParams','max_followers_to_follow'))
    bot.logger.info("Min followers to follow: " + config.get('BotParams','min_followers_to_follow'))
    bot.logger.info("Max following to follow: " + config.get('BotParams','max_following_to_follow'))
    bot.logger.info("Min following to follow: " + config.get('BotParams','min_following_to_follow'))
    bot.logger.info("Max followers to following_ratio: " + config.get('BotParams','max_followers_to_following_ratio'))
    bot.logger.info("Max following to followers_ratio: " + config.get('BotParams','max_following_to_followers_ratio'))
    bot.logger.info("Max following to block: " + config.get('BotParams','max_following_to_block'))
    bot.logger.info("Min media_count to follow:" + config.get('BotParams','min_media_count_to_follow'))
    bot.logger.info("Like delay: " + config.get('BotParams','like_delay'))
    bot.logger.info("Unlike delay: " + config.get('BotParams','unlike_delay'))
    bot.logger.info("Follow delay: " + config.get('BotParams','follow_delay'))
    bot.logger.info("Unfollow delay: " + config.get('BotParams','unfollow_delay'))
    bot.logger.info("Comment delay: " + config.get('BotParams','comment_delay'))
    bot.logger.info("Proxy: " + config.get('BotParams','proxy'))


#fn to return random value for separate jobs
def get_random(from_list):
    _random=random.choice(from_list)
    print("Random from ultimate.py script is chosen: \n" + _random + "\n")
    return _random

def stats():
    bot.logger.info('Last hour stats')
    bot.save_user_stats(bot.user_id)

def follow_hashtags(): 
    bot.logger.info("Follow hashtags")
    bot.like_hashtag(get_random(random_hashtag_file), amount=int(700/24))

def like_hashtag():
    bot.logger.info("Like timeline")
    bot.like_timeline(amount=int(300/24))

def like_followers(): 
    bot.logger.info("Like followers")
    bot.like_followers(get_random(random_user_file), nlikes=3)

def follow_followers():
    bot.logger.info("Follow followers")
    bot.follow_followers(get_random(random_user_file))

def block_bots():
    bot.logger.info("Blocking Bots")
    bot.block_bots()

def comment_medias():
    bot.logger.info("Comment medias")   
    bot.comment_medias(bot.get_timeline_medias())

def unfollow_non_followers():
    bot.logger.info("UnFollow non followers")
    bot.unfollow_non_followers()

def follow_users():
    bot.logger.info("Follow users by hashtags") 
    bot.follow_users(bot.get_hashtag_users(get_random(random_hashtag_file)))

def upload_image(): #-->fn to upload photos /auto_uploader
    bot.logger.info("upload image") 
    try:
        for pic in pics:
            if pic in posted_pic_list:
                continue
            hashtags = "/>\n​​#instabot #vaskokorobko #kyiv"       #add custom hashtags
            caption = pic[:-4].split(" ")                        #caption is made from the name of file
            caption = " ".join(caption[1:])
            caption = "\n<" + caption + hashtags                 #create full caption with hashtags
            print("upload: " + caption)
            bot.uploadPhoto(pic, caption=caption)
            if bot.LastResponse.status_code != 200:
                print("Smth went wrong. Read the following ->\n")
                print(bot.LastResponse)
                # snd msg
                break

            if not pic in posted_pic_list:
                posted_pic_list.append(pic)
                with open('pics.txt', 'a') as f:
                    f.write(pic + "\n")
                print("Succsesfully uploaded: " + pic)
                break
    except Exception as e:
        print(str(e))
# end of job8


def blacklist_non_followers():  # put non followers on blacklist
    bot.logger.info("blacklist non followers") 
    try:
        print("Creating Non Followers List")
        followings = bot.get_user_following(bot.user_id)  # getting following
        followers = bot.get_user_followers(bot.user_id)  # getting followers
        friends_file = bot.read_list_from_file("friends.txt")  # same whitelist (just user ids)
        nonfollowerslist = list((set(followings) - set(followers)) - set(friends_file))
        with open('blacklist.txt', 'a') as file:  # writing to the blacklist
            for user_id in nonfollowerslist:
                file.write(str(user_id) + "\n")
        print("removing duplicates")
        lines = open('blacklist.txt', 'r').readlines()
        lines_set = set(lines)
        out = open('blacklist.txt', 'w')
        for line in lines_set:
            out.write(line)
        print("Task Done")
    except Exception as e:
        print(str(e))

def rehash():
    global random_user_file
    global random_hashtag_file
    global config
    global setting

    config = ConfigParser.RawConfigParser()
    config.read(setting)

    bot.logger.info("Rehashing username_database and hashtag_database")
    random_user_file = bot.read_list_from_file(config.get('Files','random_user_file'))
    random_hashtag_file = bot.read_list_from_file(config.get('Files','random_hashtag_file'))

    parameter_setting()

# function to make threads -> details here http://bit.ly/faq_schedule
def run_threaded(job_fn):
    job_thread=threading.Thread(target=job_fn)
    job_thread.start()

if __name__ == '__main__':

    setting = "setting.txt"

    config = ConfigParser.RawConfigParser()
    config.read(setting)

    whitelist = config.get('Files','whitelist')
    blacklist = config.get('Files','blacklist')
    comment = config.get('Files','comment')

    bot = initbot()

    random_user_file = bot.read_list_from_file(config.get('Files','random_user_file'))
    random_hashtag_file = bot.read_list_from_file(config.get('Files','random_hashtag_file'))

    #to get pics and autopost it
    posted_pic_list = []
    try:
        with open('pics.txt', 'r') as f:
            posted_pic_list = f.read().splitlines()
    except:
        posted_pic_list = []
    #!!-> to work this feature properly write full/absolute path to .jgp files as follows ->v
    pics = glob.glob(os.environ['HOME'] + "/instagram/pics/*.jpg")  #!!change this
    pics = sorted(pics)
    #end of pics processing

    schedule.every(15).minutes.do(run_threaded, rehash)             #reload user and hashtag list every hour
    schedule.every(1).hour.do(run_threaded, stats)              #get stats
    schedule.every(8).hours.do(run_threaded, follow_hashtags)              #like hashtag
    schedule.every(2).hours.do(run_threaded, like_hashtag)              #like timeline
    schedule.every(1).days.at("17:45").do(run_threaded, like_followers)   #like followers of users from file
    schedule.every(1).days.at("18:30").do(run_threaded, follow_followers)   #follow followers
    # schedule.every(16).hours.do(run_threaded, comment_medias)             #comment medias
    schedule.every(1).days.at("08:30").do(run_threaded, unfollow_non_followers)   #unfollow non-followers
    # schedule.every(1).days.at("07:00").do(run_threaded, block_bots)   #block bots
    schedule.every(12).hours.do(run_threaded, follow_users)             #follow users from hashtag from file
    # schedule.every(1).days.at("21:28").do(run_threaded, upload_image)   #upload pics
    schedule.every(4).days.at("07:50").do(run_threaded, blacklist_non_followers)   #non-followers blacklist

    while True:
        schedule.run_pending()
        time.sleep(1)
