# Nearby search and address picking

Define the query origin explicitly. Nearby search can use a qualified device fix, the visible map area, or a chosen pin. Preserve the user's chosen origin when location changes. Set the search boundary, units, filters, and result ordering according to the existing API contract. Avoid presenting distance from an approximate origin as exact or substituting straight-line distance for travel distance or ETA.

- Use viewport-idle search, debouncing, or an explicit search-this-area action as appropriate. Coalesce equivalent requests and bound provider traffic. Couple each response and error to the originating query, viewport and filters. Cancel obsolete requests where supported and reject late results regardless of cancellation. Distinguish pending, empty, failure, and any retained results from an older query.
- Normalize coordinate order and units at each boundary. GeoJSON positions are longitude then latitude, while map or application types can take a different order. Use asymmetric test coordinates to catch swaps. Handle longitude wrap if querying regions that can cross the antimeridian.
- Treat geocoding or reverse geocoding as candidate data. Keep a selected pin separate from a provisional address label. Use a latest-request guard so a late address lookup cannot rename a newer pin. Show no match, ambiguity, quota errors, or offline status without silently substituting a different address. Confirm the user's selected location before committing a delivery address.
- Follow the chosen provider's constraints on credentials, storage, attribution, and quotas. Minimize exact coordinates in telemetry and logs. Use synthetic coordinates and fake transport to prove ordering and selection, then verify any claimed provider response, address quality, or map behavior in its actual environment.

## Sources

- [GeoJSON position contract](https://www.rfc-editor.org/rfc/rfc7946#section-3.1.1)
- [Example geocoding response and precision contract](https://developers.google.com/maps/documentation/geocoding/requests-geocoding)
- [Example geocoding usage and storage policy](https://developers.google.com/maps/documentation/geocoding/policies)
