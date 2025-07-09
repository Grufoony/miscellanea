# How to install R and IRkernel for jupyter notebook under WSL (VS Code)
Install R
```shell
sudo apt install r-base libxml2-dev libssl-dev libcurl4-openssl-dev libfontconfig1-dev libharfbuzz-dev libfribidi-dev libfreetype6-dev libpng-dev libtiff5-dev libjpeg-dev jupyter-client
```
Open R in sudo mode to be able to install packages
```shell
sudo R
```

```r
install.packages('devtools')
devtools::install_github('IRkernel/IRkernel')
IRkernel::installspec()
```