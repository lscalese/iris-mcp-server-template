Class dc.lmstudio.Settings Extends %RegisteredObject
{

Property BaseUrl As %String;

Property ApiKey As %String;

Property ModelName As %String;

Method %OnNew() As %Status
{
    Return $$$OK
}

ClassMethod GetInstance() As dc.lmstudio.Settings
{
    If $Data(%zLMStudioSettings) {
        Return %zLMStudioSettings
    }
    Set %zLMStudioSettings = ..LoadStoredSettings()
    Return %zLMStudioSettings
}

ClassMethod SetSettings(baseUrl As %String, apiKey As %String, modelName As %String) As %Status
{
    Set instance = ..%New()
    Set instance.BaseUrl = baseUrl
    Set instance.ApiKey = apiKey
    Set instance.ModelName = modelName
    Set %zLMStudioSettings = instance
    Return $$$OK
}

ClassMethod LoadStoredSettings() As dc.lmstudio.Settings
{
    Set instance = ..%New()
    Set instance.ApiKey = $Get(^lmstudio("ApiKey"),"sk-lm-3Jg5KGkk:jzADlTeNc6auuNFlOZZ7")
    Set instance.BaseUrl = $Get(^lmstudio("BaseUrl"), "http://host.docker.internal:8095")
    Set instance.ModelName = $Get(^lmstudio("ModelName"), "mistralai/magistral-small-2509")
    Return instance
}

}
