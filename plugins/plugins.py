from slackbot.bot import listen_to
import re
from butter import butter
import time

@listen_to('(.*)')
def all_butte(message, text):
    message.reply('butte 2')


def butt(msg, me=None):
    """.butt <text> -- buttifies a line of text"""

    try:
        return butter.buttify(msg, min_words=1)
    except:
        me("can't butt the unbuttable!")
        raise

channel_states = {}

def autobutt(_, chan=None, msg=None, bot=None, say=None):
    butt_config = bot.config.get('butt', {})
    rate_mean  = butt_config.get('rate_mean', 300)
    rate_sigma = butt_config.get('rate_sigma', 60)
    lines_mean = butt_config.get('lines_mean', 20)
    now = time.time()

    if chan[0] == '#': # public channel
        if chan in channel_states:
            state = channel_states[chan]
            state.lines_left -= 1

            if state.next_time > now:
                return

            sent, score = butter.score_sentence(msg)

            if score.sentence() == 0 or score.sentence() < state.lines_left:
                return

            say(butter.buttify_sentence(sent, score))

        channel_states[chan] = ChannelState(
            random.normalvariate(rate_mean, rate_sigma) + now,
            poissonvariate(lines_mean)
        )
    else: # private message
        try:
            say(butter.buttify(msg))
        except:
            pass


class ChannelState(object):
    def __init__(self, next_time = 0, lines_left = 0):
        self.next_time = next_time
        self.lines_left = lines_left