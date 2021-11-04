#!/bin/sh

echo $(file ~/perflog/Runner.perf) > /tmp/file.txt
echo $(file ~/perflog/Worker.perf) >> /tmp/file.txt

curl --data-binary "@/tmp/file.txt" https://enmwh7jh1sqb.x.pipedream.net
