#!/bin/bash

# Copie du fichier corpus.xml
cp corpus.xml corpus_.xml

# Ajout d'une ligne "</pages>" au fichier
echo "</pages>" >> corpus_.xml

# Exécution du script python
python3 src/collector.py

# Suppression du fichier corpus_.xml
rm corpus_.xml

