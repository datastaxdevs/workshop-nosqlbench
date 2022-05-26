# Benchmark your Astra DB with NoSQLBench

[![Gitpod hands-on](https://img.shields.io/badge/Gitpod-hands--on-blue?logo=gitpod)](https://gitpod.io/#https://github.com/datastaxdevs/workshop-nosqlbench)
[![License Apache2](https://img.shields.io/hexpm/l/plug.svg)](http://www.apache.org/licenses/LICENSE-2.0)
[![Discord](https://img.shields.io/discord/685554030159593522)](https://discord.com/widget?id=685554030159593522&theme=dark)

<img src="images/nosqlbench_banner.png?raw=true" />

Time: *2 hours*. Difficulty: *Intermediate*. [Start Building!](#create-your-astra-db-instance)

The goal of this workshop is to get you familiar with the powerful and versatile
tool **[`NoSQLBench`](https://docs.nosqlbench.io/)**. With that, you can perform
**industry-grade, robust benchmarks
aimed at several (distributed) target systems, especially NoSQL databases**.

Today you'll be benchmarking Astra DB, a database-as-a-service built on top of
Apache Cassandra. Along the way, you will learn the basics of NoSQLBench.

In this repository you will find all material and references you need:

- [Slide deck](#)
- [NoSQLBench Discord](https://discord.gg/dBHRakusMN)
- [NoSQLBench homepage](https://docs.nosqlbench.io/)
- [Workshop video](#)
- [Exercises](#create-your-astra-db-instance)
- [Step-by-step guide](#before-you-start)
- [DataStaxDevs Discord server](https://dtsx.io/discord) to keep in touch with us
- [Our Q&A forum](https://community.datastax.com/) (think StackOverflow for Cassandra and all things DataStax)

#### Table of Contents

1. [Before you start](#before-you-start)
2. [Create your Astra DB instance](#create-your-astra-db-instance)
3. [Launch Gitpod and setup NoSQLBench](#launch-gitpod-and-setup-nosqlbench)
4. [Run benchmarks](#run-benchmarks)
5. [Workloads](#workloads)
6. [Homework assignment](#homework-assignment)



## Before you start

<img src="images/attention.png?raw=true" width="80" align="left" />

> **Heads up**: these instructions are available in two forms:
> a short and to-the-point one (_this one_),
> with just the useful commands if you are watching us live; and
> a [longer one](extended_README.md),
> with lots of explanations and details, designed for those who follow this workshop
> at their own pace. Please choose what best suits you!



### FAQ

- What are the prerequisites?

> This workshop is aimed at data architects, solution architects, developers, or anybody who
> wants to get serious about measuring the performance of their data-intensive system.
> You should know what a (distributed) database is, and have a general understanding of the
> challenges of communicating over a network.

- Do I need to install a database or anything on my machine?

> No, no need to install anything. You will do everything in the browser.
> (That being said, the knowledge you gain today will probably be best put to
> use once you install NoSQLBench on some client machine to run tests.)

> You can also choose to work on your machine instead of using Gitpod: there's
> no problem with that, just a few setup and operational changes to keep
> in mind. We will not provide live support in this case, though,
> assuming you know what you are doing.

- Is there anything to pay?

> **No.** All materials, services and software used in this workshop is _free_.

- Do you cover NoSQLBench 4 or 5?

> Ah, I see you are a connoisseur. We focus on the newly-release **NoSQLBench 5**,
> but we provide tips and remarks aimed at those still using nb4.

### Homework

<img src="images/nosqlbench_badge_artwork.png?raw=true" width="200" align="right" />

To complete the workshop and get a verified "NoSQLBench" badge,
follow these instructions:

1. Do the hands-on practice, either during the workshop or by following the instructions in this README;
2. (optional) Complete the "Lab" assignment as detailed [here](homework/homework.md);
3. Fill the submission form [here](#). Answer the theory questions and (optionally) provide a _screenshot_ of the completed "Lab" part;
4. give us a few days to process your submission: you should receive your well-earned badge in your email inbox!



## Create your Astra DB instance

First you must create a database: an instance of Astra DB, which
you will then benchmark with NoSQLBench.

> Don't worry, you will create
> it within the "Free Tier", which offers quite a generous free
> allowance in terms of monthly I/O (about 40M operations per month)
> and storage (80 GB).

You need to:

- create an Astra DB instance [as explained here](https://awesome-astra.github.io/docs/pages/astra/create-instance/#c-procedure), with **database name** = `workshops` and **keyspace name** = `nbkeyspace`;
- generate and download a Secure Connect Bundle [as explained here](https://awesome-astra.github.io/docs/pages/astra/download-scb/#c-procedure);
- generate and retrieve a DB Token [as explained here](https://awesome-astra.github.io/docs/pages/astra/create-token/#c-procedure). **Important**: use the role _"DB Administrator"_ when creating the token.

Moreover, keep the Astra DB dashboard open: it will be useful later. In particular the
Health tab and the CQL Console.



## Launch Gitpod and setup NoSQLBench

**Ctrl-click on the Gitpod button below** to spawn your very own environment + IDE:

[![Open in Gitpod](https://gitpod.io/button/open-in-gitpod.svg)](https://gitpod.io/#https://github.com/datastaxdevs/workshop-nosqlbench)

In a few minutes, a full IDE will be ready in your browser, with a file
explorer on the left, a file editor on the top, and a console (`bash`) below it.



### Install NoSQLBench

To download NoSQLBench, type or paste this command in your Gitpod console:
```bash
curl -L -O https://github.com/nosqlbench/nosqlbench/releases/latest/download/nb
```

then make it executable and move it to a better place:
```bash
chmod +x nb
sudo mv nb /usr/local/bin/
```

Ok, now check that the program starts: invoking
```bash
nb --version
```
should output the program version (something like `4.15.91` or higher).


#### Version used

This workshop is built for the newly-released NoSQLBench 5.


### Upload the Secure Connect Bundle to Gitpod


Locate, with the file explorer on your computer, the bundle file that
you downloaded earlier (it should be called
`secure-connect-workshops.zip`)
and simply **drag-and-drop** it to the file navigator panel
("Explorer") on the left of the Gitpod view.

<details><summary>Show me</summary>
    <img src="https://github.com/datastaxdevs/workshop-nosqlbench/raw/main/images/gitpod_uploading_bundle_1_annotated.png?raw=true" />
</details>

Once you drop it you will see it listed in the file explorer itself.
As a check, you can issue the command
```bash
ls /workspace/workshop-nosqlbench/secure*zip -lh
```

so that you get the _absolute path to your bundle file_ (and also verify that it is
the correct size, about 12-13 KB).

<details><summary>Show me</summary>
    <img src="https://github.com/datastaxdevs/workshop-nosqlbench/raw/main/images/gitpod_uploading_bundle_2b_annotated.png?raw=true" />
</details>


### Configure the Astra DB parameters


Copy the provided template file to a new one and open it in the Gitpod
file editor:
```bash
cp .env.sample .env
gp open .env
# (you can also simply locate the file
#  in the Explorer and click on it)
```

Insert the "Client ID" and "Client Secret" of the DB Token you created earlier
and, if necessary, adjust the other variables.

<details><summary>Show me what the .env file would look like</summary>
    <img src="https://github.com/datastaxdevs/workshop-nosqlbench/raw/main/images/dotenv2.png?raw=true" />
</details>

Now, source this file to make the definitions therein available to this shell:
```bash
. .env
```

To check that the file has been sourced, you can try with:
```bash
echo ${ASTRA_DB_KEYSPACE_NAME}
```

and make sure the output is not an empty line.

(Note that you will have to source the file in any new shell you plan to use).



## Run benchmarks

Everything is set to start running the tool.


### A short dry run


Try launching this very short "dry-run benchmark", that instead of actually
reaching the database simply prints a series of CQL statements to the console
(as specified by the `driver=stdout` parameter):

```bash
nb cql-keyvalue astra                   \
    driver=stdout                       \
    main-cycles=10                      \
    rampup-cycles=10                    \
    keyspace=${ASTRA_DB_KEYSPACE_NAME}
```

You will see 21 (fully-formed, valid CQL) statements being printed:
one `CREATE TABLE`, then ten `INSERT`s
and then another ten between `SELECT`s and further `INSERT`s.


Now re-launch the above dry run and look for differences in the output:

```bash
nb cql-keyvalue astra                   \
    driver=stdout                       \
    main-cycles=10                      \
    rampup-cycles=10                    \
    keyspace=${ASTRA_DB_KEYSPACE_NAME}
```

is the output identical to the previous run down to the actual "random" values?

You can also peek at the `logs` directory now: it is created automatically and
populated with some information from the benchmark at each execution of `nb`.


### Benchmark your Astra DB

It is now time to start hitting the database!

This time you will run with `driver=cql` to actually reach the database:
for that to work, you will provide all connections parameters set up earlier.


The next run will ask NoSQLBench to perform a substantial amount of operations,
in order to collect enough statistical support for the results.


Here is the full command to launch:

```bash
nb cql-keyvalue                                                           \
    astra                                                                 \
    username=${ASTRA_DB_CLIENT_ID}                                        \
    password=${ASTRA_DB_CLIENT_SECRET}                                    \
    secureconnectbundle=${ASTRA_DB_BUNDLE_PATH}                           \
    keyspace=${ASTRA_DB_KEYSPACE_NAME}                                    \
    cyclerate=50                                                          \
    driver=cql                                                            \
    rampup-cycles=15000                                                   \
    main-cycles=15000                                                     \
    errors=count                                                          \
    --progress console:5s                                                 \
    --log-histograms 'histogram_hdr_data.log:.*.main.result*:20s'         \
    --log-histostats 'hdrstats.log:.*.main.result.*:20s'
```

<details><summary>Show me the command breakdown</summary>

Note that some of the parameters (e.g. `keyspace`) are workload-specific.

| command                   | meaning                                      |
|---------------------------|----------------------------------------------|
| `cql-keyvalue`            | workload
| `astra`                   | scenario
| `username`                | authentication
| `password`                | authentication
| `secureconnectbundle`     | Astra DB connection parameters
| `keyspace`                | target keyspace
| `cyclerate`               | rate-limiting (cycles per second)
| `driver=cql`              | driver to use (CQL, for AstraDB/Cassandra)
| `rampup-cycles`           | how many operations in the "rampup" phase
| `main-cycles`             | how many operations in the "main" phase
| `errors`                  | behaviour if errors occur during benchmarking
| `--progress console`      | frequency of console prints
| `--log-histograms`        | write data to HDR file (see later)
| `--log-histostats`        | write some more stats to this file

This way of invoking `nb`, the ["named scenario"](https://docs.nosqlbench.io/docs/workloads_101/11-named-scenarios/)
way, is not the only one: it is also possible to have a finer-grained control over what activities should
run with a full-fledged [CLI scripting](https://docs.nosqlbench.io/docs/reference/cli-scripting/) syntax.

</details>


The benchmark should last about ten minutes, with the progress being
printed on the console as it proceeds.


While this runs, have a look around.

#### Database contents

Now it's time to find out _what is actually being written to the database_.

Choose your database in the Astra main dashboard and click on it;
next, go to the "CQL Console" tab in the main panel. In a few seconds the
console will open in your browser, already connected to your database and
waiting for your input.

<details><summary>Show me how to get to the CQL Console in Astra</summary>
    <img src="https://github.com/datastaxdevs/workshop-nosqlbench/raw/main/images/astra_get_to_cql_console.gif?raw=true" />
</details>


Start by telling the console that you will be using the `nbkeyspace` keyspace:
```
USE nbkeyspace;
```

Check what tables have been created by NoSQLBench in this keyspace:
```
DESC TABLES;
```

You should see table `keyvalue` listed as the sole output.
Look at a a few lines from this table:
```
SELECT * FROM keyvalue LIMIT 20;
```

<details><summary>Show me what the output looks like</summary>
    <img src="https://github.com/datastaxdevs/workshop-nosqlbench/raw/main/images/select_cql.png?raw=true" />
</details>

Ok, mystery solved. It looks like the table contains simple key-value pairs,
with two columns seemingly of numeric type. Check with:
```
DESC TABLE keyvalue;
```

Oh, looks like both the key and the value columns are of type `TEXT`:
good for adapting this ready-made benchmark to other key/value stores.

<details><summary>Show me what the output looks like</summary>
    <img src="https://github.com/datastaxdevs/workshop-nosqlbench/raw/main/images/desctable_cql.png?raw=true" />
</details>

#### Database health


Locate your database in the Astra main dashboard and click on it;
next, go to the "Health" tab in the main panel. You will see what essentially
is a Grafana dashboard, with a handful of plots being displayed within the
tab - all related to how the database is performing in terms of reads and writes.

<details><summary>Show me the Database Health tab in Astra UI</summary>
    <img src="https://github.com/datastaxdevs/workshop-nosqlbench/raw/main/images/astra_db_health2_annotated.png?raw=true" />
</details>

Check the operations per second from the "Requests Combined" plot;
then have a look at the "Write Latency" and "Read Latency" plots
and take note of some of the percentiles shown there.

<details><summary>Show me "sample values" one could read from the graph</summary>

Below is a real-life example of the values that could result from a `cql-keyvalue`
benchmark session in the _main_ phase:

| Percentile  | Write Latency  | Read Latency   |
|-------------|----------------|----------------|
| P50         | 709     _µs_   |  935     _µs_  |
| P75         | 831     _µs_   |    1.31  _ms_  |
| P90         | 904     _µs_   |    1.53  _ms_  |
| P95         |   1.04  _ms_   |    1.77  _ms_  |
| P99         |   2.45  _ms_   |   15.6   _ms_  |

</details>


#### Final summary

When the benchmark has finished, open the latest `*.summary` file and look
for `cqlkeyvalue_astra_main.result-success`.

Under that metric title, you will see something similar to:

```
cqlkeyvalue_astra_main.result-success
             count = 15000
         mean rate = 50.00 calls/second
     1-minute rate = 49.94 calls/second
     5-minute rate = 50.29 calls/second
    15-minute rate = 50.57 calls/second
```


#### Additional "histostats" datafile

Use this script to generate a graph of the data collected as "histostats":

```bash
./hdr_tool/histostats_quick_plotter.py \
    hdrstats.log \
    -m cqlkeyvalue_astra_main.result-success
```

and then open, in the Gitpod editor, the `hdrstats.png` image just created.

<details><summary>Show me the generated "histostats" plot</summary>
    <img src="https://github.com/datastaxdevs/workshop-nosqlbench/raw/main/images/histostats_plot3.png?raw=true" width="360" />
</details>

> The version of the plotter script included in this repo is for **educational purposes only**:
> for general use, please head to
> [the official release page](https://pypi.org/project/nb-hdr-plotter/).

The timings will be larger than those from the Astra health tab: indeed,
these are "as seen on the client side" and include more network hops.


#### HDR extensive histogram data

Use this script to generate plots from the detailed "HDR histogram data"
generated during the benchmark:

```bash
./hdr_tool/hdr_tool.py \
    histogram_hdr_data.log \
    -b -c -s \
    -p SampleData \
    -m cqlkeyvalue_astra_main.result-success
```


<details><summary>Show me the plots generated by the HDR file</summary>

<img src="https://github.com/datastaxdevs/workshop-nosqlbench/raw/main/images/hdr_baseplot2.png?raw=true" width="260"/>

<img src="https://github.com/datastaxdevs/workshop-nosqlbench/raw/main/images/hdr_stabilityplot2.png?raw=true" width="260"/>

<img src="https://github.com/datastaxdevs/workshop-nosqlbench/raw/main/images/hdr_percentileplot2.png?raw=true" width="260"/>

</details>

> The version of the plotter script included in this repo is for **educational purposes only**:
> for general use, please head to
> [the official release page](https://pypi.org/project/nb-hdr-plotter/).

Again, the timings are larger than those found on the Astra health tab
(i.e. on server-side): these
measurements are reported "as seen by the testing client".


### Metrics, metrics, metrics

Launch a new benchmark, this time having NoSQLBench start a dockerized
Grafana/Prometheus stack for metrics (it will take a few more seconds to start):

```
nb cql-keyvalue                                                           \
    astra                                                                 \
    username=${ASTRA_DB_CLIENT_ID}                                        \
    password=${ASTRA_DB_CLIENT_SECRET}                                    \
    secureconnectbundle=${ASTRA_DB_BUNDLE_PATH}                           \
    keyspace=${ASTRA_DB_KEYSPACE_NAME}                                    \
    cyclerate=50                                                          \
    rampup-cycles=15000                                                   \
    main-cycles=15000                                                     \
    errors=count                                                          \
    --progress console:5s                                                 \
    --docker-metrics
```


<details><summary>Show me the run with Docker metrics</summary>
    <img src="https://github.com/datastaxdevs/workshop-nosqlbench/raw/main/images/grafana_startingdockermetrics.png?raw=true" />
</details>


#### Grafana dashboard

Reach the Grafana container in a new tab, with an URL that has `3000-`
in front of your Gitpod URL (e.g.
`https://3000-datastaxdevs-workshopnos-[...].gitpod.io`).

The default credentials to log in to Grafana are ... `admin/admin`. Once you're
in, don't bother to reset your password (click "Skip"). You'll get to the Grafana
landing page. Find the "Dashboards" icon in the leftmost menu bar and pick the
"Manage" menu item: finally, click on the "NB4 Dashboard" item you should see
listed there. Congratulations, you are seeing the data coming from NoSQLBench.

<details><summary>Show me how to get to the Grafana plots</summary>
    <img src="https://github.com/datastaxdevs/workshop-nosqlbench/raw/main/images/grafana_dashboard.gif?raw=true" />
</details>

> You may find it convenient to set the update frequency to something like 10
> seconds and the displayed time window to 5 minutes or so (upper-right controls).

The dashboard comprises several (interactive) plots, updated in real time.

<details><summary>Show me the dashboard contents</summary>
    <img src="https://github.com/datastaxdevs/workshop-nosqlbench/raw/main/images/grafana_plots.png?raw=true" />
</details>


#### A glance at Prometheus

To reach the Prometheus container, which handles the "raw" data behind Grafana,
open a modified URL (this time with `9090-`) in a new tab.

<details><summary>Show me the Prometheus UI</summary>
    <img src="https://github.com/datastaxdevs/workshop-nosqlbench/raw/main/images/prometheus2.gif?raw=true" />
</details>

Click on the "world" icon next to the "Execute" button in the search bar:
in the dialog that appears you can look for specific metrics.
Try to look for `result_success` and confirm, then click "Execute".


> **Tip:** switch to the "Graph" view for a more immediate visualization.
> The graphs display "raw" data, hence are in units of nanoseconds.

To make sense of the (heterogeneous) results, some filtering is in order --
but we are not entering too much into the details of Prometheus here.

Just to pique your interest, try pasting these examples and click "Execute":

```
# filtering by metadata
{__name__="result_success", type="pctile", alias=~".*main.*"}

# aggregation
avg_over_time({__name__="result_success", type="pctile", alias=~".*main.*"}[10m])

# another aggregation, + filtering
max_over_time({__name__="result_success", type="pctile", alias=~".*main.*"}[10m])
```


## Workloads

This part is about how workloads are defined.

> **Tip**: feel free to interrupt the previous benchmark, if it still runs,
> with Ctrl-C. You won't need it anymore.

### Inspect "cql-keyvalue"

Ask NoSQLBench to dump to a file the `yaml` defining the workload
you just ran:

```bash
    nb --copy cql-keyvalue
```

(you can also get a comprehensive list of all available workloads with
`nb --list-workloads`, by the way, and a more fine-grained output with
`nb --list-scenarios`.)

A file `cql-keyvalue.yaml` is created in the working directory.
You can open it (clicking on it in the Gitpod explorer or by running
`gp open cql-keyvalue.yaml`).

Have a look at the file and try to identify its structure and the various
phases the benchmark is organized into.

### Play with workloads

A good way to understand workload construction is to start from simple ones.

To run the following examples please go to the appropriate subdirectory:
```
cd workloads
```

#### Example 1: talking about food

Run the first example (and then look at the corresponding
`simple-workload.yaml`) with:

```
nb run driver=stdout workload=simple-workload cycles=12
```

Look at how _bindings_ connect the sequence of operations to "execute"
(in this case, simply print on screen) with the data to be used in
them.

#### Example 2: animal meeting

Run the second example, which is an example of structuring a workload
in _phases_ (and then open `workload-with-phases.yaml`):

```
nb workload-with-phases default driver=stdout
```

Notable features of this workload are its multi-phase structure
(a nearly universal feature of actual benchmarks), the use
of the `ratio` parameter, and the usage of template parameters in the
definition.



## Homework assignment

The "Lab" part of the homework, which requires you to finalize
a workload `yaml` and make it work according to specifications,
is detailed on [this page](homework/homework.md).
