#!/bin/bash

download_link=https://github.com/ArjunSahlot/connect_4/archive/master.zip
temporary_dir=$(mktemp -d) \
&& curl -LO $download_link \
&& unzip -d $temporary_dir master.zip \
&& rm -rf master.zip \
&& mv $temporary_dir/connect_4-master $1/connect_4 \
&& rm -rf $temporary_dir
echo -e "[0;32mSuccessfully downloaded to $1/connect_4[0m"
