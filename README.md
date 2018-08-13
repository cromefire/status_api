# Status API
Simple api to check if an (internal) endpoint is up, without exposing data or a port.

## Usage

### Setup
1. Clone repo into some location (accessible to webserver)
2. Create a new backup file in one of this locations: `<repo>/eps.{yaml|json}`, `/etc/status_api.{yaml|json}`
    (used in that order, you obviously shouldn't use to global file, if you have multiple instances)
3. Populate them with a config of this schema: `<api endpoint>: <query url>`
    (**Tip**: Prometheus endpoints are suitable as query url, as this does not leak the metrics, but only the status.)

4. Configure your webserver to use the WSGI interface at `<repo>/src/status_api/app.wsgi`

### Frontend
From your frontend you can now hit `<your configured url>/<your configured endpoint>` and use the results

### Status codes
- 200: Got a good status, with content
- 204: Good status, but no content
- 404: No such endpoint _(`code` not returned)_
- 502: Bad status code from endpoint
- 503: Connection error _(`code` not returned)_
- 504: Timeout while hitting query url _(`code` not returned)_

You have to decide which ones are bad for you (e.g. 203 can be bad or good)
     your frontend should handle these

## Example
`/path/to/cloned/repo/eps.yaml`:
```yaml
service1/database: "http://localhost:9482/metrics"
service1: "http://localhost:4563/status"
```

The webserver is configured to host this at `https://example.com/status`

If you hit it at `https://example.com/status/service1/database`, the following happens
    (may vary of course, depending on status):

1. The server finds out that the query url for this is `http://localhost:9482/metrics`
2. It hits `http://localhost:9482/metrics` and gets status code 200, but no body
3. The server returns status 204 and the json object `{"status": 204, "msg": "Empty body", "code": 200}`
    (`code` is not defined when a timeout happens or the endpoint does not exist, you should handle that case)
