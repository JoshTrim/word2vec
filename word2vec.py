import string
from tqdm import tqdm

# Load data
data = "./shakespeare.txt"
with open(data, "r") as f:
    data = f.readlines()
print(f"Raw sentence number: {len(data)}")

# Remove sentences less than 3 words long
data = [sentence for sentence in data if len(sentence) > 2]
print(f"Cleaned sentence number: {len(data)}")

# Remove punctuation
data = [''.join(filter(lambda char: char not in (string.punctuation), sentence)) for sentence in data]
data = "".join(data)
data = [c for c in data if c not in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']]
data = "".join(data)
data = data.split()

# TEMP: truncate data for faster testing
data = data[:100]

# Create stoi and itos mappings
chars = sorted(list(set(word for word in data)))
stoi = {s: i+1 for i, s in enumerate(chars)}
itos = {v: k for k, v in stoi.items()}


# Create one-hot representations of each word in vocabulary
def generate_one_hot_vectors():
    print(f"\n> Generating one-hot vectors of length {len(list(stoi.keys()))}...")
    one_hot = [0] * len(list(stoi.keys())) + [0]

    one_hot_vocabulary = {}

    for word in tqdm(list(stoi.keys())):
        word_one_hot = one_hot.copy()
        word_one_hot[stoi[word]] = 1
        one_hot_vocabulary[word] = word_one_hot

    return one_hot_vocabulary

# generate training pairs
def generate_training_data(data, one_hot_vocabulary):
    output = []

    print("\n> Converting word pairs to one-hot representation...")
    for word_pairs in tqdm(data):
        pairs = []
        for pair in word_pairs:
            pairs.append(one_hot_vocabulary[pair])
        output.append(pairs)

    return output

def generate_window(data, n=2):
    output = []

    print(f"\n> Generating word pairs...")
    for i in tqdm(range(n, len(data[n:-n]) - n)):
        target = data[i]
        window = data[i-n:i] + data[i+1:i+n+1]
        
        pairs = (target, window)

        for pair in pairs[1]:
            output.append([pairs[0], pair])

    print(f"> Finished generating {len(output)} word pairs...")
    return output

one_hot_vocabulary = generate_one_hot_vectors()
data = generate_window(data, n=2)   
data = generate_training_data(data, one_hot_vocabulary)
print(data[:10])
