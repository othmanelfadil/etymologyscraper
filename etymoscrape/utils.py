#UTILITY FUNCTIONS FOR LIGHT CLEANING
def stripper(text):
    return text.strip() if text and text.strip() else None

def cleaner(tnodes):
    text = " ".join(filter(None, (stripper(t) for t in tnodes)))
    return text.split("Related:")[0].strip()

