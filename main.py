import sys
from urllib.parse import urlencode, parse_qs
from PyQt5 import QtCore
from PyQt5.QtWebEngineCore import QWebEngineUrlRequestInterceptor
from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QApplication

ClientId = ''
ClientSecret = ''
RedirectUrl = 'localhost/callback'
RedirectScheme = 'http://'
Scopes = ['user_read', 'channel_subscriptions', 'channel_check_subscription', 'user_subscriptions', 'channel_editor',
          'chat_login']

ResponseType = 'code'

Headers = {'client_id': ClientId, 'redirect_uri': RedirectScheme+RedirectUrl, 'response_type': ResponseType,
           'scope': str.join(' ', Scopes)}

AuthUrl = 'https://api.twitch.tv/kraken/oauth2/authorize?{headers}'.format(
    headers=urlencode(Headers))


class RequestInterceptor(QWebEngineUrlRequestInterceptor):

    def __init__(self, app):
        super(RequestInterceptor, self).__init__()
        self.app = app

    def interceptRequest(self, info):
        if RedirectUrl == (info.requestUrl().host()+info.requestUrl().path()):
            params = parse_qs(info.requestUrl().query())
            if 'code' in params.keys():
                print('OAuth code is {code}'.format(code=params['code']))
                self.app.quit()


class LoginWindow(QWebEngineView):
    logged_in = QtCore.pyqtSignal(['QString'])

    def __init__(self, app):
        super(LoginWindow, self).__init__()
        self.nam = self.page()
        self.app = app
        self.setUrl(QUrl(AuthUrl))
        self.show()
        self.loadFinished.connect(self._loadFinished)
        interceptor = RequestInterceptor(self.app)
        self.page().profile().setRequestInterceptor(interceptor)
        sys.exit(app.exec_())

    def _loadFinished(self, result):
        self.page().toHtml(self.callable)

    def callable(self, data):
        self.html = data


if __name__ == "__main__":
    app = QApplication(sys.argv)
    browser = LoginWindow(app)
