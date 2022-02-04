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
4. XXX



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
it** to make sure you "Open in new tab":

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
ls /workspace/nbws1/*zip -lh
```

so that you get the _full path to your bundle file_ (and also verify that it is
the correct size).

<details><summary>Show me</summary>
    <img src="https://github.com/hemidactylus/nbws1/raw/main/images/gitpod_uploading_bundle_2_annotated.png?raw=true" />
</details>


### Configure the Astra DB token

with an `.env` file you then `source`.

```
MY_CLIENT_ID=...
MY_CLIENT_SECRET=...
```

## XXX

### A short dry run

Launch a 2-statement `driver=console` (TO ADD)

### Benchmark your Astra DB

Launch this command (explained in the slides, line by line)

You can keep it open in the editor as well for ease of usage

```
./nb cql-keyvalue \
    astra \
    username=${MY_CLIENT_ID} \
    password=${MY_CLIENT_SECRET} \
    secureconnectbundle=./secure-connect-workshops.zip \
    driver=cql \
    main-cycles=200000 \
    rampup-cycles=200000 \
    keyspace=nbkeyspace \
    --progress console:5s \
    --log-histograms 'histogram_hdr_data.log:.*.cycles.servicetime:20s' \
    --log-histostats 'hdrstats.log:cqlkeyvalue_default_main.cycles.servicetime:20s'
```

? ADD `cyclerate` here for keeping in control (also can have a theoretical value imo)

? add a note on "what {you see / you have to do} if the DB is hibernated"

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

