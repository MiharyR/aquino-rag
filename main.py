import pymupdf
import re


path = 'somme_theologique_72a102.pdf'


# Extract pdf
doc = pymupdf.open(path)
text = "\n".join(page.get_text() for page in doc)
doc.close()

# découpage du texte d'après motif de paragraphe
paragraphes = re.split('QUESTION |Article ',text)


# affiche extrait n°2 :
print(paragraphes[1])


