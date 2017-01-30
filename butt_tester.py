from butter import butter
import pprint

text = "Hi Everyone.  I passed out W2’s today, and didn’t explain some recent organizational shifts in the company.  Earlier this week, Mike Ludwig (our CFO) was let go, as we have contracted the CFO position.  The reality is, there wasn’t enough work for us to need a full-time CFO.  Mike will still be around to help on occasion (he was here this morning), but all financial concerns should be directed at Shelley for the immediate future.  On Monday, at the start of our planning meeting, let’s take some time to talk about the org changes.  Thanks for all the hard work in getting CNSA ready to roll!"
sent, score = butter.score_sentence(text)

print(score)

print(score.sentence())

print(sent)
output = butter.buttify_sentence(sent, score)


print(output)


