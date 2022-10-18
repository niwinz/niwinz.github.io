Title: How IDs are generated in Penpot
Tags: penpot, clojure
Status: hidden

Let's begin by mentioning that this post was originated from a conversation I had with the
[Taiga][9] development team about how we generate ID’s in [Penpot][0]. The idea was to know what
decisions we have made in this regard and understand the implementation details.

At [Penpot][0], since its inception, we made the decision to use [UUID][1] to generate ID's. If you
are not familiar with the subject, you’ll find useful this [good article on wikipedia][2] that
explains a bit about UUID. The simplest rationale for generating IDs is that we needed to be able to
create IDs on both the frontend and the backend. From the start, we already had a distributed ID
generation scenario but a simple incremental in the database table was not enough for us.

The quick approach would have been to use the typical UUID **v4**, but as this variant is mainly
generated with random data it implies certain problems: it’s not sortable and causes fragmentation
in the database indexes, thus degrading query performance over time. So we began by using UUID v1.

What alternatives we considered before choosing UUID?  We also considered several alternatives
before going via the UUID route:

- [ulid][3]: The basic idea behind ulid is very interesting because it is very close to the final
  solution we have taken. The main problem it’s to do with the fact that if we want to store it
  efficiently, we would have to decode the value to two int64s and store it in the database in two
  separate fields, which would make all queries more cumbersome. I’m aware that, as an alternative,
  we can take advantage of the UUID type of the database to store the 128 bits of this ID there, but
  semantically it would be possibly confusing. Storing it in a string format is not an option,
  because that would imply having more data to store and therefore larger indexes. 
- [sno][4]: in the same line as ulid, implemented only in go
- [nanoid][5]: very similar to UUID v4. Plus you need to save the value as a string, hence we
  discarded this option very quickly.

There are many custom implementations with different characteristics and there are no plan for list
them all.

Clearly, our choice to use UUID v1 doesn't comes without its own problems: unlike v4, it's partially
sortable because it strangely places the least significant bits of timestamp at the start in binary
encoding, unusual 100-ns precision gregorian epoch, and also it needs access to the MAC address
among other less important things. As for our case, we expected to use it always in virtual
environments, so the access to MAC was not so problematic. And at the frontend, we emulated the mac
generating random data in the first use.

After the conversation, I've decided to review how we're generating uuids and I've come across this
[new revision of the UUID RFC][6] where the new 3 UUID formats are outlined: the v6, v7 and v8.

To summarize, we have v6 which is similar to v1 with an improved timestamp bits ordering, v7 (with
its variants 1 and 2) mixes between v4 and v6 ,with a more standard epoch, precision in milliseconds
combining it with a random part instead of the MAC address. And finally v8, which basically defines
only the minimum necessary to preserve compatibility with the rest of the formats and leaves the
rest to the choice of the custom implementation.

For Penpot, I have chosen to take good ideas from ULID and UUID v6 and implement a custom one using
the UUID v8 format. These are the properties of our new UUID implementation:

- 48bits timestamp (milliseconds precision, custom epoch: 2022-01-01 00:00:00)
- 14bits random clockseq (monotonically increasing on timestamp collision, allows 16384 ids/ms per host)
- blocks (no exceptions raised) if clockseq overflows
- 56bits of randomness, generated on library initialization
- 4bits for user defined tag (allows distinguish between environments where the ID is generated)
- don’t run out of range until 10941 AD
- on clock regression, the 56bits of static randomness are reinitialized

With this: we maintain compatibility with the current solution as we continue to use the same type
of data that is efficiently stored in the database; have better visual readability; better
sortability and greatly improved performance. You can take a look at the [JVM implementation
here][7] and the [JS implementation here][8].

Here below is a benchmark that illustrates the difference in performance between different
implementations and versions:


```text
;; This is a standard jdk way of generate UUID v4
user=> (perf/bench :f #(java.util.UUID/randomUUID) :name "uuid-v4-java")
=> benchmarking: uuid-v4-java
--> TOTAL: 9.95sec
--> MEAN:  668.6ns

;; This is the implementation we used previously
;; https://github.com/danlentz/clj-uuid
user=> (perf/bench :f #(clj-uuid/v1) :name "uuid-v1-clj")
=> benchmarking: uuid-v1-clj
--> TOTAL: 10.01sec
--> MEAN:  300.16ns

;; This is third-party java library that generates UUID v1
user=> (perf/bench :f #(UuidCreator/getTimeBased) :name "uuid-v1-java-uc")
=> benchmarking: uuid-v1-java-uc
--> TOTAL: 10.02sec
--> MEAN:  100.74ns

;; This is third-party java library that generates UUID v7 (canonical)
user=> (perf/bench :f #(UuidCreator/getTimeOrderedEpoch) :name "uuid-v7.0-java-uc")
=> benchmarking: uuid-v7.0-java-uc
--> TOTAL: 10.52sec
--> MEAN:  448.02ns

;; This is third-party java library that generates UUID v7 (variant 1)
user=> (perf/bench :f #(UuidCreator/getTimeOrderedEpochPlus1) :name "uuid-v7.1-java-uc")
=> benchmarking: uuid-v7.1-java-uc
--> TOTAL: 10.33sec
--> MEAN:  97.86ns

;; This is our in-house implementation of UUID v8
user=> (perf/bench :f #(app.common.UUIDv8/create) :name "uuid-v8-java-penpot")
=> benchmarking: uuid-v8-java-penpot
--> TOTAL: 10.09sec
--> MEAN:  89.26ns
```

[0]: https://penpot.app
[1]: https://www.rfc-editor.org/rfc/rfc4122.html
[2]: https://en.wikipedia.org/wiki/Universally_unique_identifier
[3]: https://github.com/ulid/spec
[4]: https://github.com/muyo/sno
[5]: https://github.com/ai/nanoid
[6]: https://datatracker.ietf.org/doc/html/draft-peabody-dispatch-new-uuid-format
[7]: https://github.com/penpot/penpot/blob/develop/common/src/app/common/UUIDv8.java
[8]: https://github.com/penpot/penpot/blob/develop/common/src/app/common/uuid_impl.js
[9]: https://taiga.io
