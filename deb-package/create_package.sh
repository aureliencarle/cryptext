#!/bin/sh

# Source pour la creation de ce script :
# https://kristuff.fr/blog/post/create-debian-package-a-pratical-guide


# On s'assure que le dossier temporaire est *clean*
rm -rf deb-package/deb-build
mkdir -p deb-package/deb-build

# Création de la structure du paquet
mkdir -p deb-package/deb-build/DEBIAN
mkdir -p deb-package/deb-build/usr/lib/cryptext

# Copie des fichiers dans le répertoire source.
# D'abord le répertoire DEBIAN puis le contenu de l'application
cp deb-package/deb-utils/control     deb-package/deb-build/DEBIAN
cp deb-package/deb-utils/postinst    deb-package/deb-build/DEBIAN
cp deb-package/deb-utils/postrm      deb-package/deb-build/DEBIAN
cp -R src                  deb-package/deb-build/usr/lib/cryptext
cp cryptext.py              deb-package/deb-build/usr/lib/cryptext/

# définit les attributs
find deb-package/deb-build -type d -exec chmod 0755 {} \; # Dossiers
find deb-package/deb-build -type f -exec chmod 0644 {} \; # Fichiers
find deb-package/deb-build/usr/lib/cryptext/ -type f -exec chmod 0755 {} \; # exécutables

# scripts du paquet
chmod 755 deb-package/deb-build/DEBIAN/postinst
chmod 755 deb-package/deb-build/DEBIAN/postrm

# et finalement on construit le paquet avec --root-owner-group pour
# définir root en tant que propriétaire de l'ensemble du contenu du paquet
dpkg-deb --root-owner-group --build deb-package/deb-build deb-package/deb-dist