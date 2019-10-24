#!/bin/python3


# seems a user-friendly web crawler package
from requests_html import HTMLSession
# python library for linear algebra
import numpy as np

# pre-define counts of balls in history
winning_ball_count=[0] * 40
power_ball_count=[0] * 20
#
# and define list of balls
list_winning_ball=[x for x in range(1,41)]
list_power_ball=[x for x in range(1,21)]

#===== Step 1. Get lottery results from website =====
#
# see a general instruction at https://zhuanlan.zhihu.com/p/34206711
#
# The following website is easier to retrive date for us
# https://www.lotto.net/australia-powerball/results/

# year to search
year_range=['2018','2019']
#
# first create a new session
session = HTMLSession()
#
# loop for each year in the year_range
for year in year_range:
	#
	# create the new URL
	url = 'https://www.lotto.net/australia-powerball/results/'+year
	#
	# grab the website
	r = session.get(url)
	#
	# now we already have a full history of the year stored in r, all need to do then is to find where they are
	# This is case-by-case, it turns our in the above website, we can use a CSS selector(see https://zhuanlan.zhihu.com/p/34206711) 
	# with two numbers to find the number in the lottery
	# I called them "week" and "index_power_ball/index_winning_ball"
	#
	index_power_ball = 8
	# Count balls
	for week in range(1,60):
		# Count for power balls
		#
		# here is the CSS selector, you can see how the two numbers (week and index_power_ball) play the role
		sel='body > div > div > div.archive-container > div:nth-child('+str(week)+') > div.row-2 > ul > li:nth-child('+str(index_power_ball)+') > span'
		#
		# search for this selector
		results = r.html.find(sel)
		#
		# make sure the week exits and is after the version update 04/19/18
		if len(results) > 0:
			# results[0].text is the number of the power ball from the week we are iterating on
			# we convert it to an integer and subtract 1 to turn it to the index of the count list,
			# and we add one to that count
			power_ball_count[int(results[0].text)-1] += 1
		# otherwise terminate the search for this year
		else:
			break
		#
		# Count for winning balls
		#
		# similar as in the power ball case, except that we have 7 winning balls, so another loop is required
		for index_winning_ball in range(1,8):
			sel='body > div > div > div.archive-container > div:nth-child('+str(week)+') > div.row-2 > ul > li:nth-child('+str(index_winning_ball)+') > span' 
			results = r.html.find(sel)
			winning_ball_count[int(results[0].text)-1] += 1
# Here is the full counting list, you can uncomment to print them
#print(winning_ball_count)
#print(power_ball_count)

#===== Step 2. Generate the number for this week =====
#
# This is essentially is same as the previous version
#
for num_draw in range(4):
	p_winning = np.array(winning_ball_count) / np.sum(np.array(winning_ball_count))
	draw_winning = np.random.choice(list_winning_ball, 7, replace=False, p=p_winning)
	p_powerball = np.array(power_ball_count) / np.sum(np.array(power_ball_count))
	draw_powerball = np.random.choice(list_power_ball, 1, p=p_powerball)
	print(draw_winning, draw_powerball)
#
print("Good Luck This Week!")
