# Web security

### Cross site scripting (XSS)
- XSS is a **code injection** attack which allows the attacker to **execute malicious JavaScript** in **another** user's browser.


### HTTPS

- redirect a HTTP request to HTTPS

#### HTTP Strict-Transport-Security

- Informs browsers that the site should only be accessed using HTTPS, and that any future attempts to access it using
  HTTP should automatically be converted to HTTPS.

```json
{
  "headers": {
    "strict-transport-security": "max-age=31536000; includeSubdomains; preload"
  }
}
```

### Cross-Origin Resource Sharing (CORS)

- Protect cookies
    - Flag HTTP Only
    - Flag Secure
    - Set Expired, Max-Age
- Restrict origin domain that can modify resources on the server.
- BE send a request contains headers to allow the origin domain to access the resources.
    - By default, the browser will check the headers and allow the request if the origin domain is in the list.

```json
{
  "headers": {
    "Access-Control-Allow-Origin": "https://example.com, http://example.com",
    "Access-Control-Allow-Methods": "GET, POST",
    "Access-Control-Allow-Headers": "X-Custom-Header"
  }
}
```

#### Cross-site Request Forgery (CSRF)

- Protect cookies
    - Flag HTTP Only
    - Flag Secure
    - Set Expired, Max-Age
- Enable captcha
- csrf_token - send from BE, FE submit form with csrf_token

#### Content Security Policy (CSP)

- CSP restrict:
    - what urls can be opened in an iframe
    - what stylesheets can be loaded
    - where requests can be made, etc.

```json
{
  "headers": {
    "Content-Security-Policy": "default-src 'self'; script-src 'self' blob: https://www.googletagmanager.com {canon_allow_url}; img-src 'self' blob: data: {stock_allow_url} {ccs_allow_url}; style-src 'self' 'unsafe-inline' {canon_allow_url}; object-src 'self' blob: {stock_allow_url}; connect-src 'self' blob: https://*.amazonaws.com/ {canon_allow_url} {stock_allow_url} https://*.posterartist.canon wss://*.posterartist.canon {ccs_allow_url} wss://*.amazonaws.com/ https://analytics.google.com  https://www.google-analytics.com; frame-src 'self' blob: {canon_allow_url} {youtube_url}"
  }
}
```

#### HTTP Strict-Transport-Security (HSTS)

- Informs browsers that the site should only be accessed using HTTPS, and that any future attempts to access it using
  HTTP should automatically be converted to HTTPS.

```json
{
  "x-xss-protection": "1; mode=block"
}
```

##### ...

```json
{
  "headers": {
    "x-content-type-options": "nosniff",
    "x-xss-protection": "1; mode=block"
  }
}
```
