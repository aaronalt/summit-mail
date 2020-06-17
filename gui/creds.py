class Creds:

    def __init__(self, base_id, api_key, cfg_name, sender_email, sender_email_pw, test_email):
        self.base_id = base_id
        self.api_key = api_key
        self.cfg_name = cfg_name
        self.sender_email = sender_email
        self.sender_email_pw = sender_email_pw
        self.test_email = test_email

    @property
    def base_id(self):
        return self._base_id

    @base_id.setter
    def base_id(self, value):
        self._base_id = value

    @property
    def api_key(self):
        return self._api_key

    @api_key.setter
    def api_key(self, value):
        self._api_key = value

    @property
    def cfg_name(self):
        return self._cfg_name

    @cfg_name.setter
    def cfg_name(self, value):
        self._cfg_name = value

    @property
    def sender_email(self):
        return self._sender_email

    @sender_email.setter
    def sender_email(self, value):
        self._sender_email = value

    @property
    def sender_email_pw(self):
        return self._sender_email_pw

    @sender_email_pw.setter
    def sender_email_pw(self, value):
        self._sender_email_pw = value

    @property
    def test_email(self):
        return self._test_email

    @test_email.setter
    def test_email(self, value):
        self._test_email = value

