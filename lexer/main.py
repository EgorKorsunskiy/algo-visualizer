# now support only cpp code
from lexer.token_lists import TokenTypes, merge_rules, string_to_token_map


class Lexer:
    def __init__(self) -> None:
        # TODO: probably allow for selecting languages different from cpp
        pass

    def augmentToken(self, targetToken, tokenA, tokenB):
        if targetToken["token_type"] == TokenTypes.FN:
            targetToken["value"] = tokenA["value"]
        elif targetToken["token_type"] == TokenTypes.IDENT:
            value = tokenA["value"] if "value" in tokenA else tokenB["value"]
            targetToken["value"] = value
        return targetToken

    def merge_tokens(self, tokens: list) -> list:
        new_tokens = []
        last_insert_index = -1
        for i in range(1, len(tokens)):
            if i - 1 <= last_insert_index:
                continue
            token_couple = f"{tokens[i - 1]['token_type']}_{tokens[i]['token_type']}"
            token_to_insert = None
            if token_couple in merge_rules:
                token_to_insert = merge_rules[token_couple].copy()
                token_to_insert = self.augmentToken(
                    token_to_insert, tokens[i - 1], tokens[i]
                )
                last_insert_index = i
            else:
                token_to_insert = tokens[i - 1]
            new_tokens.append(token_to_insert)
        if last_insert_index != len(tokens) - 1:
            new_tokens.append(tokens[-1])

        return new_tokens

    def tokens_merge_helper(self, tokens, iter=2):
        for _ in range(iter):
            tokens = self.merge_tokens(tokens)
        return tokens

    def parse(self, input_string: str) -> list:
        tokens = []
        current_word = ""

        for ch in input_string:
            token_to_insert = None
            if ch in string_to_token_map:
                token_to_insert = string_to_token_map[ch]
                if len(current_word) > 0:
                    tokens.append(self.get_token_based_on_word(current_word))
                    current_word = ""
            else:
                if self.is_valid_ch(ch):
                    current_word += ch
                elif self.is_whitespace(ch) and len(current_word) > 0:
                    token_to_insert = self.get_token_based_on_word(current_word)
                    current_word = ""
            if token_to_insert != None:
                tokens.append(token_to_insert)
        if current_word:
            tokens.append(self.get_token_based_on_word(current_word))
        tokens.append({"token_type": TokenTypes.EOF})
        return tokens

    def get_token_based_on_word(self, word: str) -> dict:
        if word in string_to_token_map:
            token = string_to_token_map[word]
            return token
        elif self.is_valid_number(word):
            return {"token_type": TokenTypes.INT, "value": int(word)}
        else:
            return {"token_type": TokenTypes.IDENT, "value": word}

    # ch helpers
    def is_valid_ch(self, char: str) -> bool:
        return self.is_letter(char) or self.is_digit(char)

    def is_letter(self, char: str) -> bool:
        return char.isalpha()

    def is_digit(self, char: str) -> bool:
        return char.isdigit()

    def is_whitespace(self, char: str) -> bool:
        return char.isspace()

    # ident vs literal helpers
    def is_valid_number(self, word: str) -> bool:
        return word.isdigit()
