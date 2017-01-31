from slackbot.bot import listen_to
import re
from butter import butter
import time, json, random, math, itertools
import logging
import slackbot_settings

logger = logging.getLogger(__name__)

s_client = None

def poissonvariate(lambd):
    x = random.random()

    # special-case i = 0
    coeff = math.exp(-lambd)
    factorial = 1.0
    x -= coeff
    if x < 0: return 0

    # i = (1, 2, ...)
    for i in itertools.count(1):
        factorial *= i
        x -= coeff * (lambd**i/factorial)
        if x < 0: return i


def butt(msg, me=None):
    """.butt <text> -- buttifies a line of text"""

    try:
        return butter.buttify(msg, min_words=1)
    except:
        me("can't butt the unbuttable!")
        raise


def debutt(msg, me=None):
    """.debutt <text> -- provides debug butting info for a line of text"""

    sent, score = butter.score_sentence(msg)
    result = ''

    result += '{0}: '.format(score.sentence())
    for i, word in enumerate(sent):
        if score.word(i) == 0:
            result += '-'.join(word) + '(0) '
        else:
            result += '-'.join(word) + '({0}: {1}) '.format(
                score.word(i), score.syllable(i))
    return result


class ChannelState(object):
    def __init__(self, next_time=0, lines_left=0):
        self.next_time = next_time
        self.lines_left = lines_left

    def __dict__(self):
        return {
            'next_time': self.next_time,
            'line_left': self.lines_left
        }

    def __str__(self):
        return "next time %s line left %s" % (self.next_time, self.lines_left)


channel_states = {}

# TODO: don't fire this when someone ran .butt!


def butt_logger(message_id, text):
    global s_client
    text = "%s: %s" % (message_id, text)
    text.replace('\n', '')
    logger.info(text)
    butt_calibration(text)


def butt_calibration(send_text):
    global s_client
    reply = u'{}\n'.format(send_text)
    errors_to = s_client.find_channel_by_name(slackbot_settings.ERRORS_TO)
    s_client.rtm_send_message(errors_to, reply)


def username_lookup(message):
    client = get_client_dict(message)
    message_data = get_message_dict(message)

    user_id = message_data['_body']['user']
    users = client['users']
    return users[user_id]['name']


def get_message_dict(message, clean=False):
    message_data = message.__dict__
    return message_data


def get_channel_dict(message):
    return message.channel.__dict__


def get_client_dict(message):
    message_data = get_message_dict(message)
    client = message_data['_client']
    return client.__dict__


@listen_to('(.*)')
def autobutt(message, text):
    channel_data = get_channel_dict(message)
    channel = channel_data['_body']['name']
    message_id = channel_data['_body']['id']
    message_data = get_message_dict(message)
    global s_client
    s_client = message_data['_client']

    rate_mean = 20
    rate_sigma = 60
    lines_mean = 20
    now = time.time()

    if message_data['_body']['user'] is None:
        return None

    user_name = username_lookup(message)
    if user_name is None:
        return False

    butt_logger(message_id, "%s: %s" % (user_name, text))

    if True:
        if channel in channel_states:
            state = channel_states[channel]
            state.lines_left -= 1

            sent, score = butter.score_sentence(text)

            if state.next_time > now:
                time_left = state.next_time - now
                butt_logger(message_id, "waiting (%s seconds left)" % int(time_left))
                return

            score_sentence = score.sentence()

            if score_sentence <= 1:
                butt_logger(message_id, "sentence score was too low: %s" % score_sentence)
                return

            if score_sentence < state.lines_left:
                butt_logger(message_id, "lower score than line count %s / %s" % (score_sentence, state.lines_left))
                return

            text = butter.buttify_sentence(sent, score)
            butt_logger(message_id, "butt_text: %s" % text)
            message.send(text)

        else:
            butt_logger(message_id, "Adding channel %s to channel_states" % channel)

        channel_states[channel] = ChannelState(
            random.normalvariate(rate_mean, rate_sigma) + now,
            poissonvariate(lines_mean)
        )

