# Benchmark your Astra DB with NoSQLBench

The goal of this workshop is to get you familiar with the powerful and versatile
tool `NoSQLBench`. With that, you can perform industry-grade, robust benchmarks
aimed at several (distributed) target systems, especially NoSQL databases.

Today we are going to benchmark Astra DB, a database-as-a-service built on top of
Apache Cassandra. Along the way, you will learn the basics of NoSQLBench.

In this repository you will find all material and references you need:

- [slide deck](#)
- [exercises](#)
- [workshop video](#)
- [step-by-step guide](#before-you-start)
- [additional references](#)
- [our Discord server](https://dtsx.io/discord) for keeping in touch with DataStax Developers
- [our Q&A forum](https://community.datastax.com/) (think StackOverflow for Cassandra and all things DataStax)

#### Table of Contents

1. Before you start
2. Create your Astra DB instance
3. Launch Gitpod and setup NoSQLBench
4. Run benchmarks



## Before you start

If you are not watching us live, please look at the provided presentation material
for more coverage of the theory part. There, you will learn more about:

- Apache Cassandra, a distributed masterless NoSQL Database;
- Astra DB, a database-as-a-service in the cloud, built on Cassandra, ready to use in minutes with a few clicks;
- what "testing a data store" entails;
- the main features and general principles behind the NoSQLBench benchmarking tool.


### FAQ

- What are the prerequisites (for me / my compuer) ?

> This workshop is aimed at data architects, solution architects or anybody who
> wants to get serious about measuring the performance of their data-intensive system.
> You should know what a database is, and have a general understanding of the
> challenges of communicating over a network.

- Do I need to install a database or anything on my machine?

> No, no need to install anything. We will do everything in the browser.
> (although the knowledge you gain today will probably be best put to use
> once you install NoSQLBench on some client machine to run tests).

- Is there anything to pay?

> **No.** All materials and software we'll use today is _free_.


### Homework

To complete the workshop and get a verified "NoSQLBench" badge, you will
have to do a little homework and submit it.

_Homework details TBD. There'll be a workload yaml with ready-made "menu of bindings"
and you will be asked to use them appropriately._



## Create your Astra DB instance

First let's create a database: an instance of Astra DB, which
we will then benchmark with NoSQLBench.

> Don't worry, we will create
> it within the "Free Tier", which offers quite a generous free
> allowance in terms of monthly I/O (40M operations per month)
> and storage (80 GB).

You will need to:

- create an Astra DB instance [as explained here](https://github.com/datastaxdevs/awesome-astra/wiki/Create-an-AstraDB-Instance), with database name = `workshops` and keyspace = `nbkeyspace`;
- generate and download a Secure Connect Bundle [as explained here](https://github.com/datastaxdevs/awesome-astra/wiki/Download-the-secure-connect-bundle);
- generate and retrieve a DB Token [as explained here](https://github.com/datastaxdevs/awesome-astra/wiki/Create-an-Astra-Token#c---procedure). **Important**: use the role "DB Administrator" for the token.

Moreover, keep the Astra DB dashboard open: it will be useful later. In particular the
Health tab and the CQL Console.



## Launch Gitpod and setup NoSQLBench

Gitpod is an IDE in the cloud (modeled after VSCode). It comes with a full
"virtual machine" (actually a Kubernetes-managed container), which we will
use as if it were our own computer (e.g. downloading files, executing programs
and scripts, even launching containers from within it).

The button below will: spawn your own Gitpod container + clone this repository
in it + preinstall the required dependencies: **ctrl-click on
it** to make sure you "Open in new tab" (Note: you may have to authenticate
through Github in the process):

[![Open in Gitpod](https://gitpod.io/button/open-in-gitpod.svg)](https://gitpod.io/#https://github.com/hemidactylus/nbws1)

In a few minutes, a full IDE will be ready in your browser, with a file
explorer on the left, a file editor on the top, and a console (`bash`) below it.

> There are many more other features, probably familiar to those who have
> experience with VSCode. Feel free to play around a bit!


### Install NoSQLBench

Let's download the latest stable version of NoSQLBench to this machine.
First make sure you are in the top-level repository directory with your
Gitpod console: type `pwd` and see if the output is `/workspace/nbws1`.

We will download the "Linux binary" distribution of NoSQLBench:
as instructed [here](https://github.com/nosqlbench/nosqlbench/blob/main/DOWNLOADS.md),
we get the file (it's a few hundred megabytes) with
```
curl -L -O https://github.com/nosqlbench/nosqlbench/releases/latest/download/nb
```

and when the download is finished we make it executable and move it,
out of convenience, to a directory which is part of the search path:
```
chmod +x nb
sudo mv nb /usr/local/bin/
```

Ok, let's check that the program starts: invoking
```
nb --version
```
should output the program version (something like `4.15.86` -- or higher).

> You will probably see a message like `Picked up JAVA_TOOL_OPTIONS ...` when
> you start `nb`. You can ignore it: it is a consequence of some settings by
> Gitpod and does not have to do with NoSQLBench itself.

> Note that if your Gitpod instance gets hibernated (which happens after some
> inactive time) and you restart it later, recall that only the contents
> of `/workspace` will be restored: hence, you would have to repeat the
> installation.

### Upload the Secure Connect Bundle to Gitpod

NoSQLBench will need to connect to your Astra DB database: to do so, the
Secure Connect Bundle zip file you downloaded earlier must be uploaded
to your Gitpod environment.

Locate the bundle file on your computer with the file explorer
(it will probably be called something like `secure-connect-workshops.zip`
and be around 12 KB in size) and simply **drag-and-drop** it to
the file navigator panel ("Explorer") on the left of the Gitpod view.

<details><summary>Show me</summary>
    <img src="https://github.com/hemidactylus/nbws1/raw/main/images/gitpod_uploading_bundle_1_annotated.png?raw=true" />
</details>

Once you drop it you will see it listed in the file explorer itself.
As a check, you can issue the command
```
ls ./secure*zip -lh
```

so that you get the _relative path to your bundle file_ (and also verify that it is
the correct size). Note that, as per best practices with NoSQLBench, (relative)
paths to files should start with `./`.

<details><summary>Show me</summary>
    <img src="https://github.com/hemidactylus/nbws1/raw/main/images/gitpod_uploading_bundle_2_annotated.png?raw=true" />
</details>


### Configure the Astra DB parameters

If we want NoSQLBench to access the Astra DB instance, we have to pass it
the required connection parameters and secret. To do so, we now set up
a `.env` file, which will make our life easier later.

Copy the provided template file to a new one and open it in the Gitpod
file editor:
```
cp .env.sample .env
gp open .env
# (you can also simply locate the file
#  in the Explorer and click on it)
```

Insert the "Client ID" and "Client Secret" of the DB Token you created earlier
and, if necessary, adjust the other variables.

<details><summary>Show me what the .env file could look like</summary>
    <img src="https://github.com/hemidactylus/nbws1/raw/main/images/dotenv.png?raw=true" />
</details>

Now, source this file to make the definitions therein available to this shell:
```
. .env
```

To check that the file has been sourced, you can try with:
```
echo ${ASTRA_DB_KEYSPACE_NAME}
```

and make sure the output is not an empty line.


(Note that you will have to source the file in any new shell you plan to use).



## Run benchmarks

Everything is set to start running the tool.


### A short dry run

From a user's perspective, NoSQLBench sends operations (e.g. reads, writes)
to the target system (e.g. a database) and record how the latter responds
(failures and, most important, response time).

Try launching this very short "dry-run benchmark", that instead of actually
reaching the database simply prints a series of CQL statements to the console
(as specified by the `driver` parameter):

```
nb cql-keyvalue astra                   \
    driver=stdout                       \
    main-cycles=10                      \
    rampup-cycles=10                    \
    keyspace=${ASTRA_DB_KEYSPACE_NAME}
```

You will see 21 (fully-formed, valid CQL) statements being printed:
one `CREATE TABLE`, then ten `INSERT`s
and then another ten between `SELECT`s and further `INSERT`s.

This corresponds
to the three phases defined in the `cql-keyvalue` _workload_: **schema**,
**rampup** and **main**. The most relevant benchmark results are from the
**main** phase, which mimics the kind of load the database would be subject to
when operating normally.

> For most workloads, a three-phase structure is the most reasonable choice: first
> the schema is set up, then an amount of data is poured in, and finally
> the target system is subject to a mixture of reads and writes. The third
> and last phase (_main_) usually generates contention on the server, which is
> the very situation we usually want to put to test.

Now re-launch the above dry run (you may find it convenient to copy the few
last lines of the output to a temporary file in the Gitpod editor for an easier
comparison):

```
nb cql-keyvalue astra                   \
    driver=stdout                       \
    main-cycles=10                      \
    rampup-cycles=10                    \
    keyspace=${ASTRA_DB_KEYSPACE_NAME}
```

do you notice that the output is identical down to the actual values used
in the `INSERT`s and `DELETE`s?
Indeed an important goal for any benchmark is its _reproducibility_:
here, among other
consequences, this means that the operations (their sequence and contents alike)
should be completely determined with no trace of actual randomness.

You can also peek in the `logs` directory now: it is created automatically and
populated with some information from the benchmark at each execution of `nb`.


### Benchmark your Astra DB

It is now time to start hitting the database!
What you launched earlier is the `cql-keyvalue` _workload_, one of the several
ready-to-use workloads included with NoSQLBench (but you can build your own
by all means).
In particular, you ran the `astra` _scenario_, which determines a particular
way the workload is to be unfolded and executed.

This time we will have `driver=cql` to actually reach the database:
for that to work, we will provide all connections parameters we set up earlier.

We will ask NoSQLBench to perform a substantial amount of operations, so to have
enough statistical support for the results.

> On the other hand, we will rate-limit the operations sent to the database
> (with the `cyclerate` parameter). This is mainly because often the goal
> of a benchmark is to verify whether the system can withstand
> a _known, controlled_ workload;
> but in this case there are also other practical reasons: (1) we don't want
> you to consume
> too much of your Free Tier monthly allowance in this "functional demo"; moreover,
> (2) if you are running on the Free Tier you may otherwise hit the
> guardrails and the performance limitations coming with that class of Astra DB
> instances.

Here is the full command to launch:

```
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
    --progress console:5s                                                 \
    --log-histograms 'histogram_hdr_data.log:.*.cycles.servicetime:20s'   \
    --log-histostats 'hdrstats.log:cqlkeyvalue_astra_main.cycles.servicetime:20s'
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
| `cyclerate`               | rate-limiting (100 per second)
| `driver=cql`              | driver to use (CQL, for AstraDB/Cassandra)
| `rampup-cycles`           | how many operations in the "rampup" phase
| `main-cycles`             | same for the "main" phase
| `--progress console`      | frequency of console prints
| `--log-histograms`        | write data to HDR file (see later)
| `--log-histostats`       | write some more stats to this file

This way of invoking `nb`, the ["named scenario"](https://docs.nosqlbench.io/docs/workloads_101/11-named-scenarios/)
way, is not the only one: it is also possible to have a finer-grained control over what activities should
run with a full-fledged [CLI scripting](https://docs.nosqlbench.io/docs/reference/cli-scripting/) syntax.

</details>

> _Note_: if you were targeting a "regular" Cassandra instance (as opposed to Astra DB),
> the command line above would change a little: the scenario would be `default`,
> you would need to provide a parameter such as `hosts=192.168.1.1,192.168.1.2`,
> and there would be _no_ `secureconnectbundle` parameter. As for username and password,
> ... well, that depends on how you configured the Cassandra installation.
> The crucial thing is that NoSQLBench uses the very same CQL drivers to
> access the database, regardless of whether Astra DB or any Cassandra cluster.

The above command should last approximately ten minutes, during which NoSQLBench
sends a constant stream of I/O operations to the database and collects timing
information on how it responds. You will see a **console output** keeping you
updated on the progress of the
currently-running phase (`schema`/`rampup`/`main`).

While this runs, let's have a look around.

#### Database contents

By this point, you may have a quesiton:
_"but what is being written to the database, exactly?_

To find out, we will connect to the database and inspect the contents of the
keyspace. There are several ways one could connect to Astra DB:
using Cassandra drivers with most programming languages,
through the HTTP requests enabled by the Stargate Data API, or directly
with a client that "speaks" the CQL language.
Today we will make use of the **CQL Console** available in the browser
within the Astra UI.

Choose your database in the Astra main dashboard and click on it;
next, go to the "CQL Console" tab in the main panel. In a few seconds the
console will open in your browser, already connected to your database and
waiting for your input.

<details><summary>Show me how to get to the CQL Console in Astra</summary>
    <img src="https://github.com/hemidactylus/nbws1/raw/main/images/astra_get_to_cql_console.gif?raw=true" />
</details>

> Commands entered in the CQL Console are terminated with a semicolon (`;`)
> and can span multiple lines. Run them with the `Enter` key. If you want to
> interrupt the command you are entering, hit `Ctrl-C` to be brought back
> to the prompt. See [here](#) for more references to the CQL language commands.

Start by telling the console that you will be using the `nbkeyspace` keyspace:
```
USE nbkeyspace;
```

Check what tables have been created in this keyspace:
```
DESC TABLES;
```

You should see table `keyvalue` listed as the sole output.
Look at a a few lines from this table:
```
SELECT * FROM keyvalue LIMIT 20;
```

<details><summary>Show me how the output looks like</summary>
    <img src="https://github.com/hemidactylus/nbws1/raw/main/images/select_cql.png?raw=true" />
</details>

Ok, mystery solved. It looks like the table contains simple key-value pairs,
with two columns seemingly of numeric type. Let's check:
```
DESC TABLE keyvalue;
```

Surprise! As a matter of fact both columns are of type `TEXT` (that is,
variable-length strings). Indeed, most key-value stores admit string keys
and (unless specific schemas are enforced) the values are also either binary
or ASCII byte sequences: this workload can then be easily adapted for
benchmarking other key-value databases.

<details><summary>Show me what the output looks like</summary>
    <img src="https://github.com/hemidactylus/nbws1/raw/main/images/desctable_cql.png?raw=true" />
</details>

#### Database health

By now, the benchmark is probably still running. That's good: we get a chance
to inspect the "database health" while NoSQLBench is writing to it.
Remember we instructed the tool to work at a steady rate in terms of
operations per second.

Locate your database in the Astra main dashboard and click on it;
next, go to the "Health" tab in the main panel. You will see what essentially
is a Grafana dashboard, with a handful of plots being displayed within the
tab - all related to how the database is performing in terms of reads and writes.

<details><summary>Show me the Database Health tab in Astra UI</summary>
    <img src="https://github.com/hemidactylus/nbws1/raw/main/images/astra_db_health_annotated.png?raw=true" />
</details>

> **Tip**: you can customize the width of the time window in the graphs and the
> update frequency. Today it could make sense to set these to 15 minutes and 5 seconds respectively.

Take a look at the plot labeled "Requests Combined": this describes the amount
of write and read requests per second received by the database. You will note
that the _total_ fluctuates around the value provided with the `cyclerate`
parameter during the whole test: but during _rampup_ it will be all writes,
while the _main_ phase will be an equal mixture of reads and writes.

Now turn your attention to the "Write Latency" plot. This provides quantities
related to the "latency", as experienced by the coordinator node, involved
in servicing write requests. In particular, some reference
percentiles are reported as they vary in time: indeed, when describing the
performance of the target system, percentiles are a much better tool than
averages or maximum values. Note down the values you read from the plot
in the middle of the _main_ phase.

<details><summary>Show me "sample values" one could read from the graph</summary>

Below is a real-life example of the values that could result from a `cql-keyvalue`
benchmark session:

| Percentile  | Write Latency | Read Latency |
|-------------|---------------|--------------|
| P50         | 735   _µs_    |   1.05 _ms_  |
| P75         | 908   _µs_    |  13    _ms_  |
| P90         |  33.1 _ms_    |  58    _ms_  |
| P95         |  78.2 _ms_    | 113    _ms_  |
| P99         | 220   _ms_    | 254    _ms_  |

</details>

What is the meaning of a percentile? Well, if we say "P75 for reading
is 13 milliseconds," that means "75% of the read requests are serviced
_within 13 ms from being received by the server_." This kind of
metric, in most cases, is more meaningful than quoting the maximum value
recorded (for one, the max tends to fluctuate way more).

#### Final summary

By now the benchmark should have finished. If it hasn't yet, give it time to complete:
you will see a summary being printed, after which you will get the console
prompt back.

Each run of NoSQLBench generates timestamped files in the `logs`
directory (which is created automatically if not present). The on-screen
summary is a shortened form of the data found in the summary files there.

Now open the most recent `*.summary` file in that directory, corresponding
to the `nb` invocation that just completed.
Find the metric called `cqlkeyvalue_astra_main.cycles.servicetime`: this
corresponds to events of the type "a command was issued to the database during
the _main_ phase (and the time needed for it to complete, as seen from the client
side, was recorded)".

Under that metric title, you will see something similar to:

```
         count = 5000
     mean rate = 49.93 calls/second
 1-minute rate = 50.14 calls/second
 5-minute rate = 50.85 calls/second
15-minute rate = 51.07 calls/second
```

This tells you the total count and the per-minute rate
(as averaged over different time windows) for this operation.

NoSQLBench keeps track of count/timing information for many
operations, which range from substitution of variables in the
workload commands to actual sending of an I/O operation to the database.



** Quick inspection of the HDR histostats** (created by that option in calling nb)
And look at the numbers for the `cqlkeyvalue_astra_main.cycles.servicetime`.

** Quick inspection of the HDR proper** (see later for more)


### Your own analysis of the HDR

The HDR can be analyzed with any post-analysis tool you can imagine, as long as capable of reading [that format](#).

Here we provide a sample such tool written in Python (have a look at the code, experiment with it, etc).

Try to launch:

    ./hdr_tool/hdr_tool.py histogram_hdr_data.log -b -c -s -p SampleData -m cqlkeyvalue_astra_main.cycles.servicetime

(explanation, or try `-h`)

Three images are generated:

- chunks (may be good for other studies)

- percentiles (check P90. For me it gave 77 ms for 'main', compare with read/write above 58/33 ms. Caution in comparing, hdr mixes everything for main (read/writes)). Difference = network net time (one was on server, other is here in github).

- actual histo (replot with shorter max value in plot?)

TODO add option to control max value of plot.

So imagine you are to write a SLO for your product ...

### Metrics, metrics, metrics

A new run of `nb` with `--docker-metrics`.
While it runs:

- check the reported Grafana graphs and connect them to metrics seen earlier / concepts with percentiles etc
- go to Prometheus and paste these just to have an idea. If you're interested, we just give some links.

## Workloads

### dump and inspect the workload

    nb --copy cql-keyvalue

The general structure of a workload

### play with a sample workload

We have included a sample, easy workload for you to play with:

...

### a semi-finished workload (homework)

And we also provide another workload: ... (homework)

Bindings in the yaml itself, but also link at the "example bindings" on the nb docs.