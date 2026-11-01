{{- /* The source text for agents. Links stay relative, so they resolve to the markdown of the target page. */ -}}
{{- $fm := dict "title" .Title -}}
{{- range $k := slice "summary" "ecli" "datum" "instantie" "procedure" "zaaknummer" "onderwerpen" "wet" "artikel" "valid_from" "source" -}}
  {{- with index $.Params $k -}}
    {{- $v := . -}}
    {{- if in (slice "datum" "valid_from") $k }}{{ $v = time.Format "2006-01-02" . }}{{ end -}}
    {{- $fm = merge $fm (dict $k $v) -}}
  {{- end -}}
{{- end -}}
---
{{ transform.Remarshal "yaml" $fm | strings.TrimSpace }}
---

{{ .RawContent }}
