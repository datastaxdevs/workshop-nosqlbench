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

Now copy the few last lines of the output to a temporary file in the Gitpod
editor and re-launch the above dry run:

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
should be completely determined with no trace of randomness.

You can also peek in the `logs` directory now: it is created automatically and
populated with some information from the benchmark at each execution of `nb`.


### Benchmark your Astra DB

It is now time to start hitting the database!
What you launched earlier is the `cql-keyvalue` _workload_, one of several
ready-to-use included with NoSQLBench (but you can build your own).
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
    cyclerate=100                                                         \
    driver=cql                                                            \
    rampup-cycles=40000                                                   \
    main-cycles=40000                                                     \
    --progress console:5s                                                 \
    --log-histograms 'histogram_hdr_data.log:.*.cycles.servicetime:20s'   \
    --log-histostats 'hdrstats.log:cqlkeyvalue_default_main.cycles.servicetime:20s'
```

<details><summary>Show me the command breakdown</summary>

Note that some of the parameters (e.g. `keyspace` are workload-specific)

| command | meaning |
|---------|---------|
| `cql-keyvalue`                                        | workload
| `astra`                                               | scenario
| `username=...`                                        | authentication
| `password=...`                                        | authentication
| `secureconnectbundle=...`                             | Astra DB connection parameters
| `keyspace=`                                           | target keyspace
| `cyclerate=100`                                       | rate-limiting (100 per second)
| `driver=cql`                                          | driver to use (CQL to speak with Astra DB/Cassandra)
| `rampup-cycles=40000`                                 | 
| `main-cycles=40000`                                   | how many operations in the "main" phase
| `--progress console:5s`                               | same for the "rampup" phase
| `--log-histograms 'histogram_hdr_data.log:[...]:20s'` | write data to HDR file (see later)
| `--log-histostats 'hdrstats.log:[...]:20s'`           | write some more stats to this file


</details>

While it runs:

- go to the CQL console, see what is created
- check the Health tab on Astra UI

When it finishes:

- inspect summary file
- inspect HDR file (and histostats). Look at the numbers (num/seconds) for a standard metric.

### Your own analysis of the HDR

Launch `hdr_tool.py` and look at the results. Note down percentiles and max value.

A good point for more stuff on percentiles and "SLO". (theory)

### Metrics, metrics, metrics

A new run of `nb` with `--docker-metrics`.
While it runs:

- check the reported Grafana graphs and connect them to metrics seen earlier / concepts with percentiles etc
- go to Prometheus and paste these just to have an idea. If you're interested, we just give some links.

