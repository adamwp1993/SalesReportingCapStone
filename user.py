
class User():

    def __init__(self, username, user_id):
        self.username = username
        self.user_id = user_id

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def get_id(self):
        return self.user_id

    def is_anonymous(self):
        return False

