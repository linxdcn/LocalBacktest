
class LbtConfig():
    # wind or jq
    __datasource = 'wind'
    __jq_user = 'jq_user'
    __jq_password = 'jq_password'

    @staticmethod
    def set_datasource(source):
        LbtConfig.__datasource = source
    
    @staticmethod
    def get_datasource():
        return LbtConfig.__datasource

    @staticmethod
    def set_jq_user(user):
        LbtConfig.__jq_user = user

    @staticmethod
    def get_jq_user():
        return LbtConfig.__jq_user
    
    @staticmethod
    def set_jq_password(password):
        LbtConfig.__jq_password = password
    
    @staticmethod
    def get_jq_password():
        return LbtConfig.__jq_password