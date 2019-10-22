class PhraseCorrector:

    def _fix_parenthese(self, tokens):
        if len(tokens) == 0:
            return (False, '')
        else:
            changes = False
            if tokens[(-1)] == '(':
                changes = True
                tokens.pop(-1)
            open = [i for i, v in enumerate(tokens) if v == '(']
            close = [i for i, v in enumerate(tokens) if v == ')']
            for o in open:
                if o + 1 in close:
                    tokens.pop(o + 1)
                    tokens.pop(o)

            open_p = tokens.count('(')
            close_p = tokens.count(')')
            dif_count_parenthese = open_p - close_p
            for i in range(0, dif_count_parenthese):
                changes = True
                tokens.append(')')

            for i in range(dif_count_parenthese, 0):
                tokens.pop(tokens.index(')'))

            return (
             changes, tokens)

    def _remove_last_concept(self, tokens):
        if len(tokens) == 0:
            return (False, '')
        else:
            changes = False
            if tokens[(-1)].startswith(':'):
                tokens.pop(-1)
                changes = True
            return (
             changes, tokens)

    def _remove_last_concept_before_parentese(self, tokens):
        close = [i for i, v in enumerate(tokens) if v == ')']
        changes = False
        for c in close:
            if tokens[(c - 1)].startswith(':'):
                changes = True
                tokens.pop(c - 1)
                close = [i for i, v in enumerate(tokens) if v == ')']

        return (changes, tokens)

    def fix_predict(self, predict):
        changes = True
        split = predict.split()
        
        while changes:
            changes = False
                    
            changes_concept_parenthese, split = self._remove_last_concept_before_parentese(split)
            changes_concept, split            = self._remove_last_concept(split)
            changes_parentheses, split        = self._fix_parenthese(split)
            
            if changes_concept_parenthese or changes_concept or changes_parentheses:
                changes = True
                    
        return ' '.join(split)
