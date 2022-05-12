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

- [slide deck](#)
- [NoSQLBench Discord](https://discord.gg/dBHRakusMN)
- [NoSQLBench homepage](https://docs.nosqlbench.io/)
- [workshop video](#)
- [exercises](#create-your-astra-db-instance)
- [step-by-step guide](#before-you-start)
- [DataStaxDevs Discord server](https://dtsx.io/discord) to keep in touch with us
- [our Q&A forum](https://community.datastax.com/) (think StackOverflow for Cassandra and all things DataStax)

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
<!-- 2L IF long -->
> a [short and to-the-point](README.md) one,
<!-- 2L ELIF short -->
> a short and to-the-point one (_this one_),
<!-- 2L ENDIF -->
> with just the useful commands if you are watching us live; and
<!-- 2L IF long -->
> a longer one (_this one_),
<!-- 2L ELIF short -->
> a [longer one](extended_README.md),
<!-- 2L ENDIF -->
> with lots of explanations and details, designed for those who follow this workshop
> at their own pace. Please choose what best suits you!

<!-- 2L IF long -->
If you are not watching us live, please look at the provided presentation material
for more coverage of the theory part. There, you will learn more about:

- benchmarking a database;
- Apache Cassandra™, a distributed NoSQL highly available database;
- Astra DB, a database-as-a-service in the cloud, built on Cassandra, ready to use in minutes for free with a few clicks;
- the main features and general principles behind the NoSQLBench benchmarking tool.
<!-- 2L ENDIF -->


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

<!-- 2L IF long -->
Gitpod is an IDE in the cloud (modeled after VSCode). It comes with a full
"virtual machine" (actually a Kubernetes-managed container), which you will
use as if it were your own computer (e.g. downloading files, executing programs
and scripts, even launching containers from within it).

Now **ctrl-click on the Gitpod button below**. It will:

- spawn your own Gitpod container;
- clone this repository in it;
- preinstall the required dependencies.

_Note that you may have to authenticate through Github in the process._
(Also make sure you "Open in new tab" to keep this readme open alongside.)
<!-- 2L ELIF short -->
**Ctrl-click on the Gitpod button below** to spawn your very own environment + IDE:
<!-- 2L ENDIF -->

[![Open in Gitpod](https://gitpod.io/button/open-in-gitpod.svg)](https://gitpod.io/#https://github.com/datastaxdevs/workshop-nosqlbench)

In a few minutes, a full IDE will be ready in your browser, with a file
explorer on the left, a file editor on the top, and a console (`bash`) below it.

<!-- 2L IF long -->
> There are many more other features, probably familiar to those who have
> experience with VSCode. Feel free to play around a bit!
<!-- 2L ENDIF -->

### Install NoSQLBench

<!-- 2L IF long -->
Download the latest stable version of NoSQLBench to your Gitpod environment.
First make sure you are in the top-level repository directory with your
Gitpod console: type `pwd` and see if the output is `/workspace/workshop-nosqlbench`.

Please download the "Linux binary" distribution of NoSQLBench:
as instructed [here](https://github.com/nosqlbench/nosqlbench/blob/main/DOWNLOADS.md),
you can obtain the latest stable binary (it's a few hundred megabytes) with
<!-- 2L ELIF short -->
To download NoSQLBench, type or paste this command in your Gitpod console:
<!-- 2L ENDIF -->
```bash
curl -L -O https://github.com/nosqlbench/nosqlbench/releases/latest/download/nb
```

<!-- 2L IF long -->
and, when the download is finished, make it executable and move it,
out of convenience, to a directory which is part of the search path:
<!-- 2L ELIF short -->
then make it executable and move it to a better place:
<!-- 2L ENDIF -->
```bash
chmod +x nb
sudo mv nb /usr/local/bin/
```

Ok, now check that the program starts: invoking
```bash
nb --version
```
should output the program version (something like `4.15.91` or higher).

<!-- 2L IF long -->
> You will probably see a message like `Picked up JAVA_TOOL_OPTIONS ...` when
> launching `nb`. You can ignore it: it is a consequence of some settings by
> Gitpod and does not have to do with NoSQLBench itself.

> Note that if your Gitpod instance gets hibernated (which happens after some
> inactive time) and you restart it later, recall that only the contents
> of `/workspace` will be restored: hence, you would have to repeat the
> installation.

<!-- 2L ENDIF -->

### Upload the Secure Connect Bundle to Gitpod

<!-- 2L IF long -->
NoSQLBench will need to connect to your Astra DB database: to do so, the
Secure Connect Bundle zip file must be uploaded
to your Gitpod environment.
<!-- 2L ENDIF -->

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
<!-- 2L IF long -->
As an aside, note that, as per best practices with NoSQLBench, (relative)
paths to files would start with `./`.
<!-- 2L ENDIF -->

<details><summary>Show me</summary>
    <img src="https://github.com/datastaxdevs/workshop-nosqlbench/raw/main/images/gitpod_uploading_bundle_2b_annotated.png?raw=true" />
</details>


### Configure the Astra DB parameters

<!-- 2L IF long -->
If you want NoSQLBench to be able to access the Astra DB instance, you have to pass it
the required connection parameters and secrets. To do so, set up
a `.env` file, which will make your life easier later.
<!-- 2L ENDIF -->

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

<!-- 2L IF long -->
From a user's perspective, NoSQLBench sends operations (e.g. reads, writes)
to the target system (e.g. a database) and record how the latter responds
(service time, number of ops/second and failures).
<!-- 2L ENDIF -->

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

<!-- 2L IF long -->
These three blocks correspond
to the three phases defined in the `cql-keyvalue` _workload_: **schema**,
**rampup** and **main**. The most relevant benchmark results are from the
**main** phase, which mimics the kind of load the database would be subject to
when operating normally.

> For most workloads, a three-phase structure is the most reasonable choice: first
> the schema is set up, then an amount of data is poured in, and finally
> the target system is subject to a mixture of reads and writes. The third
> and last phase (_main_) in most cases is designed to generate contention on the server, which is
> the very situation one usually wants to put to test.

<!-- 2L ENDIF -->

Now re-launch the above dry run and look for differences in the output:

```bash
nb cql-keyvalue astra                   \
    driver=stdout                       \
    main-cycles=10                      \
    rampup-cycles=10                    \
    keyspace=${ASTRA_DB_KEYSPACE_NAME}
```

<!-- 2L IF long -->
do you notice that the output of this second run is identical to the first,
down to the actual values used in the `INSERT`s and `DELETE`s?
Indeed an important goal for any benchmark is its _reproducibility_:
here, among other
consequences, this means that the operations (their progression and contents alike)
should be completely determined with no trace of actual randomness.
<!-- 2L ELIF short -->
is the output identical to the previous run down to the actual "random" values?
<!-- 2L ENDIF -->

You can also peek at the `logs` directory now: it is created automatically and
populated with some information from the benchmark at each execution of `nb`.


### Benchmark your Astra DB

It is now time to start hitting the database!
<!-- 2L IF long -->
What you launched earlier is the `cql-keyvalue` _workload_, one of the several
ready-to-use workloads included with NoSQLBench.
In particular, you ran the `astra` _scenario_, which determines a particular
way the workload is to be unfolded and executed.
<!-- 2L ENDIF -->

This time you will run with `driver=cql` to actually reach the database:
for that to work, you will provide all connections parameters set up earlier.

<!-- 2L IF long -->
> Note: for this workload, as you could check by examining its definition
> (see the _Inspect "cql-keyvalue"_ section below), you could leave the driver
> specification out since `cql` is the default.

<!-- 2L ENDIF -->

The next run will ask NoSQLBench to perform a substantial amount of operations,
in order to collect enough statistical support for the results.

<!-- 2L IF long -->
> On the other hand, you will rate-limit the operations sent to the database
> (with the `cyclerate` parameter). This is mainly because often the goal
> of a benchmark is to verify whether the system can withstand
> a _known, controlled_ workload;
> but in this case there are also other practical reasons: (1) you don't want to consume
> too much of your Free Tier monthly allowance in this "functional demo"; moreover,
> (2) if you are running on the Free Tier you may otherwise hit the
> guardrails and the performance limitations specific to free-tier Astra databases.
 
<!-- 2L ENDIF -->

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

<!-- 2L IF long -->
> _Note_: if you were targeting a "regular" Cassandra instance (as opposed to Astra DB),
> the command line above would change a little: the scenario would be `default`,
> you would need to provide a parameter such as `hosts=192.168.1.1,192.168.1.2`,
> and there would be _no_ `secureconnectbundle` parameter. As for username and password,
> ... well, that depends on how the Cassandra cluster is configured.
> Moreover, in the next steps, you will have to look at metric with "default"
> in their name instead of "astra".
> Note that NoSQLBench uses the very same CQL drivers to
> access the database, regardless of whether Astra DB or a Cassandra cluster.

<!-- 2L ENDIF -->

<!-- 2L IF long -->
The above command should last approximately ten minutes, during which NoSQLBench
sends a constant stream of I/O operations to the database and collects timing
information on how it responds. You will see a **console output** keeping you
updated on the progress of the
currently-running phase (`schema`/`rampup`/`main`).
<!-- 2L ELIF short -->
The benchmark should last about ten minutes, with the progress being
printed on the console as it proceeds.
<!-- 2L ENDIF -->

<!-- 2L IF long -->
> If the execution fails with,
> `"Cannot construct cloud config from the cloudConfigUrl ..."`,
> chances are your (free-tier) database is currently in
> [Standby status](https://docs.datastax.com/en/astra/docs/db-status.html#_standby).
> To resume it, open its Health tab or the CQL Console tab in the Astra DB UI
> and wait two or three minutes before retrying.

<!-- 2L ENDIF -->

While this runs, have a look around.

#### Database contents

<!-- 2L IF long -->
By this point, you may have a question:
_"but what is being written to the database, exactly?_

To find out, connect to the database and inspect the contents of the
keyspace. There are several ways one could connect to Astra DB:
using Cassandra drivers with most programming languages;
through the HTTP requests enabled by the Stargate Data API; or directly
with a client that "speaks" the CQL language.
Today you will make use of the **CQL Console** available in the browser
within the Astra UI.
<!-- 2L ELIF short -->
Now it's time to find out _what is actually being written to the database_.
<!-- 2L ENDIF -->

Choose your database in the Astra main dashboard and click on it;
next, go to the "CQL Console" tab in the main panel. In a few seconds the
console will open in your browser, already connected to your database and
waiting for your input.

<details><summary>Show me how to get to the CQL Console in Astra</summary>
    <img src="https://github.com/datastaxdevs/workshop-nosqlbench/raw/main/images/astra_get_to_cql_console.gif?raw=true" />
</details>

<!-- 2L IF long -->
> Commands entered in the CQL Console are terminated with a semicolon (`;`)
> and can span multiple lines. Run them with the `Enter` key. If you want to
> interrupt the command you are entering, hit `Ctrl-C` to be brought back
> to the prompt. See [here](https://docs.datastax.com/en/cql-oss/3.x/cql/cql_reference/cqlCommandsTOC.html)
> for more references to the CQL language commands.

<!-- 2L ENDIF -->

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

<!-- 2L IF long -->
Surprise! As a matter of fact both columns are of type `TEXT` (that is,
variable-length strings). Indeed, most key-value stores admit string keys
and (unless specific schemas are enforced) the values are also either binary blobs
or ASCII sequences: this workload could then be adapted to
benchmarking other key-value databases.
<!-- 2L ELIF short -->
Oh, looks like both the key and the value columns are of type `TEXT`:
good for adapting this ready-made benchmark to other key/value stores.
<!-- 2L ENDIF -->

<details><summary>Show me what the output looks like</summary>
    <img src="https://github.com/datastaxdevs/workshop-nosqlbench/raw/main/images/desctable_cql.png?raw=true" />
</details>

#### Database health

<!-- 2L IF long -->
By now, the benchmark is probably still running. That's good: you get a chance
to inspect the "database health" while NoSQLBench is writing to it.
Remember you instructed the tool to work at a steady rate in terms of
operations per second.
<!-- 2L ENDIF -->

Locate your database in the Astra main dashboard and click on it;
next, go to the "Health" tab in the main panel. You will see what essentially
is a Grafana dashboard, with a handful of plots being displayed within the
tab - all related to how the database is performing in terms of reads and writes.

<details><summary>Show me the Database Health tab in Astra UI</summary>
    <img src="https://github.com/datastaxdevs/workshop-nosqlbench/raw/main/images/astra_db_health2_annotated.png?raw=true" />
</details>

<!-- 2L IF long -->
> **Tip**: you can customize the width of the time window in the graphs and the
> update frequency. Today it could make sense to set these to 15 minutes and 5 seconds respectively.

Take a look at the plot labeled "Requests Combined": this describes the amount
of write and read requests per second received by the database. You will note
that the _total_ fluctuates around the value provided with the `cyclerate`
parameter during the whole test: but during _rampup_ it will be all writes,
while the _main_ phase will be an equal mixture of reads and writes.

Now turn your attention to the "Write Latency"/"Read Latency" plots. These
provide quantities related to the "latency", as experienced by the
[coordinator node](https://docs.datastax.com/en/cassandra-oss/3.0/cassandra/dml/dmlClientRequestsRead.html),
involved in servicing write/read requests. In particular, some reference
percentiles are reported as they vary in time: indeed, when describing the
performance of the target system, percentiles are a much better tool than
averages or maximum values. Note down the values you read from the plot
in the middle of the _main_ phase.
<!-- 2L ELIF short -->
Check the operations per second from the "Requests Combined" plot;
then have a look at the "Write Latency" and "Read Latency" plots
and take note of some of the percentiles shown there.
<!-- 2L ENDIF -->

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

<!-- 2L IF long -->
What is the meaning of a percentile? Well, if one says "P75 for reading
is 13 milliseconds," that means "75% of the read requests are serviced
_within 13 ms from being received by the server_." This kind of
metric, in most cases, is more meaningful than quoting the maximum value
recorded (for one, the max tends to fluctuate way more).

Quoting high percentiles such as P95, P99 or similar is a standard practice
when expressing the performance of a data system.
<!-- 2L ENDIF -->

#### Final summary

<!-- 2L IF long -->
By now the benchmark should have finished. If it hasn't yet, give it time to complete:
you will see a summary being printed, after which you will get the console
prompt back.

Each run of NoSQLBench generates timestamped files in the `logs`
directory (which is created automatically if not present). The on-screen
summary is a shortened form of the data found in the summary files there.

Now open the most recent `*.summary` file in that directory, corresponding
to the `nb` invocation that just completed.
Find the metric called `cqlkeyvalue_astra_main.result-success`: this
corresponds to events of the type _"a command was issued to the database during_
_the_ main _phase and succeeded (and the time needed for it to complete, as seen from the client_
_side, was recorded)"_.

> The related metric `cqlkeyvalue_astra_main.result` is similar,
> but comprises all events regardless of whether they succeeded or not.
> In "healthy" cases, these two are identical or at most very close to each other.
> This difference is sometimes characterized as the "goodput/throughput" dichotomy.

<!-- 2L ELIF short -->
When the benchmark has finished, open the latest `*.summary` file and look
for `cqlkeyvalue_astra_main.result-success`.
<!-- 2L ENDIF -->

Under that metric title, you will see something similar to:

```
cqlkeyvalue_astra_main.result-success
             count = 15000
         mean rate = 50.00 calls/second
     1-minute rate = 49.94 calls/second
     5-minute rate = 50.29 calls/second
    15-minute rate = 50.57 calls/second
```

<!-- 2L IF long -->
This tells you the total count and the per-minute rate
(as averaged over different time windows) for this operation.

NoSQLBench keeps track of count/timing information for many
operations, which range from substitution of variables in the
workload commands to actual sending of an I/O operation to the database.
<!-- 2L ENDIF -->

#### Additional "histostats" datafile

<!-- 2L IF long -->
You instructed NoSQLBench to output timing information in two other formats:

**First**, with the `--log-histostats` option you get a file with
a listing, for selected metrics, of the min, max and some percentiles as
measured over a desired time window. Try to look at the file `hdrstats.log`
in the Gitpod editor and figure out its structure.

If you want to graphically look at the data thus collected, **we provide a sample
script for plotting**. Simply enter the command (try `-h` for more options)
<!-- 2L ELIF short -->
Use this script to generate a graph of the data collected as "histostats":
<!-- 2L ENDIF -->

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

<!-- 2L IF long -->
> Tip: you can use **Ctrl-mousewheel** to zoom on the image in Gitpod.

Look at the values of, say, the P90 percentile: it will be larger
than both the read and write corresponding percentiles given in the Astra DB
"health" tab. That's because this time you are seeing things **from the vantage
point of the testing client**, and the (Gitpod-to-Astra) communication over
the network is included in the "service time".
<!-- 2L ELIF short -->
The timings will be larger than those from the Astra health tab: indeed,
these are "as seen on the client side" and include more network hops.
<!-- 2L ENDIF -->

<!-- 2L IF long -->
> Besides, the comparison
> is made somewhat murkier by the fact that NoSQLBench measures "cycles", which
> means reads _and_ writes in the _main_ phase; while the Astra health dashboard
> keeps these two separate. A way to make this comparison more apples-to-apples
> would be to "instrument" the metric collection: adding the `instrument=true`
> parameter to the invocation will attach a separate timer to each of the
> named metric in the workload definition, and each of these metrics will
> be featured e.g. in the summary file or anywhere for further inspection.

<!-- 2L ENDIF -->

#### HDR extensive histogram data

<!-- 2L IF long -->
**Second**, the `--log-histograms` option has the effect that NoSQLBench writes
the whole of the measurements it takes in the [HDR file format](http://hdrhistogram.org/).

This is an optimized way to save the full histogram of the measured service time
using exact counts over very thin fixed-width bins. Try to inspect the contents
of file `histogram_hdr_data.log`: you will notice the data is stored in ASCII-encoded long strings.

Fortunately for you, **we provide a sophisticated plotting tool**
for this file, which may serve as inspiration or be used directly for your own benchmarks.

Try running the command (run with `-h` to see more options)
<!-- 2L ELIF short -->
Use this script to generate plots from the detailed "HDR histogram data"
generated during the benchmark:
<!-- 2L ENDIF -->

```bash
./hdr_tool/hdr_tool.py \
    histogram_hdr_data.log \
    -b -c -s \
    -p SampleData \
    -m cqlkeyvalue_astra_main.result-success
```

<!-- 2L IF long -->
and look at the `SampleData*.png` plots that are generated:

- the "base plot" is the full collected histogram of the chosen metric;
- the "stability plot" plots measurements from each time window separately, to help assessing whether the _main_ phase is really a steady state;
- the "percentile plot" reformulates the histogram in terms of percentiles.
<!-- 2L ENDIF -->

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

<!-- 2L IF long -->
> **Tip**: this script is just a demonstration of the versatility of the HDR format:
> you can invent your own post-analysis tool and attach it to the data collected by
> NoSQLBench. Look at the (Python) source code of the tool for inspiration!
> (Or simply take the tool and use it on your data.)

<!-- 2L ENDIF -->

### Metrics, metrics, metrics

<!-- 2L IF long -->
On top of everything you have seen, it is possible to
have NoSQLBench start a Grafana dashboard locally alongside the benchmark
itself, powered behind the scenes by Prometheus-based real-time metric collection.

All it takes is the additional `--docker-metrics` option to the command line,
and Docker must be available on your system (Note: Gitpod comes with Docker preinstalled).

You can try launching another benchmark as follows (note the last option
and the fact that this time we dropped the `driver` parameter):
<!-- 2L ELIF short -->
Launch a new benchmark, this time having NoSQLBench start a dockerized
Grafana/Prometheus stack for metrics (it will take a few more seconds to start):
<!-- 2L ENDIF -->

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

<!-- 2L IF long -->
This command might take a few additional seconds to start the first time,
as Docker images are being downloaded and the containers are started.
Then, successful start of the Grafana dashboard
should be logged, at which point the usual `cql-keyvalue` workload will start.
<!-- 2L ENDIF -->

<details><summary>Show me the run with Docker metrics</summary>
    <img src="https://github.com/datastaxdevs/workshop-nosqlbench/raw/main/images/grafana_startingdockermetrics.png?raw=true" />
</details>

<!-- 2L IF long -->
> It is possible that Gitpod will detect new services running on some local ports
> and automatically open the Grafana dashboard in its mini-browser. Better to
> ignore it and re-open the URL in a new, actual browser tab as instructed below.

<!-- 2L ENDIF -->

#### Grafana dashboard

<!-- 2L IF long -->
The Grafana container is running and exposed on local port 3000. Luckily,
Gitpod is kind enough to map local ports to externally-accessible addresses,
such as `https://3000-datastaxdevs-workshopnos-nq5y2jf5uw9.ws-eu38.gitpod.io`.
Your URL will be different: to construct it, simply prepend a `3000-`
to the URL of the Gitpod IDE. Then, open this address in a new tab.
<!-- 2L ELIF short -->
Reach the Grafana container in a new tab, with an URL that has `3000-`
in front of your Gitpod URL (e.g.
`https://3000-datastaxdevs-workshopnos-[...].gitpod.io`).
<!-- 2L ENDIF -->

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
<!-- 2L IF long -->
Let's see some of them and their significance.
<!-- 2L ENDIF -->

<details><summary>Show me the dashboard contents</summary>
    <img src="https://github.com/datastaxdevs/workshop-nosqlbench/raw/main/images/grafana_plots.png?raw=true" />
</details>

<!-- 2L IF long -->
- **"Ops and Successful Ops"**. One-minute averages of the total operations dispatched per second by NoSQLBench. This will match the reported per-second averages found in the `*.summary` file. There are separate curves for each phase, so you will clearly see _rampup_ leaving the room to _main_ at some point during the test.
- **"p75/p99 client overhead"**. This is related to timing of operations internal to NoSQLBench (note the scale, barely a few _micro_-seconds). You should keep an eye on those to check that the benchmarking client is not experiencing bottlenecks of sorts.
- **"service time distribution/range"**. Here you can see percentiles for "service time" relative to the various phases, a measurement corresponding to the "success" metric introduced earlier. These quantities then directly relate to the HDR histogram data analyzed above and should match them. Note that the "min" and "max" are denoted "p0" and "p100" here (indeed this is what they are, by definition).
<!-- 2L ENDIF -->

#### A glance at Prometheus

<!-- 2L IF long -->
If you want to look at the "raw" source of data feeding the Grafana plots,
head to the Prometheus UI, exposed at local port 9090. If you are on Gitpod,
similarly to what you did for Grafana earlier,
you get there by prepend a `9090-`
to the domain name you are using your IDE at. Then, open this address
in a new tab.
<!-- 2L ELIF short -->
To reach the Prometheus container, which handles the "raw" data behind Grafana,
open a modified URL (this time with `9090-`) in a new tab.
<!-- 2L ENDIF -->

<details><summary>Show me the Prometheus UI</summary>
    <img src="https://github.com/datastaxdevs/workshop-nosqlbench/raw/main/images/prometheus2.gif?raw=true" />
</details>

Click on the "world" icon next to the "Execute" button in the search bar:
in the dialog that appears you can look for specific metrics.
Try to look for `result_success` and confirm, then click "Execute".

<!-- 2L IF long -->
The search results are many datapoints, pertaining to several metrics related
to the service time. Still, those are for different phases and, most important,
different measurements (percentiles, averages, counts), which does not really
make sense to inspect together.
<!-- 2L ENDIF -->

> **Tip:** switch to the "Graph" view for a more immediate visualization.
> The graphs display "raw" data, hence are in units of nanoseconds.

<!-- 2L IF long -->
Fortunately, each datapoint is fully equipped with detailed metadata,
which allow for sophisticated filtering. Further, you can use the flexible,
powerful [query language used by Prometheus](https://prometheus.io/docs/prometheus/latest/querying/basics/)
to even perform aggregations on top of the data queries.
<!-- 2L ELIF short -->
To make sense of the (heterogeneous) results, some filtering is in order --
but we are not entering too much into the details of Prometheus here.
<!-- 2L ENDIF -->

Just to pique your interest, try pasting these examples and click "Execute":

```
# filtering by metadata
{__name__="result_success", type="pctile", alias=~".*main.*"}

# aggregation
avg_over_time({__name__="result_success", type="pctile", alias=~".*main.*"}[10m])

# another aggregation, + filtering
max_over_time({__name__="result_success", type="pctile", alias=~".*main.*"}[10m])
```

<!-- 2L IF long -->
Also, note that Prometheus exposes a REST access, so you can imagine, for
instance, a running scripts that tracks the metrics and responds to them
in real time.
<!-- 2L ENDIF -->

## Workloads

<!-- 2L IF long -->
We mentioned that `cql-keyvalue` is one of several ready-to-use _workloads_,
but also that you can easily build your own: for example, to test a specific
data model or ensure you closely mimic your application's request pattern.

So, now it's time for a closer inspection of workloads. Each workload is built as
a `yaml` file, defining its scenarios and the sequences of phases each scenario
is made of.

Phases, in turn, consist of several statements that the driver will know how to
"execute" (i.e. send to the target system as operations to execute).

There is [quite some freedom](https://docs.nosqlbench.io/docs/workloads_101/00-designing-workloads/)
in creating workloads: in the following you will just explore some of
this space. Look into the reference documentation for more.
<!-- 2L ELIF short -->
This part is about how workloads are defined.
<!-- 2L ENDIF -->

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

<!-- 2L IF long -->
This is not a line-by-line analysis, but broadly speaking
there are three important sections:

- **scenarios**. This defines which _phases_ constitute each scenario. More specifically, each phase is expressed as an inline script, which in turn follows the [NoSQLBench CLI scripting syntax](https://docs.nosqlbench.io/docs/reference/cli-scripting/).
- **bindings**. Each _binding_ defines a particular recipe to generate a sequence of pseudo-random values. Emphasis is on the "pseudo", since bindings are (usually) a _fully deterministic_, reproducible, mappings of cycle numbers to values. The sequence of "keys" produced as the the _rampup_ phase of key-value workload unfolds, for instance, is defined here by the `seq_key` binding. Bindings are defined using a functional compositional approach, starting from a set of available building blocks, and can generate values of many different data types.
- **blocks**. Here, groups of "statements" (better: _operations_) are defined for use within scenarios. Within the body of operations, [bindings](https://docs.nosqlbench.io/docs/workloads_101/03-data-bindings/) can be employed (`{binding_name}`), which implies they will take values along the generated sequence as the cycle number unfolds; similarly, [template parameters](https://docs.nosqlbench.io/docs/workloads_101/09-template-params/) can be used (`<<parameter_name:default>>`, or `TEMPLATE(parameter_name,default)`) to be replaced according to settings passed through the command-line or when defining the scenario composition in the "scenarios" section.

Try to track what happens when you invoke the `cql-keyspace astra` workload/scenario:
1. the _schema_ phase is invoked: it consists of running, with the `cql` driver, the blocks whose tags [match the selector](https://docs.nosqlbench.io/docs/workloads_101/05-op-tags/#tag-filtering-rules) `tags==phase:schema-astra`. Also some parameters are passed to the execution. (_Note that the schema phase differs between an Astra DB target and a regular Cassandra target, while later phases do not_.)
2. When _schema_ is over, the _rampup_ is started. This runs all blocks matching `tags==phase:rampup`, and passes the parameters `threads` and `cycles`. The latter will preferrably read the value passed through command-line (look for `rampup-cycles=...` in the benchmark command you ran earlier), with a default.
3. Running _rampup_ then entails running the block with `name: rampup` (as can be seen by the tags attached to it). In the block, a [consistency level](https://docs.datastax.com/en/dse/5.1/cql/cql/cql_reference/cqlsh_commands/cqlshConsistency.html) is defined, again using template parameters. The statement (or operation) that is repeatedly executed is an `INSERT` statement, which writes rows to a DB table:
4. The `INSERT` targets a table in a keyspace whose name (as well as the table name itself) can be provided through a command-line parameter (compare with the `keyspace=...` part of the benchmark command you ran earlier). The default keyspace is `baselines`.
5. In this `INSERT` statement, also the bindings `seq_key` and `seq_value` occur: that is, you can imagine a loop with an index `i` looping over `rampup-cycles` integer values: each time the `INSERT` statement is executed, "key" and "value" will be equal to the corresponding mapping functions "evaluated at `i`".
6. When these `rampup-cycles` `INSERT` statements are all executed, the _rampup_ phase will be done and the execution will turn to the _main_ phase. The tag filtering this time matches _two_ operations. They will be combined in an alternating fashion, according to their `ratio` (see [here](https://docs.nosqlbench.io/docs/reference/core-op-params/#ratio) for details), with the final result, in this case, of reproducing a mixed read-write workload.
7. The scenario will then have completed.
<!-- 2L ELIF short -->
Have a look at the file and try to identify its structure and the various
phases the benchmark is organized into.
<!-- 2L ENDIF -->

### Play with workloads

A good way to understand workload construction is to start from simple ones.

To run the following examples please go to the appropriate subdirectory:
```
cd workloads
```

#### Example 1: talking about food

<!-- 2L IF long -->
Take a look at `simple-workload.yaml`. This defines two
[operations](https://docs.nosqlbench.io/docs/workloads_101/01-op-templates/)
(formerly called "statements") that are to be interleaved according
to their 
[ratio](https://docs.nosqlbench.io/docs/reference/core-op-params/#ratio)
parameter. As you saw earlier, there are parts of the
operation body that depend on the cycle number
as specified by the binding functions defined under `bindings`.

Run the workload with:
<!-- 2L ELIF short -->
Run the first example (and then look at the corresponding
`simple-workload.yaml`) with:
<!-- 2L ENDIF -->

```
nb run driver=stdout workload=simple-workload cycles=12
```

<!-- 2L IF long -->
The driver here is `stdout`, so each operation will simply print its body
to screen. As you can see, these are not valid CQL statements, indeed one would
get errors if invoking with `drivers=cql`. This is an important point: the
operation body itself can take any form, since _its actual syntactical validation
will happen at driver level_. NoSQLBench offers several drivers, and it is
important to match statement bodies with the proper drivers (`stdout` in
particular can take basically anything as input).

Bindings are defined in a functional way, by providing a sequence of
functions that will be composed, left-to-right. It is implied that the input to
the first such function is the cycle number, so for instance the binding:
```
 multiplier: AddHashRange(100); Clamp(5,20); NumberNameToString()
```

means: the `multiplier` binding will be a function that takes the cycle number as input,
[adds a pseudorandom 0-100 value](https://docs.nosqlbench.io/docs/bindings/funcref-general/#addhashrange)
to it, [adjusts the result](https://docs.nosqlbench.io/docs/bindings/funcref-general/#clamp)
so that it lies within the [5, 20] interval, and finally
produces the [spelled-out name](https://docs.nosqlbench.io/docs/bindings/funcref-premade/#numbernametostring)
of the resulting number.

For a general introduction to bindings and a list of the (many) available
functions, please see [here](https://docs.nosqlbench.io/docs/bindings/binding-concepts/).
<!-- 2L ELIF short -->
Look at how _bindings_ connect the sequence of operations to "execute"
(in this case, simply print on screen) with the data to be used in
them.
<!-- 2L ENDIF -->

#### Example 2: animal meeting

<!-- 2L IF long -->
The previous example, albeit silly, was meant to show the basics of building
workloads.
An important feature is the possibility to package several workflows into a
single sequence that can then be run at once (["named scenarios"](https://docs.nosqlbench.io/docs/workloads_101/11-named-scenarios/)).

The need to perform a _schema_ initialization and to execute a _rampup_ phase
before doing the actual _main_ benchmarking is, as discussed earlier,
almost universal: named scenarios have been designed with that need in mind.

Try to run the following example scenario:
<!-- 2L ELIF short -->
Run the second example, which is an example of structuring a workload
in _phases_ (and then open `workload-with-phases.yaml`):
<!-- 2L ENDIF -->

```
nb workload-with-phases default driver=stdout
```

<!-- 2L IF long -->
You see that here several clearly distinct phases take place.
If you inspect the structure of `workload-with-phases.yaml`, 
you can see that the file begins by defining the `default` scenario
as a sequence of `run` invocations, each involving certain statement blocks
selected through tags.

This `yaml` file also shows usage of template parameters:
with (interchangeable) expressions such as `TEMPLATE(rampup-cycles,5)`
and `<<act_ratio:1>>`
NoSQLBench can use a command-line-provided parameter (with a default value)
inside the workload specs. Try to re-run the workload adding
`rampup-cycles=10 act_ratio=11` to see the difference.

> Note: keep in mind that `act_ratio` is constrained in its
> values so that the sum of the `ratio`
> parameters for the operations in `main`
> divides exactly the number of cycles
> in that phase. This sum constitutes the (["stride"](https://docs.nosqlbench.io/docs/reference/standard-metrics/#strides)).

<!-- 2L ELIF short -->
Notable features of this workload are its multi-phase structure
(a nearly universal feature of actual benchmarks), the use
of the `ratio` parameter, and the usage of template parameters in the
definition.
<!-- 2L ENDIF -->



## Homework assignment

The "Lab" part of the homework, which requires you to finalize
a workload `yaml` and make it work according to specifications,
is detailed on [this page](homework/homework.md).
