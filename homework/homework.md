# Homework "Lab" instructions

First go to the appropriate subdirectory: `cd homework` (first do a
`cd ..` if you are still in `workloads`). There you'll find
an unfinished workload `homework-workload.yaml`. Your task is to **complete
it according to the specs below** (and submit a screenshot of the final yaml
file in the "homework" form).

> _Note: the practical lab is optional for receiving the badge._
> _It is very instructive for your learning, however,_
> _so please give it a chance!_

#### The workload

You are required to test a hypothetical Astra DB application with "users" storing
metadata for some of their "images". There are two tables, whose structure
can be seen in the _schema_ phase of the provided unfinished workload yaml.

The load you are to benchmark unfolds as follows:

- first there are only writes, to both tables: there have to be four times more entries in the images table than in the users table;
- then, in the actual main phase, only reads must take place, from both tables at the same frequency. You have been asked to make sure the reads also try to retrieve rows that cannot possibly exist.

The provided workload file already does most of the job: it creates the tables,
it sort-of-writes data to them, and it sort-of performs the reads.

#### Your tasks:

1. Make sure that four times as many writes to `himages` as to `husers` occur. _Hint: use the
`ratio` parameter in one of the rampup operations - see the provided sample workloads for examples._

2. At the top of the file there are several "anonymized" bindings to choose from. Use them to finalize the `INSERT` and `SELECT` statements in the _rampup_ and _main_ phases, by replacing the `{???}` parts. The choice must satisfy the required benchmarking specifications, besides of course matching the data types in the Astra DB tables. _Hints: (1) Look at the docs on bindings; and (2) test with `driver=stdout` and very small cycle numbers for a quick assessment of what the various bindings are._

3. Check that the bindings appearing in the `SELECT` statement ensure many reads will look for rows that cannot have been inserted. _Tip: what does the function `Mod(N)` do as the cycle number increases?_

#### Useful commands, reference, advice

Info on the [`ratio` parameter](https://docs.nosqlbench.io/docs/reference/core-op-params/#ratio).

[Documentation on bindings](https://docs.nosqlbench.io/docs/bindings/binding-concepts/): you can also search for the particular functions employed in this example.

A possible way to run the workload with Astra DB would be similar to:

```
nb homework-workload astra                    \
  driver=cql                                  \
  username=${ASTRA_DB_CLIENT_ID}              \
  password=${ASTRA_DB_CLIENT_SECRET}          \
  secureconnectbundle=${ASTRA_DB_BUNDLE_PATH} \
  keyspace=${ASTRA_DB_KEYSPACE_NAME}          \
  rampup-cycles=1000                          \
  main-cycles=1000                            \
  cyclerate=50                                \
  --progress console:5s
```

On a "regular" Cassandra installation (assuming no authentication required)
that would be something like:

```
nb homework-workload astra  \
  driver=cql                \
  hosts=192.168.1.100       \
  keyspace=nbkeyspace       \
  rampup-cycles=1000        \
  main-cycles=1000          \
  cyclerate=50              \
  --progress console:5s
```

_(in this case, keep in mind that the scenario is still called "astra" simply
to denote the fact that the keyspace is supposed to already exist and will
not be created within the workload.)_

Good luck!
