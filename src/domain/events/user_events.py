from dataclasses import dataclass
from email import message


@dataclass
class UserCreatedEvent:
    topic:str
    message:dict 

@dataclass
class UserRegistredEvent:
    message:dict
@dataclass
class UserRefreshedEvent:
    pass

@dataclass
class UserAuthenticateEvent:
    pass

@dataclass
class UserCurrentedEvent:
    pass