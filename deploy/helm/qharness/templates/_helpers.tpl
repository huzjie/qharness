{{- define "qharness.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{- define "qharness.fullname" -}}
{{- .Release.Name }}-{{ include "qharness.name" . }}
{{- end }}
