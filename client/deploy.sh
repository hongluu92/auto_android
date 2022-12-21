#!/bin/bash
yarn build-prod
scp -r dist/* brv@34.87.62.8:/home/honglm1011/nerf/client/