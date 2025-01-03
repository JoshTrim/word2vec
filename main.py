sample_text = '''
In psychology, theory of mind refers to the capacity to understand other people by ascribing mental states to them.
A theory of mind includes the understanding that others' beliefs, desires, intentions, emotions, and thoughts may be different from one's own.
Possessing a functional theory of mind is crucial for success in everyday human social interactions.
People utilize a theory of mind when analyzing, judging, and inferring others' behaviors.
The discovery and development of theory of mind primarily came from studies done with animals and infants.
Factors including drug and alcohol consumption, language development, cognitive delays, age, and culture can affect a person's capacity to display theory of mind.
Having a theory of mind is similar to but not identical with having the capacity for empathy or sympathy.

It has been proposed that deficits in theory of mind may occur in people with autism, anorexia nervosa, schizophrenia, dysphoria, cocaine addiction, and brain damage caused by alcohol's neurotoxicity.
Neuroimaging shows that the medial prefrontal cortex (mPFC), the posterior superior temporal sulcus (pSTS), the precuneus, and the amygdala are associated with theory of mind tasks.
Patients with frontal lobe or temporoparietal junction lesions find some theory of mind tasks difficult.
One's theory of mind develops in childhood as the prefrontal cortex develops.
It has been argued that children in a culture of collectivism develop knowledge access earlier and understand diverse beliefs later than Western children in a culture of individualism.
'''

import numpy as np
import re

np.random.seed(42)

WINDOW_SIZE = 2


def tokenize(text: str):
    """basically gets all words without apostrophes"""
    pattern = re.compile(r'[A-Za-z]+[\w^\']*|[\w^\']*[A-Za-z]+[\w^\']*')
    return pattern.findall(text.lower())

def generate_mappings(tokens: list[str]):
    """generates token -> idx and idx -> token maps."""
    token_to_idx = {}
    idx_to_token = {}

    for idx, token in enumerate(set(tokens)):
        token_to_idx[token] = idx
        idx_to_token[idx] = token

    return token_to_idx, idx_to_token

def one_hot_encode(token_idx: int, vocabulary_size: int):
    """Create a vector the size of the vocabulary, set token idx to 1."""
    res = [0] * vocabulary_size
    res[token_idx] = 1
    return res

def concat(*iterables):
    for iterable in iterables:
        yield from iterable

def generate_training_data(tokens: list[str], token_to_idx: dict[str, int], window: int):
    X = []
    y = []
    n_tokens = len(tokens)

    for i in range(n_tokens):
        idx = concat(
            range(max(0, i - window), i),
            range(i, min(n_tokens, i + window + i))
        )

        for j in idx:
            if i == j:
                continue
            X.append(one_hot_encode(token_to_idx[tokens[i]], len(token_to_idx)))
            y.append(one_hot_encode(token_to_idx[tokens[j]], len(token_to_idx)))

    return np.asarray(X), np.asarray(y)


tokens = tokenize(sample_text)
token_to_idx, idx_to_token = generate_mappings(tokens)
print("Size of vocabulary: ", len(token_to_idx))
X, y = generate_training_data(tokens, token_to_idx, WINDOW_SIZE)
print(X.shape)

