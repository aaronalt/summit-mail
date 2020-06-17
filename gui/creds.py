class Creds:

    def __init__(self, base_id, api_key, cfg_name):
        self.base_id = base_id
        self.api_key = api_key
        self.cfg_name = cfg_name

    @property
    def base_id(self):
        print("getting base_id...")
        return self._base_id

    @base_id.setter
    def base_id(self, value):
        print("setting base_id")
        self._base_id = value

    @property
    def api_key(self):
        print("getting api_key...")
        return self._api_key

    @api_key.setter
    def api_key(self, value):
        print("setting api_key...")
        self._api_key = value

    @property
    def cfg_name(self):
        print("getting cfg_name...")
        return self._cfg_name

    @cfg_name.setter
    def cfg_name(self, value):
        print("setting cfg_name...")
        self._cfg_name = value