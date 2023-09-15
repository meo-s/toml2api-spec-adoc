# toml2api-spec-adoc

Spring REST Docs에 의해 생성된 스니펫과 부가적인 TOML 설정 파일을 기반으로 간단한 adoc 파일을 생성해줍니다.

## Example

**`greet-controller.toml`**

```toml
[GreetController]
api-name = 'Greet API'
api-description = 'Welcome!'

[[GreetController.api-cases]]
priority = 0
name = 'main'
display-name = 'Main'
description = 'This section also could be described.'

[GreetController.api-cases.request]
description = 'This is normal request.'

[GreetController.api-cases.response]
description = 'This is normal response.'

[[GreetController.api-cases]]
name = 'partial-params'
emit = true
```

**Generated `greet-api.adoc`**

```adoc
= Greet API

Welcome!

== Main

=== Request

This is main request.

==== Sample

include::xxx/build/generated-snippets/GreetController/main/http-request.adoc[]

==== Query Parameters

include::xxx/build/generated-snippets/GreetController/main/query-parameters.adoc[]

=== Response

This is main response.

==== Sample

include::xxx/build/generated-snippets/GreetController/main/http-response.adoc[]

==== Fields

include::xxx/build/generated-snippets/GreetController/main/response-fields.adoc[]
```
