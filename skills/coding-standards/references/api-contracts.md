# API contracts

Use this when an HTTP route, request or response schema, or generated OpenAPI specification changes.

## Contract source

The typed API contract in code (an Effect `HttpApi`, a schema-annotated router, decorated controllers) is the source of truth. Generate the OpenAPI specification from it, format it, and inspect the diff after every contract change. Change the contract's annotations, then regenerate; a hand edit to generated JSON is lost on the next run.

## Annotations

- Give every value a generated client must supply a safe, realistic example: branded IDs, names, request bodies, lifecycle states. Importer placeholders such as `<string>` produce unusable requests.
- Describe where each identifier comes from. When one operation creates an ID another consumes, say it comes from the create response, so clients can chain requests instead of persisting instance-specific IDs.
- Include a representative success example and each public error example per operation, conforming to the production schemas and the envelope in [`public-errors.md`](public-errors.md).
- Declare every correlation response header, including on error responses, when the contract library models response headers. When it does not, omit that metadata rather than casting generated types to inject it.
- Document authentication schemes with their real header names and purpose, and verify a generated client's auth mapping by importing it.
- List only truthful server URLs. A stable local URL is fine; an invented production hostname is not.

## Versioning

When the repository has no established convention, version every route from `/v1`. Request, response, error, and persistence schema names carry no version suffix. Each endpoint has exactly one route: its versioned one.

## Completion check

The specification was regenerated from the contract, formatted, and its diff inspected; every client-supplied value has a realistic example; ID provenance and request ordering are described; each operation has success and public error examples that match production schemas; correlation headers, auth schemes, and server URLs are declared truthfully; and every route follows the repository's versioning convention.
