echo "Cloning the repository..."
git clone https://github.com/doctest/doctest.git
echo "Installing doctest..."
mkdir -p /usr/local/include/doctest
mv ./doctest/doctest/doctest.h /usr/local/include/doctest/doctest.h
echo "Cleaning up..."
rm -rf ./doctest
echo "Done!"