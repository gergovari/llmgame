
from dataclasses import dataclass
from block import Block, Instruction, Essential, Custom, Card, Initial, Summary, Assistant, User

from openai import OpenAI

@dataclass
class BlockManager:
    blocks: list[Block]
    
    def edit(self, old: Block, new: Block):
        for i, block in enumerate(self.blocks):
            if block is old:
                instances[i] = new_instance
                break

    def erase(self, old: Block):
        self.blocks.remove(old)

    def erase_until(self, until: Block):
        for i in range(len(self.blocks) - 1, -1, -1):
            if self.blocks[i] is until:
                break
            del self.blocks[i]

class LLM:
    
    openai = OpenAI()
    block_priority = {
            Instruction: 10,
            Essential: 20,
            Custom: 30,
            Card: 35,
            Initial: 40,
            Summary: 998,
            Assistant: 999,
            User: 999,
    }
 
    def summarize(self, context: list) -> str:
        result = [{
                "role": "user",
                "content": "Summarize the following roleplaying game:"
            }]
        return generate(result + context, model="gpt-4o-mini")

    def generate(self, context: list, model: str = "gpt-4o") -> str:
        completion = self.openai.chat.completions.create(
            model=model,
            messages=context
        )
        return completion.choices[0].message.content

    def blocks_to_context(self, blocks: list[Block]) -> str:
        messages = []

        cards = [obj for obj in blocks if isinstance(obj, Card)]
        other = [obj for obj in blocks if not isinstance(obj, Card)]
        final = list(other)

        for block in other:
            for card in cards:
                for trigger in card.triggers:
                    if trigger in block.prompt:
                        final.append(card)

        final = sorted(final, key=lambda x: self.block_priority.get(type(x), 34))
        for block in final:
            if isinstance(block, (Instruction, Essential, Custom, Card)):
                messages.append({ 
                        "role": "system", 
                        "content": block.prompt
                })
            elif isinstance(block, Assistant):
                messages.append({ 
                        "role": "assistant", 
                        "content": block.prompt
                })
            else:
                messages.append({ 
                        "role": "user", 
                        "content": block.prompt
                })

        return messages

@dataclass
class DM:
    blockmanager: BlockManager
    llm: LLM
    turn_until_summary: int = 4

    turn_counter: int = 0
    
    def summarize(self):
        filtered = [block for block in self.blocks if isinstance(block, (Initial, Summary, Assistant, User))]
        summarized = self.llm.summarize(self.llm.blocks_to_context(filtered))
        self.blocks = [block for block in self.blockmanager.blocks if block not in filtered]
        self.blocks.append(Summary(summary=summarized))

    def turn(self, prompt: str):
        self.blockmanager.blocks.append(User(entry=prompt))
        self.continue_game()
        #self.turn_counter += 1
        #if self.turn_counter >= self.turn_until_summary:
        #    summarize()
        #    turn_counter = 0

    def continue_game(self):
        answer = self.llm.generate(self.llm.blocks_to_context(self.blockmanager.blocks))
        self.blockmanager.blocks.append(Assistant(entry=answer))

    def retry(self):
        self.blockmanager.blocks.pop()
        self.continue_game()
