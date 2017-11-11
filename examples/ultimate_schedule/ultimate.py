# -*- coding: utf-8 -*-
import schedule
import time
import sys
import os
import random
import yaml             #->added to make pics upload -> see job8
import glob             #->added to make pics upload -> see job8
from tqdm import tqdm
import threading        #->added to make multithreadening possible -> see fn run_threaded

sys.path.append(os.path.join(sys.path[0],'../../'))
from instabot import Bot

whitelist = "whitelist.txt"
blacklist = "blacklist.txt"
comment = "comment.txt"
setting = "setting.txt"

if os.stat(setting).st_size == 0:
    print("Looks like setting are broken")
    print("Let's make new one")
    setting_input()

f = open(setting)
lines = f.readlines()
setting_0 = int(lines[0].strip())
setting_1 = int(lines[1].strip())
setting_2 = int(lines[2].strip())
setting_3 = int(lines[3].strip())
setting_4 = int(lines[4].strip())
setting_5 = int(lines[5].strip())
setting_6 = int(lines[6].strip())
setting_7 = int(lines[7].strip())
setting_8 = int(lines[8].strip())
setting_9 = int(lines[9].strip())
setting_10 = int(lines[10].strip())
setting_11 = int(lines[11].strip())
setting_12 = int(lines[12].strip())
setting_13 = int(lines[13].strip())
setting_14 = int(lines[14].strip())
setting_15 = int(lines[15].strip())
setting_16 = int(lines[16].strip())
setting_17 = int(lines[17].strip())
setting_18 = lines[18].strip()

bot = Bot(
    max_likes_per_day=setting_0,
    max_unlikes_per_day=setting_1,
    max_follows_per_day=setting_2,
    max_unfollows_per_day=setting_3,
    max_comments_per_day=setting_4,
    max_likes_to_like=setting_5,
    max_followers_to_follow=setting_6,
    min_followers_to_follow=setting_7,
    max_following_to_follow=setting_8,
    min_following_to_follow=setting_9,
    max_followers_to_following_ratio=setting_10,
    max_following_to_followers_ratio=setting_11,
    min_media_count_to_follow=setting_12,
    like_delay=setting_13,
    unlike_delay=setting_14,
    follow_delay=setting_15,
    unfollow_delay=setting_16,
    comment_delay=setting_17,
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

comments_file_name = "comments.txt"
random_user_file = bot.read_list_from_file("username_database.txt")
random_hashtag_file = bot.read_list_from_file("hashtag_database.txt")

#to get pics and autopost it
posted_pic_list = []
try:
    with open('pics.txt', 'r') as f:
        posted_pic_list = f.read().splitlines()
except:
    posted_pic_list = []
#!!-> to work this feature properly write full/absolute path to .jgp files as follows ->v
pics = glob.glob("/home/WZ/sandrine/instagram/pics/*.jpg")  #!!change this
pics = sorted(pics)
#end of pics processing

def setting_input():
    with open(setting, "w") as f:
        while True:
            print(
                "How many likes do you want to do in a day? (enter to use default number: 1000)")
            f.write(str(int(sys.stdin.readline().strip()or "1000")) + "\n")
            print("How about unlike? (enter to use default number: 1000)")
            f.write(str(int(sys.stdin.readline().strip()or "1000")) + "\n")
            print(
                "How many follows do you want to do in a day? (enter to use default number: 350)")
            f.write(str(int(sys.stdin.readline().strip()or "350")) + "\n")
            print("How about unfollow? (enter to use default number: 350)")
            f.write(str(int(sys.stdin.readline().strip()or "350")) + "\n")
            print(
                "How many comments do you want to do in a day? (enter to use default number:100)")
            f.write(str(int(sys.stdin.readline().strip()or "100")) + "\n")
            print("Maximal likes in media you will like?")
            print(
                "We will skip media that have greater like than this value (enter to use default number: 100)")
            f.write(str(int(sys.stdin.readline().strip()or "100")) + "\n")
            print("Maximal followers of account you want to follow?")
            print("We will skip media that have greater followers than this value (enter to use default number: 2000)")
            f.write(str(int(sys.stdin.readline().strip()or "2000")) + "\n")
            print("Minimum followers a account should have before we follow?")
            print(
                "We will skip media that have lesser followers than this value (enter to use default number: 10)")
            f.write(str(int(sys.stdin.readline().strip()or "10")) + "\n")
            print("Maximum following of account you want to follow?")
            print("We will skip media that have a greater following than this value (enter to use default number: 7500)")
            f.write(str(int(sys.stdin.readline().strip()or "7500")) + "\n")
            print("Minimum following of account you want to follow?")
            print("We will skip media that have lesser following from this value (enter to use default number: 10)")
            f.write(str(int(sys.stdin.readline().strip()or "10")) + "\n")
            print(
                "Maximal followers to following_ratio (enter to use default number: 10)")
            f.write(str(int(sys.stdin.readline().strip()or "10")) + "\n")
            print("Maximal following to followers_ratio (enter to use default number: 2)")
            f.write(str(int(sys.stdin.readline().strip()or "2")) + "\n")
            print("Minimal media the account you will follow have.")
            print(
                "We will skip media that have lesser media from this value (enter to use default number: 3)")
            f.write(str(int(sys.stdin.readline().strip()or "3")) + "\n")
            print(
                "Delay from one like to another like you will perform (enter to use default number: 10)")
            f.write(str(int(sys.stdin.readline().strip()or "10")) + "\n")
            print(
                "Delay from one unlike to another unlike you will perform (enter to use default number: 10)")
            f.write(str(int(sys.stdin.readline().strip()or "10")) + "\n")
            print(
                "Delay from one follow to another follow you will perform (enter to use default number: 30)")
            f.write(str(int(sys.stdin.readline().strip()or "30")) + "\n")
            print(
                "Delay from one unfollow to another unfollow you will perform (enter to use default number: 30)")
            f.write(str(int(sys.stdin.readline().strip()or "30")) + "\n")
            print(
                "Delay from one comment to another comment you will perform (enter to use default number: 60)")
            f.write(str(int(sys.stdin.readline().strip()or "60")) + "\n")
            print(
                "Want to use proxy? insert your proxy or leave it blank if no. (just enter)")
            f.write(str(sys.stdin.readline().strip()) or "None" + "\n")
            print("done with all settings")
            break


def parameter_setting():
    print("current parameter\n")
    f = open(setting)
    data = f.readlines()
    print("Max likes per day: " + data[0])
    print("Max unlikes per day: " + data[1])
    print("Max follows per day: " + data[2])
    print("Max unfollows per day: " + data[3])
    print("Max comments per day: " + data[4])
    print("Max likes to like: " + data[5])
    print("Max followers to follow: " + data[6])
    print("Min followers to follow: " + data[7])
    print("Max following to follow: " + data[8])
    print("Min following to follow: " + data[9])
    print("Max followers to following_ratio: " + data[10])
    print("Max following to followers_ratio: " + data[11])
    print("Min media_count to follow:" + data[12])
    print("Like delay: " + data[13])
    print("Unlike delay: " + data[14])
    print("Follow delay: " + data[15])
    print("Unfollow delay: " + data[16])
    print("Comment delay: " + data[17])
    print("Proxy: " + data[18])


#fn to return random value for separate jobs
def get_random(from_list):
    _random=random.choice(from_list)
    print("Random from ultimate.py script is chosen: \n" + _random + "\n")
    return _random

def stats():
    bot.logger.info('Last hour stats')
    bot.save_user_stats(bot.user_id)

def job1(): 
    bot.logger.info("Follow hashtags")
    bot.like_hashtag(get_random(random_hashtag_file), amount=int(700/24))

def job2():
    bot.logger.info("Like timeline")
    bot.like_timeline(amount=int(300/24))

def job3(): 
    bot.logger.info("Like followers")
    bot.like_followers(get_random(random_user_file), nlikes=3)

def job4():
    bot.logger.info("Follow followers")
    bot.follow_followers(get_random(random_user_file))

def job5():
    bot.logger.info("Comment medias")   
    bot.comment_medias(bot.get_timeline_medias())

def job6():
    bot.logger.info("UnFollow non followers")
    bot.unfollow_non_followers()

def job7():
    bot.logger.info("Follow users by hashtags") 
    bot.follow_users(bot.get_hashtag_users(get_random(random_hashtag_file)))

def job8(): #-->fn to upload photos /auto_uploader
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


def job9():  # put non followers on blacklist
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
    bot.logger.info("Rehashing username_database and hashtag_database") 
    random_user_file = bot.read_list_from_file("username_database.txt")
    random_hashtag_file = bot.read_list_from_file("hashtag_database.txt")

# function to make threads -> details here http://bit.ly/faq_schedule
def run_threaded(job_fn):
    job_thread=threading.Thread(target=job_fn)
    job_thread.start()

schedule.every(15).minutes.do(run_threaded, rehash)             #reload user and hashtag list every hour
schedule.every(1).hour.do(run_threaded, stats)              #get stats
schedule.every(8).hours.do(run_threaded, job1)              #like hashtag
schedule.every(2).hours.do(run_threaded, job2)              #like timeline
# schedule.every(1).days.at("16:00").do(run_threaded, job3)   #like followers of users from file
schedule.every(1).days.at("10:30").do(run_threaded, job4)   #follow followers
# schedule.every(16).hours.do(run_threaded, job5)             #comment medias
schedule.every(2).days.at("08:00").do(run_threaded, job6)   #unfollow non-followers
schedule.every(12).hours.do(run_threaded, job7)             #follow users from hashtag from file
# schedule.every(1).days.at("21:28").do(run_threaded, job8)   #upload pics
schedule.every(4).days.at("07:50").do(run_threaded, job9)   #non-followers blacklist

while True:
    schedule.run_pending()
    time.sleep(1)
