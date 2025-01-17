
from abc import ABC
from dataclasses import dataclass 

@dataclass
class Block(ABC):
    @property
    def prompt(self) -> str:
        pass

@dataclass
class Custom(Block):
    name: str
    entry: str

    @property
    def prompt(self) -> str:
        return f"{self.name}: {self.entry}"

@dataclass
class Essential(Custom):
    pass

@dataclass
class Card(Custom):
    triggers: list[str]

@dataclass
class Instruction(Block):
    name: str
    entries: list[str]

    @property
    def prompt(self) -> str:
        output = ""
        for entry in self.entries:
            output += f"    - {entry}\n"

        return f"{self.name}: \n{output.rstrip()}"

@dataclass
class Summary(Block):
    summary: str

    @property
    def prompt(self) -> str:
        output = ""
        for entry in self.entries:
            output += entry + "\n"

        return f"Summary of the story so far: {self.summary}"

@dataclass
class Entry(Block):
    entry: str

    @property
    def prompt(self) -> str:
        return self.entry

@dataclass
class Initial(Entry):
    pass

@dataclass
class User(Entry):
    pass

@dataclass
class Assistant(Entry):
    pass
