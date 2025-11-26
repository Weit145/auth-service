from dataclasses import dataclass


@dataclass
class UserCreatedEvent:
    username: str
    email: str
    token_pod:str

@dataclass
class UserRegistredEvent:
    id:int 

@dataclass
class UserRefreshedEvent:
    pass

@dataclass
class UserAuthenticateEvent:
    pass

@dataclass
class UserCurrentedEvent:
    pass