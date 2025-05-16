import nltk
from nltk import word_tokenize, pos_tag, ne_chunk
from nltk.tree import Tree

# Download NLTK resources
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('words')
nltk.download('date')

def extract_named_entities(text):
    entities = {'PERSON': [], 'ORGANIZATION': [], 'GPE': [], 'DATE': []}
    sentences = nltk.sent_tokenize(text)

    for sentence in sentences:
        tokens = word_tokenize(sentence)
        tagged = pos_tag(tokens)
        chunked = ne_chunk(tagged)

        current_chunk = []
        current_label = None

        for subtree in chunked:
            if isinstance(subtree, Tree):
                label = subtree.label()
                entity = " ".join(token for token, pos in subtree)

                # Fix misclassifications
                if label == 'PERSON' and any(word in entity.lower() for word in ['inc', 'ltd', 'corporation']):
                    label = 'ORGANIZATION'

                if label in entities:
                    entities[label].append(entity)

    # Remove duplicates
    for key in entities:
        entities[key] = list(set(entities[key]))

    return entities

# Example document
document = """
SpaceX Inc was founded by Elon Musk in the United States on April 1, 1976.
They launched the iPhone in 2007. The headquarters is located in Cupertino, California.
"""

# Extract and print results
results = extract_named_entities(document)
print("Named Entities Found:")
for category, names in results.items():
    print(f"{category}: {names}")

