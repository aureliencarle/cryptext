#!/bin/sh

# Source pour la creation de ce script :
# https://kristuff.fr/blog/post/create-debian-package-a-pratical-guide

PACKAGE_DIR="deb-package"

# On s'assure que le dossier temporaire est *clean*
rm -rf $PACKAGE_DIR/deb-build
mkdir -p $PACKAGE_DIR/deb-build

# Création de la structure du paquet
mkdir -p $PACKAGE_DIR/deb-build/DEBIAN
mkdir -p $PACKAGE_DIR/deb-build/usr/lib/cryptext

# Copie des fichiers dans le répertoire source.
# D'abord le répertoire DEBIAN puis le contenu de l'application
cp $PACKAGE_DIR/deb-utils/control     $PACKAGE_DIR/deb-build/DEBIAN
cp $PACKAGE_DIR/deb-utils/postinst    $PACKAGE_DIR/deb-build/DEBIAN
cp $PACKAGE_DIR/deb-utils/postrm      $PACKAGE_DIR/deb-build/DEBIAN
cp -R src                  $PACKAGE_DIR/deb-build/usr/lib/cryptext
cp scripts/main.py              $PACKAGE_DIR/deb-build/usr/lib/cryptext/

# définit les attributs
find $PACKAGE_DIR/deb-build -type d -exec chmod 0755 {} \; # Dossiers
find $PACKAGE_DIR/deb-build -type f -exec chmod 0644 {} \; # Fichiers
find $PACKAGE_DIR/deb-build/usr/lib/cryptext/ -type f -exec chmod 0755 {} \; # exécutables

# scripts du paquet
chmod 755 $PACKAGE_DIR/deb-build/DEBIAN/postinst
chmod 755 $PACKAGE_DIR/deb-build/DEBIAN/postrm

# et finalement on construit le paquet avec --root-owner-group pour
# définir root en tant que propriétaire de l'ensemble du contenu du paquet
dpkg-deb --root-owner-group --build $PACKAGE_DIR/deb-build $PACKAGE_DIR/deb-dist