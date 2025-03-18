
class CompositeConfig:
    def __init__(self, user, chat, study_group, course) -> None:
        self.user = user
        self.chat = chat
        self.study_group = study_group
        self.course = course
    
    def get_user_config(self):
        return self.user
    def get_chat_config(self):
        return self.chat
    def get_study_config(self):
        return self.study_group
    def get_couuse_config(self):
        return self.course
    