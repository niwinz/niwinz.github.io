Title: Channels & CSP pattern in promesa library
Tags: penpot, clojure
Status: hidden

## A bit of context

Lets begin with how it started: at [penpot][0] we are using [core.async][1] extensivelly on the
backend background processes but specially in handling websocket connections. And it worked OK for
us, but that does not mean that it has no problems.

The [core.async][1] approach for creating lightweight processes (aka go macro) consists on a macro
transformations, that is a very clever idea but it also has its limitations.

There I can mention some examples of it:

- all yield points should be defined inline, visible to the macro and it does not span on callbacks
  and there are clear difference between blocking and parking operations
- the code inside go macro only can use parking operations and code inside threads only can use
  blocking operations.

Here you can read more on this topic [here][2] and [here][3].

And even though the pattern seems attractive for frontend code, corner cases multiply there. Just
for completeness, I leave those refences to blogs post that explain pretty well the case: [here][4]
and [here][5].


## What happened next?

With the [JDK19][6] release and the one of the most waited JEPS included: [JEP 425: Virtual Threads
(Preview)][7]; I immediatelly started experimenting on it in the [promesa][8] codebase. And after
some interations I have concluded that the virtual threads are perfect replacement for
implementation detail of core.async go blocs. So I decided to implement it on the promesa code base.

So, I pleased to announce the first **experimental** release of [promesa][8] that laverages virtual
threads and new channel implementation combined with CompletableFuture's.

The main highlights and differences with [core.async][3] are:

- **There are no macro transformations**, the `go` macro is a convenient alias for `p/vthread` (or
  `p/thread` when vthreads are not available); there are not limitation on using blocking calls
  inside `go` macro and no difference between parking and blocking.
- **No callbacks**, functions returns promises or blocks.
- **No take/put limits**; you can attach more than 1024 pending tasks to a channel.
- **Simplier mental model**, there are no differences between parking and blocking operations.
- **Analogous performance**; in my own stress tests it has the same performance as core.async.

There are [Code Walkthrought][10] where you can learn the main API usage patterns: Also the
[documentation][11] and [changelog][12].


[0]: https://github.com/penpot/penpot
[1]: https://github.com/clojure/core.async
[2]: http://danboykis.com/posts/things-i-wish-i-knew-about-core-async/
[3]: https://clojure.org/guides/core_async_go
[4]: https://mauricio.szabo.link/blog/2020/06/11/clojurescript-vs-clojure-core-async/
[5]: https://mauricio.szabo.link/blog/2022/04/22/clojurescript-vs-core-async-debate-the-last-updates/
[6]: https://openjdk.org/projects/jdk/19/
[7]: https://openjdk.org/jeps/425
[8]: https://github.com/funcool/promesa
[9]: https://kk
[10]: https://github.com/funcool/promesa/blob/master/doc/csp-walkthrought.clj
[11]:  kkk
[12]: jkk
