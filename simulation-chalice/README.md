# aws lambda performance tests

This repository contains code that will allow you to run some performance tests against aws lambda. You'll need `chalice` to provision everything. The chalice app will have an endpoint that will sleep "n" seconds. We use it to simulate a job that needs to heavily compute.

From this folder, you merely need to type the following to deploy (obviously you need `chalice` installed):

```
chalice deploy
```

This will give you a link, which you can use to update the `knock.py` file. You'll want to change this bit.

```
def make_url(sleep_time=1, uniq_id="none"):
    return f"https://l9bvun2xk5.execute-api.eu-west-1.amazonaws.com/api/sleep/{sleep_time}/{uniq_id}"
```

With this configured you can now fire up async python requests from the command line. To be able to run it you'll need `fire` and `aiohttp`. Try it out!

```
python3 knock.py ping
python3 knock.py run-batch --n=50 --sleep_time=1
python3 knock.py run-batch --min_requests=50 --max_requests=1000 --stepsize=20 --sleep_time=1
```

## Pretty charts.

You can use the `tee` command line to write your stats to a file.

```
python3 knock.py run-batch 3000 2 | tee -a <filepath>.csv
```

This R-code will allow you to make pretty plots.

```
library(tidyverse)

df <- read_csv("<filepath>", col_names = c("requests","total_time","ip_adr","starttime_host","endtime_host","request_id", "batch_id"))

ggplot() +
  geom_point(data=df, aes(starttime_host, ip_adr), size=0.5, colour="blue") +
  geom_point(data=df, aes(endtime_host, ip_adr), size=0.5, colour="red")
```
