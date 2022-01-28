# Benchmark your Astra DB with NoSQLBench

The goal of this workshop is to get you familiar with the powerful and versatile
tool `NoSQLBench`. With that, you can perform industry-grade, robust benchmarks
aimed at several data stores, especially NoSQL distributed databases.

Today we are going to benchmark Astra DB, a database-as-a-service built on top of
Apache Cassandra. Along the way, you will learn the basics of NoSQLBench.

In this repository you will find all material you need:

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
- the main concepts behind testing a data store;
- the main features and general principles behind the NoSQLBench benchmarking tool.

### FAQ

- What are the prerequisites (for me / my compuer) ?

> This workshop is aimed at data architects, solution architects or anybody who
> wants to get serious about measuring the performance of their architecture.
> You should know what a database is, and have a general understanding of the
> challenges coming with communicating over a network.

- Do I need to install a database or anything on my machine?

> No need to install anything. We will do everything in the browser.
> (although the knowledge gained
> today will probably be most useful once you install NoSQLBench on some client
> machine to run further tests).

- Is there something to pay?

> **No.** All materials and software to use is _free_.

### Homework

To complete the workshop and get a verified badge, you will have to do a little
homework and submit it.

_Homework details TBD._

## Create your Astra DB instance

First let's create a database: an instance of Astra DB, which
we will then benchmark with NoSQLBench.

> Don't worry, we will create
> it within the "Free Tier", which offers quite a generous free
> allowance in terms of monthly I/O (40M operations per month)
> and storage (80 GB)._

_TODO:_

- create Astra DB with database = `workshops` and keyspace = `nbkeyspace`;
- generate and download SCB.zip;
- generate a "DB Administrator" token and store client ID and client secret for later.

Keep the Astra DB dashboard open: it will be useful later. In particular the
Health tab and the CQL Console.

## Launch Gitpod and setup NoSQLBench

Gitpod is an IDE in the cloud (modeled after VSCode). It comes with a full
"virtual machine" (actually a Kubernetes-managed container), which we will
use as if it were our own computer (downloading files, executing programs
and scripts, etc).

The button below will spawn your own Gitpod container, clone this repository
in it and preinstall a bunch of required dependencies for later: Ctrl-click on
it or anyway make sure you "Open in new tab" to keep this README open:

[![Open in Gitpod](https://gitpod.io/button/open-in-gitpod.svg)](https://gitpod.io/#https://github.com/hemidactylus/nbws1)

In a few minutes, a full IDE will be ready in your browser, with a file
explorer on the left, a file editor on the top, and a console (`bash`) below it.

> There are many more other features, probably familiar to those who have
> experience with VSCode. Feel free to play around a bit!

### Install NoSQLBench

`curl -L -O https://github.com/nosqlbench/nosqlbench/releases/latest/download/nb`

`chmod +x nb`

`sudo mv nb /usr/local/bin/`

### Upload the Secure Connect Bundle to Gitpod

(drag-and-drop, verify with `ls`)

### Configure the Astra DB token

with an `.env` file you then `source`.

```
MY_CLIENT_ID=...
MY_CLIENT_SECRET=...
```

## XXX

```
nb cql-keyvalue \
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

Add `cyclerate=100` (and `--docker-metrics`) later.
