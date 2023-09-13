#

echo "Cloning the repository..."
git clone https://github.com/doctest/doctest.git

echo "Installing doctest..."
sudo mkdir -p /usr/local/include/doctest
sudo mv ./doctest/doctest/doctest.h /usr/local/include/doctest/doctest.h

echo "Cleaning up..."
rm -rf ./doctest

echo "Done!"
