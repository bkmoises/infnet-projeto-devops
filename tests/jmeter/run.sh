#!/bin/bash

mkdir -p output

docker build -t jmeter-test .

docker run --rm -v $(pwd)/output:/tests/report \
  -v $(pwd)/stress_test.jmx:/tests/stress_test.jmx \
  --network="host" \
  jmeter-test \
  -n -t /tests/stress_test.jmx -l /tests/result.jtl -e -o /tests/report
