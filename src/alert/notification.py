import telegram
from single_instance import SingleInstance

class NotificationBot(object):
    def __init__(self):
        self.settings = SingleInstance.get('settings')
        self.log = SingleInstance.get('log')
        self._token = self.settings['telegram']['token']
        self._chat_id = self.settings['telegram']['chat_id']
        self.tlg_bot = None
        self.initialize_bot()
        self.redis = SingleInstance.get('redis')
        self.alert_time = {}
        self.set_default_time_bucket()


    def initialize_bot(self):
        try:
            self.tlg_bot = telegram.Bot(token=self._token)
            self.log.info("Bot creation success!! token: %s" % (self._token))
        except Exception , err:
            self.log.error("Bot creation failure!! --> %s" % str(err))


    def set_default_time_bucket(self):
        default_alert_interval = ['day', 'hour', 'minute', 'second']
        for interval in default_alert_interval:
            self.alert_time[interval] = {}
            for coin in self.settings['target']['coins'].split(','):
                self.alert_time[interval][coin.upper()] = None


    def send_message(self, msg):
        self.tlg_bot.sendMessage(chat_id = self._chat_id, text=msg)


    def default_notification(self, date, coin, price_info):
        noti_targets = self.settings['target']['coins']
        interval = self.settings['alert']['default']

        time_bucket = {}

        time_bucket['day'] = date.strftime("%Y%m%d")
        time_bucket['hour'] = date.strftime("%H")
        time_bucket['minute'] = date.strftime("%M")
        time_bucket['second'] = date

        msg = "[Default price notification]\n[[%s]]\n\
            %10s: %10s\n\
            %10s: %10s\n\
            %10s: %10s\n\
            %10s: %10s\n"\
            % (coin, "max price", price_info["max_price"], \
            "min price", price_info["min_price"],\
            "buy price", price_info["buy_price"],\
            "sell price", price_info["sell_price"])

        if self.alert_time[interval][coin] != time_bucket[interval]:
            self.send_message(msg)
            self.alert_time[interval][coin] = time_bucket[interval]

if __name__ == "__main__":
    pass







