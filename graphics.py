from processing import *
from analysis import *
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

#load the structure with the statistics

D=load_obj("dict")

#store the dictionary of each stat by day
days=[]
stats=[]

for key in sorted(D):
	days.append(key)
	stats.append(D[key])

#obtain each data from day by day

# print(stats[0].keys())



#-------------- General Analysis --------------- 

#overall sentiment over the days:
ov_sent=[a['os'] for a in stats]

#number tweets
no_tws=[a['no_tweets'] for a in stats]

#brexit
no_brexit=[a['n Brexit'] for a in stats]
sent_brexit=[a['ms Brexit'] for a in stats]

#-------------- PARTY ANALYSIS -----------------

#labour
no_labour=[a['n Labour party'] for a in stats]
sent_labour=[a['ms Labour party'] for a in stats]

#conservatives
no_conservat=[a['n Conservative party'] for a in stats]
sent_conservat=[a['ms Conservative party'] for a in stats]

#brexit party
no_brexitpart=[a['n Brexit party'] for a in stats]
sent_brexitpart=[a['ms Brexit party'] for a in stats]

#libdems involves combining the two keys
no_l1=np.array([a['n Lib dems'] for a in stats])
no_l2=np.array([a['n Liberal Democrats'] for a in stats])
no_libdem=list(no_l1+no_l2)

sent_l1=np.array([a['ms Lib dems'] for a in stats])
sent_l2=np.array([a['ms Liberal Democrats'] for a in stats])
sent_libdem=list((sent_l1*no_l1+sent_l2*no_l2)/(no_l1+no_l2))

#-------------------- Leader Analysis ------------------






plot_overall=False
if plot_overall:
	plt.figure()
	plt.plot(days,ov_sent,marker='x',linestyle="--",color='g'
		,markeredgecolor='r',alpha=0.7,label="Overall Sentiment")
	plt.grid('on')
	ax = plt.gca()
	plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d/%Y'))
	plt.gca().xaxis.set_major_locator(mdates.DayLocator())
	ax.set_facecolor('#D9E6E8')
	plt.legend()
	plt.ylabel(r"Mean Sentiment")
	plt.tight_layout()
	plt.show()

plot_numbers=False
if plot_numbers:
	plt.plot(days,no_tws,marker='x',linestyle="--",color='g'
		,markeredgecolor='r',alpha=0.7)
	plt.grid('on')
	ax = plt.gca()
	ax.set_facecolor('#D9E6E8')
	plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
	plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d/%Y'))
	plt.gca().xaxis.set_major_locator(mdates.DayLocator())
	plt.ylabel(r"# of Tweets")
	plt.tight_layout()
	plt.show()

# plot_psents=True
if plot_psents:

	# plt.figure(figsize=(7,7))
	plt.plot(days,sent_conservat,marker='x',linestyle="--"
		,alpha=0.7,label="Conservative")
	plt.plot(days,sent_labour,marker='x',linestyle="--"
		,alpha=0.7,label="Labour")
	plt.plot(days,sent_libdem,marker='x',linestyle="--"
		,alpha=0.7,label="Liberal Democrat")
	plt.plot(days,sent_brexitpart,marker='x',linestyle="--"
		,alpha=0.7,label="Brexit Party")
	plt.grid('on')
	ax = plt.gca()
	plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d/%Y'))
	plt.gca().xaxis.set_major_locator(mdates.DayLocator())
	ax.set_facecolor('#D9E6E8')
	plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)
	plt.ylabel(r"Mean Sentiment")
	plt.tight_layout()
	plt.show()

# plot_partynos=True
if plot_partynos:
	plt.plot(days,no_conservat,marker='x',linestyle="--",
		alpha=0.7,label="Conservative")
	plt.plot(days,no_labour,marker='x',linestyle="--",
		alpha=0.7,label="Labour")
	plt.plot(days,no_brexitpart,marker='x',linestyle="--",
		alpha=0.7,label="Brexit Party")
	plt.plot(days,no_libdem,marker='x',linestyle="--",
		alpha=0.7,label="Liberal Democrats")
	plt.grid('on')
	ax = plt.gca()
	plt.legend()
	ax.set_facecolor('#D9E6E8')
	plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
	plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d/%Y'))
	plt.gca().xaxis.set_major_locator(mdates.DayLocator())
	plt.ylabel(r"# of Tweets")
	plt.tight_layout()
	plt.show()
	#an idea:
	#https://www.bbc.com/news/uk-politics-50572454


plot_nleaders=True
if plot_nleaders:
	plt.plot(days,no_conservat,marker='x',linestyle="--",
		alpha=0.7,label="Conservative")
	plt.plot(days,no_labour,marker='x',linestyle="--",
		alpha=0.7,label="Labour")
	plt.plot(days,no_brexitpart,marker='x',linestyle="--",
		alpha=0.7,label="Brexit Party")
	plt.plot(days,no_libdem,marker='x',linestyle="--",
		alpha=0.7,label="Liberal Democrats")
	plt.grid('on')
	ax = plt.gca()
	plt.legend()
	ax.set_facecolor('#D9E6E8')
	plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
	plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d/%Y'))
	plt.gca().xaxis.set_major_locator(mdates.DayLocator())
	plt.ylabel(r"# of Tweets")
	plt.tight_layout()
	plt.show()

