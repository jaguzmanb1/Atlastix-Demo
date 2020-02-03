
## Atlastix Pipeline for `<DATASOURCE>`

general aspects:

* Elasticsearch / Kibana version is 7.5.2
* Python used version 3.8.1
* kibana Object that contains, a dashboard, visualizations and a index pattern

### Directory layout

Path | Contents
--- | ---
`/collector/` | the thing that collects data from a source (Python)
`/kibana/` | viz/dashboard/index-pattern artefacts
`/sourceconfig/` | documentation of any required data source config (creds/perms)
